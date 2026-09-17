"""Regression checks for the refactor; these never step the physics simulation."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from droid2sim.evaluation.success import evaluate
from droid2sim.paths import ROOT, resolve_output
from droid2sim.trajectory import load_trajectory


class TrajectoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "trajectory.npz"
        self.times = np.array([0.0, 0.1, 0.2])
        self.joints = np.arange(21, dtype=float).reshape(3, 7) / 10
        self.gripper = np.array([[0.0], [0.8], [0.2]])
        np.savez(
            self.path, time=self.times, joint_position=self.joints, gripper_position=self.gripper
        )
        self.record_checksum()

    def record_checksum(self):
        checksum = hashlib.sha256(self.path.read_bytes()).hexdigest()
        (self.path.parent / "sha256.json").write_text(json.dumps({self.path.name: checksum}))

    def test_original_targets_are_read_only_and_exact_at_sample_times(self):
        trajectory = load_trajectory(self.path)
        for index, time in enumerate(self.times):
            joints, closure = trajectory.sample(time)
            np.testing.assert_array_equal(joints, self.joints[index])
            self.assertEqual(closure, self.gripper[index, 0])
        with self.assertRaises(ValueError):
            trajectory.joints[0, 0] = 99

    def test_interpolation_matches_original_replay_including_endpoints(self):
        trajectory = load_trajectory(self.path)
        for time in np.linspace(-0.1, 0.3, 101):
            joints, closure = trajectory.sample(time)
            expected = [np.interp(time, self.times, self.joints[:, j]) for j in range(7)]
            np.testing.assert_array_equal(joints, expected)
            self.assertEqual(closure, np.interp(time, self.times, self.gripper.ravel()))

    def test_tampered_recording_is_rejected(self):
        with self.path.open("ab") as stream:
            stream.write(b"tampered")
        with self.assertRaisesRegex(ValueError, "SHA256"):
            load_trajectory(self.path)

    def test_unordered_timestamps_are_rejected_even_with_valid_checksum(self):
        np.savez(
            self.path, time=[0, 0.2, 0.1], joint_position=self.joints, gripper_position=self.gripper
        )
        self.record_checksum()
        with self.assertRaisesRegex(ValueError, "increasing"):
            load_trajectory(self.path)


class ArchivedResultTests(unittest.TestCase):
    def test_all_five_original_predicates_are_preserved(self):
        for iteration in range(1, 6):
            with self.subTest(iteration=iteration):
                folder = ROOT / f"artifacts/iteration{iteration}"
                state = json.loads((folder / "state.json").read_text())
                scene = json.loads((folder / "scene_parameters.json").read_text())
                expected = json.loads((folder / "success.json").read_text())
                self.assertEqual(evaluate(state, scene), expected)
                self.assertEqual(expected["success"], iteration == 2)

    def test_relative_outputs_do_not_depend_on_shell_directory(self):
        self.assertEqual(resolve_output("artifacts/final"), ROOT / "artifacts/final")
        self.assertEqual(resolve_output(Path("/tmp/example")), Path("/tmp/example"))


if __name__ == "__main__":
    unittest.main()
