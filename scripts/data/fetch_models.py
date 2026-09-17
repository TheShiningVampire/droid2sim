from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
import json
from droid2sim.data.download import fetch, log

manifest = json.load(open("sources/menagerie_tree.json"))
sha = manifest["sha"]
log(
    "Menagerie pinned tree "
    + sha
    + ". Fetch only franka_emika_panda and robotiq_2f85 XML, mesh assets and licenses; exclude preview videos/images."
)
for x in manifest["tree"]:
    p = x["path"]
    if (
        x["type"] == "blob"
        and p.split("/")[0] in ["franka_emika_panda", "robotiq_2f85"]
        and (
            p.endswith((".xml", ".obj", ".stl", ".png"))
            or p.split("/")[-1] in ["LICENSE", "README.md"]
        )
    ):
        fetch(
            f"https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/{sha}/{p}",
            "vendor/mujoco_menagerie/" + p,
        )
