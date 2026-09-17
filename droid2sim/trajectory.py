"""Read and sample the recorded trajectory without changing its observations."""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import numpy as np

from .paths import EPISODE


@dataclass(frozen=True)
class Trajectory:
    time: np.ndarray
    joints: np.ndarray
    gripper: np.ndarray
    sha256: str

    def sample(self, time: float) -> tuple[np.ndarray, float]:
        """Interpolate recorded targets for a physics step; never optimize them."""
        joints = np.array([np.interp(time, self.time, self.joints[:, joint]) for joint in range(7)])
        closure = float(np.interp(time, self.time, self.gripper))
        return joints, closure


def load_trajectory(path: Path = EPISODE / "trajectory.npz") -> Trajectory:
    """Verify the extraction checksum and return read-only observation arrays."""
    path = Path(path)
    expected = json.loads((path.parent / "sha256.json").read_text())[path.name]
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError("Recorded trajectory changed: SHA256 mismatch")

    with np.load(path) as recording:
        times = recording["time"]
        joints = recording["joint_position"]
        gripper = recording["gripper_position"].ravel()
    if times.ndim != 1 or len(times) < 2 or np.any(np.diff(times) <= 0):
        raise ValueError("Recording timestamps must be strictly increasing")
    if joints.shape != (len(times), 7) or gripper.shape != times.shape:
        raise ValueError("Recording must contain seven joints and one gripper per step")
    for array in (times, joints, gripper):
        if not np.isfinite(array).all():
            raise ValueError("Recording contains non-finite values")
        array.setflags(write=False)
    return Trajectory(times, joints, gripper, actual)
