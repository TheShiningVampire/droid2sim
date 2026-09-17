from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
"""Offline image measurements and limited kinematic response identification. No simulation steps."""
import json
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = REPO_ROOT
OUT = ROOT / "artifacts/measurements"
OUT.mkdir(exist_ok=True)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
a = np.load(ROOT / "data/episode/trajectory.npz")
q = a["joint_position"]
u = a["action_joint_position"]
dt = 1 / 15
split = 120
response = []
for j in range(7):
    fits = []
    for lag in [0, 1, 2]:
        ids = np.arange(max(lag, 0), split - 1)
        x = u[ids - lag, j] - q[ids, j]
        dy = q[ids + 1, j] - q[ids, j]
        b = float(np.clip(x @ dy / max(x @ x, 1e-12), 0, 1))
        mse = float(np.mean((dy - b * x) ** 2))
        fits.append((mse, lag, b))
    _, lag, b = min(fits)
    ids = np.arange(split, len(q) - 1)
    actual = q[ids + 1, j]
    pred = q[ids, j] + b * (u[ids - lag, j] - q[ids, j])
    base = q[ids, j]
    rmse = float(np.sqrt(np.mean((pred - actual) ** 2)))
    hold = float(np.sqrt(np.mean((base - actual) ** 2)))
    response.append(
        dict(
            joint=j + 1,
            command_lag_steps=lag,
            discrete_response_fraction=b,
            equivalent_first_order_rate_s_inv=float(-np.log(max(1 - b, 1e-9)) / dt),
            heldout_one_step_rmse_rad=rmse,
            hold_last_state_baseline_rmse_rad=hold,
            relative_improvement=1 - rmse / hold if hold else None,
            train_steps=split,
            test_transitions=len(ids),
        )
    )
notes = [
    "This is an offline first-order command-response surrogate, not identification of physical mass, inertia, friction or contact stiffness.",
    "Fits action_dict/joint_position against observed q[k+1]; exact actuator command timing and internal DROID control interpolation are unavailable.",
    "One-step held-out predictions condition on observed q[k]; this is not a free-running validation or a MuJoCo parameter fit.",
    "The current simulation replays observed joint states, not these action commands. These coefficients must not be substituted directly for actuator kp.",
    "No identified parameter was applied to the final scene; five-iteration cap preserved.",
]
json.dump(
    dict(model="q[k+1]=q[k]+b*(command[k-lag]-q[k])", fits=response, limitations=notes),
    open(OUT / "joint_response_surrogate.json", "w"),
    indent=2,
)


# Track the distinctive teal cap only; missing or uncertain detections remain missing.
def track(frames, anchor, minimum_area=5):
    last = np.array(anchor, dtype=float)
    rows = []
    for t, im in enumerate(frames):
        hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, np.array([72, 75, 30]), np.array([105, 255, 235]))
        mask[:40] = 0
        mask[145:] = 0
        mask[:, :85] = 0
        mask[:, 210:] = 0
        count, labels, st, cent = cv2.connectedComponentsWithStats(mask)
        candidates = [
            i
            for i in range(1, count)
            if minimum_area <= st[i, 4] <= 100 and np.linalg.norm(cent[i] - last) < 25
        ]
        if candidates:
            i = min(candidates, key=lambda i: np.linalg.norm(cent[i] - last))
            point = cent[i]
            area = int(st[i, 4])
            last = point.copy()
            rows.append(dict(frame=t, visible=True, xy=point.tolist(), area=area))
        else:
            rows.append(dict(frame=t, visible=False, xy=None, area=0))
    return rows


real = np.load(ROOT / "data/episode/ext1.npy")
sim = np.load(ROOT / "artifacts/final/sim_ext1.npy")
r = track(real, [161, 128])
s = track(sim, [161, 128], 3)
json.dump(
    dict(
        real=r,
        sim=s,
        method="HSV teal-cap connected components, bounded workspace, area limits, nearest previous detection within25px; no interpolation of missing detections",
        limitations="Automatic appearance-based estimates; cap centroid is not marker COM; perspective and occlusion change centroid. Exterior1 only; not 3D ground truth.",
    ),
    open(OUT / "cap_tracks_ext1.json", "w"),
    indent=2,
)
valid = [i for i in range(len(r)) if r[i]["visible"] and s[i]["visible"]]
err = {i: float(np.linalg.norm(np.array(r[i]["xy"]) - s[i]["xy"])) for i in valid}
metrics = dict(
    matched_frames=len(valid),
    total_frames=len(r),
    mean_cap_pixel_error=float(np.mean(list(err.values()))),
    median_cap_pixel_error=float(np.median(list(err.values()))),
    max_cap_pixel_error=float(max(err.values())),
    final_cap_pixel_error=err.get(180),
    phase_mean_error_px={
        name: float(np.mean([err[i] for i in ids if i in err]))
        for name, ids in [
            ("before_grasp", range(0, 96)),
            ("grasp", range(96, 120)),
            ("transport", range(120, 153)),
            ("release_final", range(153, 181)),
        ]
    },
    warning="Automatic color-cap correspondences, visually reviewed on sampled frames; errors combine camera, object pose/geometry and motion differences.",
)
json.dump(metrics, open(OUT / "visual_error.json", "w"), indent=2)
ids = list(range(0, 181, 15)) + [110, 125, 155]
sheet = Image.new("RGB", (4 * 640, 4 * 220), "#111822")
for j, t in enumerate(ids):
    x = (j % 4) * 640
    y = (j // 4) * 220
    for k, frames, rows, color in [(0, real, r, "lime"), (1, sim, s, "cyan")]:
        im = Image.fromarray(frames[t])
        d = ImageDraw.Draw(im)
        if rows[t]["visible"]:
            u, v = rows[t]["xy"]
            d.ellipse((u - 5, v - 5, u + 5, v + 5), outline=color, width=2)
        sheet.paste(im, (x + k * 320, y + 30))
    ImageDraw.Draw(sheet).text(
        (x + 5, y + 4),
        f"frame {t} | real teal cap / sim teal cap | error {err.get(t, float('nan')):.1f}px",
        font=ImageFont.truetype(F, 15),
        fill="white",
    )
sheet.save(OUT / "tracking_review.jpg")
print(json.dumps(metrics, indent=2))
print("Joint response surrogate:", json.dumps(response, indent=2))
