from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
import json
import collections
import pathlib

entries = json.load(open("downloads.json"))
groups = collections.defaultdict(int)
for x in entries:
    p = x["file"]
    group = "Other source documents/manifests"
    if p.startswith("data/droid_100/"):
        group = "DROID 100-episode RLDS sample"
    elif p.startswith("data/calibration/"):
        group = "Published DROID calibration/ID maps"
    elif p.startswith("vendor/"):
        group = "Menagerie Panda and Robotiq assets"
    elif p.startswith("data/raw/"):
        group = "Rejected mug raw data (archived under data/rejected_mug_raw)"
    groups[group] += x["bytes"]
print(json.dumps(dict(groups), indent=2))
pathlib.Path("artifacts/download_summary.json").write_text(json.dumps(dict(groups), indent=2))
