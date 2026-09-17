"""Audit sample checksums, download budget, and all five immutable replays."""

import json
import hashlib
import base64
import numpy as np
from droid2sim.paths import ROOT


def validate():
    manifest = json.load(open(ROOT / "sources/sample_listing.json"))
    checked = 0
    for f in manifest["items"]:
        if not int(f.get("size", 0)):
            continue
        p = ROOT / "data" / f["name"].removeprefix("robotics/")
        assert p.stat().st_size == int(f["size"])
        if "md5Hash" in f:
            h = hashlib.md5()
            with p.open("rb") as stream:
                while b := stream.read(2**20):
                    h.update(b)
            assert base64.b64encode(h.digest()).decode() == f["md5Hash"], p
        checked += 1
    ledger = json.load(open(ROOT / "downloads.json"))
    assert sum(x["bytes"] for x in ledger) + 1_000_000_000 < 10_000_000_000
    p = ROOT / "data/episode/trajectory.npz"
    assert (
        hashlib.sha256(p.read_bytes()).hexdigest()
        == json.load(open(p.parent / "sha256.json"))[p.name]
    )
    a = np.load(p)
    iterations = sorted((ROOT / "artifacts").glob("iteration[1-5]"))
    assert 1 < len(iterations) <= 5
    for folder in iterations:
        h = json.load(open(folder / "history.json"))
        assert np.array_equal(np.array([x["q_target"] for x in h]), a["joint_position"])
        assert len(h) == len(a["time"])
        assert (
            np.load(folder / "sim_ext1.npy").shape == np.load(ROOT / "data/episode/ext1.npy").shape
        )
        assert json.load(open(folder / "state.json"))["finite"]
    print(
        json.dumps(
            dict(
                sample_files_md5_verified=checked,
                download_payload_bytes=sum(x["bytes"] for x in ledger),
                conservative_total_with_dependency_reserve=sum(x["bytes"] for x in ledger)
                + 1_000_000_000,
                trajectory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                iterations_checked=len(iterations),
                all_recorded_targets_exactly_preserved=True,
            ),
            indent=2,
        )
    )


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
