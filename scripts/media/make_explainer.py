from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
"""Generate a short, silent captioned explainer entirely from local artifacts."""
import textwrap
import numpy as np
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont

ROOT = REPO_ROOT
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(n, b=False):
    return ImageFont.truetype(BOLD if b else FONT, n)


BG = "#111822"
FG = "#edf2f8"
MUTED = "#b1c0d1"
BLUE = "#77c3ff"
GREEN = "#77dfaf"
RED = "#ff9b94"
real = {n: np.load(ROOT / f"data/episode/{n}.npy") for n in ["ext1", "ext2", "wrist"]}
sim = np.load(ROOT / "artifacts/final/sim_ext1.npy")
fails = {i: np.load(ROOT / f"artifacts/iteration{i}/sim_ext1.npy") for i in [1, 3, 4, 5]}
a = np.load(ROOT / "data/episode/trajectory.npz")


def canvas(title, sub):
    im = Image.new("RGB", (1280, 720), BG)
    d = ImageDraw.Draw(im)
    d.text((40, 30), title, font=font(36, True), fill=FG)
    d.text((40, 85), sub, font=font(22), fill=MUTED)
    return im, d


def text(d, xy, s, size=24, color=FG, width=80):
    x, y = xy
    for line in textwrap.wrap(s, width):
        d.text((x, y), line, font=font(size), fill=color)
        y += size + 11
    return y


def paste(im, frame, xy, size):
    im.paste(Image.fromarray(frame).resize(size), xy)


