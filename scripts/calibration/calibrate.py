from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
import os

os.environ["MUJOCO_GL"] = "egl"
import mujoco
import numpy as np
import cv2
import json
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
from PIL import Image, ImageDraw
from droid2sim.data.download import log

m = mujoco.MjModel.from_xml_path("robot.xml")
d = mujoco.MjData(m)
a = np.load("data/episode/trajectory.npz")
indices = [60, 90, 110, 120, 130, 150, 160, 180]
annotations = {
    "ext1": [
        [155, 80],
        [170, 117],
        [170, 122],
        [177, 98],
        [149, 76],
        [119, 111],
        [113, 109],
        [102, 79],
    ],
    "ext2": [
        [177, 20],
        [181, 49],
        [178, 50],
        [179, 36],
        [178, 32],
        [198, 80],
        [190, 66],
        [188, 46],
    ],
}
points = []
for t in indices:
    d.qpos[:7] = a["joint_position"][t]
    mujoco.mj_forward(m, d)
    points.append(d.site("rq_pinch").xpos.copy())
points = np.array(points)
cams = {}
for name, uv in annotations.items():
    uv = np.array(uv, dtype=float)
    K = np.array([[135.0, 0, 160], [0, 135, 90], [0, 0, 1.0]])
    ok, rv, tv = cv2.solvePnP(points, uv, K, None, flags=cv2.SOLVEPNP_SQPNP)

    def residual(x):
        k = K.copy()
        k[0, 0] = k[1, 1] = x[6]
        pred = cv2.projectPoints(points, x[:3], x[3:6], k, None)[0][:, 0]
        return np.r_[(pred - uv).ravel(), (x[6] - 135) / 15]

    fit = least_squares(
        residual,
        np.r_[rv.ravel(), tv.ravel(), 135.0],
        bounds=(np.r_[[-np.inf] * 6, 100], np.r_[[np.inf] * 6, 230]),
        loss="soft_l1",
    )
    K[0, 0] = K[1, 1] = fit.x[6]
    T = np.eye(4)
    T[:3, :3] = Rotation.from_rotvec(fit.x[:3]).as_matrix()
    T[:3, 3] = fit.x[3:6]
    T = np.linalg.inv(T)
    cams[name] = dict(
        width=320,
        height=180,
        K=K.tolist(),
        cam_to_world=T.tolist(),
        source="estimated PnP from manually marked Menagerie pinch location; focal fitted with prior 135px, centered principal point, zero distortion assumed",
        annotation_indices=indices,
        annotation_pixels=uv.tolist(),
        rmse_px=float(np.sqrt(np.mean(residual(fit.x)[:-1] ** 2))),
    )
    print(
        name,
        "f",
        K[0, 0],
        "cam",
        T[:3, 3],
        "rmse",
        cams[name]["rmse_px"],
        "residual",
        residual(fit.x)[:-1].reshape(-1, 2),
    )
    frames = np.load("data/episode/" + name + ".npy")
    sheet = Image.new("RGB", (640, 180 * 4))
    for j, t in enumerate(indices):
        im = Image.fromarray(frames[t])
        draw = ImageDraw.Draw(im)
        q = cv2.projectPoints(points[j], fit.x[:3], fit.x[3:6], K, None)[0].ravel()
        u = uv[j]
        draw.ellipse((q[0] - 3, q[1] - 3, q[0] + 3, q[1] + 3), outline="red")
        draw.ellipse((u[0] - 3, u[1] - 3, u[0] + 3, u[1] + 3), outline="lime")
        draw.text((2, 2), str(t), fill="red")
        sheet.paste(im, ((j % 2) * 320, (j // 2) * 180))
    sheet.save("artifacts/calibration_" + name + ".jpg")
json.dump(cams, open("cameras.json", "w"), indent=2)
json.dump(
    {"indices": indices, "world_pinch_points": points.tolist(), "annotations": annotations},
    open("artifacts/calibration_correspondences.json", "w"),
    indent=2,
)


# Triangulate measured table and bowl centers, marker endpoints. Approximate centers of perspective ellipses are biased.
def triangulate(a, b):
    P = []
    for name in ["ext1", "ext2"]:
        c = cams[name]
        P.append(np.array(c["K"]) @ np.linalg.inv(c["cam_to_world"])[:3])
    p = cv2.triangulatePoints(
        P[0], P[1], np.array(a, dtype=float).reshape(2, 1), np.array(b, dtype=float).reshape(2, 1)
    )
    return (p[:3] / p[3]).ravel()


for label, u, v in [
    ("bowl_center", (168, 116), (181, 53)),
    ("pen_end1", (158, 129), (187, 57)),
    ("pen_end2", (177, 113), (172, 55)),
    ("table_center", (138, 109), (166, 94)),
]:
    print(label, triangulate(u, v))
log(
    "Fallback camera estimates: manually annotated eight pinch locations per exterior camera; solvePnP then robust refinement with focal prior 135 px +/-15 (320x180). Principal point at image center, zero lens distortion assumed. Save correspondences and reprojection overlays. This estimates calibration; it is not released ground truth."
)
