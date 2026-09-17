"""Check whether the marker was lifted out of the bowl and placed on the table."""

import argparse
import json

import numpy as np
from scipy.spatial.transform import Rotation

from droid2sim.paths import resolve_output

PREDICATE = (
    "The marker has been lifted above the bowl rim with gripper contact and ends "
    "entirely outside the bowl, within the circular tabletop, nearly horizontal "
    "at tabletop height, with speed below 4 cm/s."
)


def evaluate(state, scene):
    """Evaluate the original predicate without loading a robot or running physics."""
    position = np.array(state["final_poses"]["pen"]["position"])
    bowl_position = np.array(state["final_poses"]["bowl"]["position"])
    table, pen, bowl = (scene[name] for name in ("table", "pen", "bowl"))
    quaternion = state["final_poses"]["pen"]["quaternion_wxyz"]
    axis = Rotation.from_quat(quaternion[1:] + quaternion[:1]).as_matrix()[:, 0]
    endpoints = np.array(
        [
            position - axis * pen["length"] / 2,
            position + axis * pen["length"] / 2,
        ]
    )
    # Keep the experiment's original thresholds. This is task-level success;
    # it does not certify low penetration, correct orientation, or true physics.
    checks = {
        "outside_bowl": bool(
            np.linalg.norm(position[:2] - bowl_position[:2]) - pen["length"] / 2
            > bowl["top_radius"] + 0.005
        ),
        "on_table": bool(
            np.max(np.linalg.norm(endpoints[:, :2] - table["center_xy"], axis=1)) < table["radius"]
        ),
        "resting_height": bool(abs(position[2] - (table["top_z"] + pen["radius"])) < 0.012),
        "nearly_horizontal": bool(abs(axis[2]) < 0.2),
        "settled": bool(np.linalg.norm(state["pen_final_velocity"][:3]) < 0.04),
        "lifted_from_bowl": bool(state["pen_max_z"] > bowl_position[2] + bowl["height"] + 0.025),
        "gripper_contact": bool(state["frames_with_pen_gripper_contact"] > 0),
        "finite": state["finite"],
    }
    return {
        "success": all(checks.values()),
        "checks": checks,
        "predicate": PREDICATE,
        "final_pen_position": position.tolist(),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="artifacts/final")
    args = parser.parse_args(argv)
    output = resolve_output(args.out)
    state = json.loads((output / "state.json").read_text())
    scene = json.loads((output / "scene_parameters.json").read_text())
    result = evaluate(state, scene)
    (output / "success.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