fps = 15
duration = 42
out = ROOT / "pipeline_explainer.mp4"
with imageio.get_writer(out, fps=fps, macro_block_size=1, quality=8) as writer:
    for frame in range(duration * fps):
        t = frame / fps
        chapter = int(t // 6)
        u = t % 6
        idx = min(int(u / 6 * 181), 180)
        if chapter == 0:
            im, d = canvas(
                "One real episode → one MuJoCo replay",
                "Real-to-sim reconstruction | DROID → estimated scene → position-controlled replay",
            )
            paste(im, real["ext1"][idx], (40, 160), (590, 332))
            paste(im, sim[idx], (650, 160), (590, 332))
            d.text((55, 173), "REAL INPUT", font=font(24, True), fill=RED)
            d.text((665, 173), "SIMULATION", font=font(24, True), fill=BLUE)
            text(
                d,
                (40, 525),
                "Task: “Take the pen out of the bowl and place it on the table.”",
                27,
                width=80,
            )
            text(
                d,
                (40, 577),
                "181 recorded steps • 15 Hz nominal • 12.07 s • robot base = world frame",
                23,
                color=MUTED,
                width=100,
            )
        elif chapter == 1:
            im, d = canvas(
                "Input 1: three synchronized image streams",
                "Exterior 1 + exterior 2 + wrist camera | RLDS images: 320 × 180",
            )
            for j, n in enumerate(["ext1", "ext2", "wrist"]):
                paste(im, real[n][idx], (40 + j * 408, 185), (384, 216))
                d.text((40 + j * 408, 145), n.upper(), font=font(25, True), fill=BLUE)
            text(
                d,
                (40, 450),
                "The selected episode’s raw-release folder is missing. Its HD stereo video, camera metadata and measured depth are unavailable.",
                28,
                width=78,
            )
            text(
                d,
                (40, 565),
                "We use the permitted RLDS fallback. No depth from another episode is used.",
                24,
                color=RED,
                width=90,
            )
        elif chapter == 2:
            im, d = canvas(
                "Input 2: recorded robot motion + language",
                "Joint observations q1…q7, normalized gripper closure, and task instruction",
            )
            q = a["joint_position"]
            colors = ["#7bc4ff", "#ffbc76", "#83e2bd", "#db9aff", "#ff8991", "#e3dc72", "#a1adc2"]
            x0, y0, w, h = 65, 180, 800, 280
            d.rectangle((x0, y0, x0 + w, y0 + h), outline="#415369", width=2)
            for j in range(7):
                yy = (q[:, j] - q.min()) / (q.max() - q.min())
                pts = [(x0 + k / (len(q) - 1) * w, y0 + h * (1 - v)) for k, v in enumerate(yy)]
                d.line(pts, fill=colors[j], width=3)
            d.line((x0 + idx / 180 * w, y0, x0 + idx / 180 * w, y0 + h), fill=FG, width=2)
            text(d, (925, 200), "7 joints", 32, color=BLUE, width=14)
            text(d, (925, 280), "1 gripper", 32, color=GREEN, width=14)
            text(
                d,
                (40, 505),
                "Every recorded sample is preserved. Only interpolation between samples supplies 1 ms physics steps.",
                28,
                width=80,
            )
            text(
                d,
                (40, 610),
                "Trajectory SHA256 is checked before every replay.",
                23,
                color=MUTED,
                width=100,
            )
        elif chapter == 3:
            im, d = canvas(
                "Method: fit the scene around the fixed motion",
                "Official Menagerie Panda + Robotiq 2F-85 models",
            )
            labels = [
                (
                    "CAMERAS",
                    "Manual robot landmarks\n+ known forward kinematics\n+ table silhouette",
                ),
                ("SCENE", "Circular table\nOpen collision bowl\nCapsule marker"),
                ("PHYSICS", "Native position actuators\nDynamic object contacts\nNo grasp welds"),
            ]
            for j, (title, desc) in enumerate(labels):
                x = 40 + j * 410
                d.rounded_rectangle(
                    (x, 175, x + 380, 445), radius=18, fill="#1d2b3a", outline="#435d76", width=2
                )
                d.text((x + 20, 195), title, font=font(28, True), fill=BLUE)
                for k, line in enumerate(desc.split("\n")):
                    d.text((x + 20, 260 + 43 * k), line, font=font(20), fill=FG)
            text(
                d,
                (40, 500),
                "Camera calibration, object dimensions, initial poses and physical parameters are estimates. The recorded robot trajectory is never optimized.",
                27,
                width=83,
            )
        elif chapter == 4:
            im, d = canvas(
                "Verification: watch the failures, too",
                "Five scene iterations used | four failed | one task-level success",
            )
            for j, i in enumerate([1, 3, 4, 5]):
                x = 40 + (j % 2) * 620
                y = 155 + (j // 2) * 230
                paste(im, fails[i][idx], (x, y), (400, 225))
                d.text((x + 416, y + 35), f"#{i} FAIL", font=font(24, True), fill=RED)
            text(
                d,
                (40, 640),
                "All failed simulations are preserved in VIDEOS.html and artifacts/iteration*/.",
                21,
                color=MUTED,
                width=110,
            )
        elif chapter == 5:
            im, d = canvas(
                "Retained result: qualitative pick-and-place",
                "Iteration 2 | success.py = true | not a validated physical reconstruction",
            )
            paste(im, real["ext1"][idx], (40, 155), (590, 332))
            paste(im, sim[idx], (650, 155), (590, 332))
            text(
                d,
                (40, 515),
                "The marker leaves the bowl and ends on the table. Grasp orientation differs, and maximum marker-contact penetration is 4.23 mm.",
                27,
                width=80,
            )
            text(
                d,
                (40, 620),
                "Lower-penetration variants failed. Contact sensitivity remains unresolved.",
                23,
                color=RED,
                width=100,
            )
        else:
            im, d = canvas(
                "Have we done system identification?",
                "Not physical SysID: no fitted mass, friction or contact parameters validated against real motion",
            )
            text(
                d,
                (55, 175),
                "Done: camera/geometry fitting and manual scene-parameter trials.",
                30,
                color=GREEN,
                width=73,
            )
            text(
                d,
                (55, 285),
                "Not done: a quantitative dynamic-parameter fit to tracked real object motion, with independent validation.",
                30,
                color=RED,
                width=73,
            )
            text(
                d,
                (55, 425),
                "Now measured: cap-image error and a held-out joint-response surrogate. Physical mass/friction/contact SysID remains undone.",
                28,
                width=78,
            )
            text(
                d,
                (55, 565),
                "The original five-scene-iteration cap is reached. No additional physics trials are hidden.",
                24,
                color=MUTED,
                width=88,
            )
        if chapter in [0, 1, 4, 5]:
            d.text((940, 118), "Illustrative playback ~2x", font=font(17), fill=MUTED)
        d.rectangle((40, 695, 1240, 701), fill="#344152")
        d.rectangle((40, 695, 40 + 1200 * t / duration, 701), fill=BLUE)
        writer.append_data(np.array(im))
        if frame % 90 == 0:
            im.save(ROOT / f"artifacts/explainer_chapter_{chapter}.jpg")
print(out)
