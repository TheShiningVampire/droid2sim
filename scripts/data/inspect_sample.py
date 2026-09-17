from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import tensorflow_datasets as tfds
from PIL import Image, ImageDraw
import json
from droid2sim.data.download import log

root = REPO_ROOT
b = tfds.builder_from_directory(str(root / "data/droid_100/1.0.0"))
(root / "sources/actual_schema.txt").write_text(str(b.info))
print(b.info, flush=True)
out = root / "artifacts/candidates"
out.mkdir(parents=True, exist_ok=True)
rows = []
for i, e in enumerate(tfds.as_numpy(b.as_dataset(split="train", shuffle_files=False))):
    steps = list(e["steps"])
    n = len(steps)
    meta = {k: v.decode() for k, v in e["episode_metadata"].items()}
    lang = steps[0]["language_instruction"].decode()
    row = dict(
        index=i,
        n=n,
        duration_assuming_15hz=n / 15,
        instruction=lang,
        metadata=meta,
        reward=float(steps[-1]["reward"]),
    )
    rows.append(row)
    print(json.dumps(row), flush=True)
    sheet = Image.new("RGB", (320 * 3, 180 * 2 + 60), "white")
    d = ImageDraw.Draw(sheet)
    d.text((5, 5), f"{i}: {n}/15={n / 15:.1f}s {lang[:110]}", fill="black")
    for c, key in enumerate(["exterior_image_1_left", "exterior_image_2_left"]):
        for j, t in enumerate([0, n // 2, n - 1]):
            sheet.paste(Image.fromarray(steps[t]["observation"][key]), (320 * j, 60 + 180 * c))
    sheet.save(out / f"{i:03d}.jpg")
(root / "artifacts/episodes.json").write_text(json.dumps(rows, indent=2))
log(
    "Decoded all 100 episodes with TFDS. Saved actual schema and exterior start/mid/end contact sheets. Screening durations initially assume 15 Hz, to be verified against platform code/raw timestamps. No trajectory filtering or trimming."
)
