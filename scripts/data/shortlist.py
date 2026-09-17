from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
import json
import pathlib
from PIL import Image, ImageDraw

rows = []
for line in pathlib.Path("screening.log").read_text().splitlines():
    if line.startswith('{"index"'):
        rows.append(json.loads(line))
c = [
    r
    for r in rows
    if 120 <= r["n"] <= 375 and r["instruction"] and "/success/" in r["metadata"]["file_path"]
]
print("\n".join(f"{r['index']}: {r['n'] / 15:.1f}s {r['instruction']}" for r in c))
for k in range(0, len(c), 12):
    batch = c[k : k + 12]
    im = Image.new("RGB", (960, 140 * len(batch)), "white")
    for j, r in enumerate(batch):
        s = Image.open(f"artifacts/candidates/{r['index']:03d}.jpg")
        s = s.resize((480, 210))
        # use original start views and middle ext1 to retain readability
        src = Image.open(f"artifacts/candidates/{r['index']:03d}.jpg")
        for a, (x, y) in enumerate([(0, 60), (0, 240), (320, 60)]):
            im.paste(src.crop((x, y, x + 320, y + 180)).resize((240, 135)), (a * 240, j * 140))
        ImageDraw.Draw(im).text(
            (724, j * 140 + 4),
            f"{r['index']}: {r['n'] / 15:.1f}s\n"
            + r["instruction"][:35]
            + "\n"
            + r["instruction"][35:70],
            fill="black",
        )
    im.save(f"artifacts/overview_{k // 12}.jpg")
