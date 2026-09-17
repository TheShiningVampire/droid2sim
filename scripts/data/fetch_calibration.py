from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
from droid2sim.data.download import fetch

for name in [
    "episode_id_to_path.json",
    "cam2base_extrinsics.json",
    "cam2base_extrinsic_superset.json",
    "cam2cam_extrinsics.json",
    "intrinsics.json",
]:
    fetch("https://huggingface.co/KarlP/droid/resolve/main/" + name, "data/calibration/" + name)
