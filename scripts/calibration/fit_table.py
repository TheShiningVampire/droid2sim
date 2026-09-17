from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
import cv2
import numpy as np
import json
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

cams = json.load(open("cameras.json"))
corr = json.load(open("artifacts/calibration_correspondences.json"))
points = np.array(corr["world_pinch_points"])
uvs = corr["annotations"]
params = []
contours = []
for name in ["ext1", "ext2"]:
    im = np.load("data/episode/" + name + ".npy")[0]
    mask = cv2.inRange(im, np.array([180, 180, 180]), np.array([255, 255, 255]))
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cont = max(cs, key=cv2.contourArea)[:, 0].astype(float)
    contours.append(cont[::3])
    print(name, cv2.fitEllipse(cont.astype(np.float32)))
    T = np.linalg.inv(cams[name]["cam_to_world"])
    params.extend(
        np.r_[Rotation.from_matrix(T[:3, :3]).as_rotvec(), T[:3, 3], cams[name]["K"][0][0]]
    )
theta = np.linspace(0, 2 * np.pi, 180)
params.extend([0.65, -0.09, -0.10, 0.30])


def residual(x):
    table = np.c_[
        x[14] + x[17] * np.cos(theta), x[15] + x[17] * np.sin(theta), np.full(len(theta), x[16])
    ]
    out = []
    for j, name in enumerate(["ext1", "ext2"]):
        p = x[j * 7 : j * 7 + 7]
        K = np.array([[p[6], 0, 160], [0, p[6], 90], [0, 0, 1.0]])
        proj = cv2.projectPoints(points, p[:3], p[3:6], K, None)[0][:, 0]
        out.extend(((proj - np.array(uvs[name])) / 3).ravel())
        pp = cv2.projectPoints(table, p[:3], p[3:6], K, None)[0][:, 0]
        # Symmetric contour distances constrain circular tabletop in both cameras.
        dist = np.linalg.norm(pp[:, None, :] - contours[j][None, :, :], axis=2)
        out.extend(dist.min(axis=0) / 3)
        out.extend(dist.min(axis=1)[::3] / 3)
        out.append((p[6] - 135) / 25)
    out.append((x[17] - 0.30) / 0.06)
    return out


lo = np.r_[[-np.inf] * 6, 100, [-np.inf] * 6, 100, 0.3, -0.5, -0.25, 0.2]
hi = np.r_[[np.inf] * 6, 230, [np.inf] * 6, 230, 1.0, 0.3, 0.03, 0.5]
f = least_squares(residual, params, bounds=(lo, hi), loss="soft_l1", max_nfev=200)
print("table", f.x[14:], "cost", f.cost)
for j, name in enumerate(["ext1", "ext2"]):
    p = f.x[j * 7 : j * 7 + 7]
    T = np.eye(4)
    T[:3, :3] = Rotation.from_rotvec(p[:3]).as_matrix()
    T[:3, 3] = p[3:6]
    cams[name]["cam_to_world"] = np.linalg.inv(T).tolist()
    cams[name]["K"][0][0] = cams[name]["K"][1][1] = float(p[6])
    cams[name]["source"] += "; jointly refined using circular tabletop silhouette"
    print(name, p[6], np.linalg.inv(T)[:3, 3])
json.dump(cams, open("cameras.json", "w"), indent=2)
json.dump(
    dict(
        center=f.x[14:17].tolist(),
        radius=float(f.x[17]),
        method="joint camera and circular table silhouette fit; horizontal table assumed",
    ),
    open("artifacts/table_fit.json", "w"),
    indent=2,
)
