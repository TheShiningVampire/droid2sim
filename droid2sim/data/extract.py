"""Extract only the selected RLDS episode, preserving every recorded sample."""

import argparse
import hashlib
import json
import os

import imageio.v2 as imageio
import numpy as np
from PIL import Image

from droid2sim.data.download import log
from droid2sim.paths import EPISODE, ROOT

IMAGE_KEYS = {
    "ext1": "exterior_image_1_left",
    "ext2": "exterior_image_2_left",
    "wrist": "wrist_image_left",
}


def extract():
    # TensorFlow is needed for data preparation only, not replay or evaluation.
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
    import tensorflow_datasets as tfds

    config = json.loads((ROOT / "episode.json").read_text())
    fps = config["control_hz"]
    EPISODE.mkdir(parents=True, exist_ok=True)
    builder = tfds.builder_from_directory(str(ROOT / "data/droid_100/1.0.0"))
    dataset = builder.as_dataset(split="train", shuffle_files=False)
    for index, episode in enumerate(tfds.as_numpy(dataset)):
        if index != config["index"]:
            continue
        original_path = episode["episode_metadata"]["file_path"].decode()
        if original_path != config["metadata"]["file_path"]:
            raise ValueError("Episode index does not match the saved original path")
        steps = list(episode["steps"])
        observations = [step["observation"] for step in steps]
        arrays = {
            key: np.stack([observation[key] for observation in observations])
            for key in ("joint_position", "gripper_position", "cartesian_position")
        }
        arrays["time"] = np.arange(len(steps)) / fps
        arrays["gripper_opening_m"] = 0.085 * (1 - arrays["gripper_position"])
        for key in steps[0].get("action_dict", {}):
            arrays["action_" + key] = np.stack([step["action_dict"][key] for step in steps])
        trajectory_path = EPISODE / "trajectory.npz"
        np.savez(trajectory_path, **arrays)
        for camera, key in IMAGE_KEYS.items():
            frames = np.stack([observation[key] for observation in observations])
            np.save(EPISODE / f"{camera}.npy", frames)
            imageio.mimwrite(EPISODE / f"real_{camera}.mp4", frames, fps=fps, macro_block_size=1)
            for label, frame in (("start", 0), ("mid", len(steps) // 2), ("end", len(steps) - 1)):
                Image.fromarray(frames[frame]).save(EPISODE / f"{camera}_{label}.png")
        (EPISODE / "instruction.txt").write_text(config["instruction"] + "\n")
        checksum = hashlib.sha256(trajectory_path.read_bytes()).hexdigest()
        (EPISODE / "sha256.json").write_text(json.dumps({trajectory_path.name: checksum}, indent=2))
        log(
            f"Extracted chosen RLDS episode: {len(steps)} unchanged samples at {fps} Hz; three camera videos/keyframes and trajectory checksum saved."
        )
        return trajectory_path
    raise ValueError("The selected episode was not found in the sample")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Replace an existing extraction")
    args = parser.parse_args(argv)
    if (EPISODE / "trajectory.npz").exists() and not args.force:
        from droid2sim.trajectory import load_trajectory

        trajectory = load_trajectory()
        print(
            f"Existing extraction verified: {len(trajectory.time)} samples. Use --force to replace it."
        )
    else:
        print(extract())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
