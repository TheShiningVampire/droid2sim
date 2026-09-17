# System identification status

**No physical SysID of mass, inertia, friction or contact stiffness has been completed.** The original five trials were manual scene fitting. One passed, and reducing contact penetration made the grasp fail. That is evidence of sensitivity, not proof that the successful parameters are physically correct.

A new **offline kinematic command-response surrogate** has now been fitted using the selected episode. It does not change the final replay or consume another scene iteration.

## Inputs and model

`data/episode/trajectory.npz` provides observed `joint_position` and logged `action_joint_position`. For each joint, the diagnostic fits:

`q[k+1] = q[k] + b * (command[k-lag] - q[k])`

The first 120 samples are training data. The last 60 transitions are held out. Lag is chosen from 0, 1 or 2 steps using training error only; b is constrained to [0,1]. Predictions are one-step predictions conditioned on the observed current state, not free-running rollouts.

| Joint | Selected lag (steps) | Response fraction b | Held-out RMSE (rad) | Hold-current-state baseline RMSE (rad) |
|---|---:|---:|---:|---:|
| 1 | 0 | 0.1854 | 0.00556 | 0.01616 |
| 2 | 1 | 0.2848 | 0.00607 | 0.02225 |
| 3 | 0 | 0.2272 | 0.00460 | 0.01674 |
| 4 | 0 | 0.1529 | 0.00655 | 0.02169 |
| 5 | 0 | 0.1857 | 0.01137 | 0.02402 |
| 6 | 0 | 0.2504 | 0.00486 | 0.01064 |
| 7 | 0 | 0.1365 | 0.01218 | 0.02210 |

This improves one-step RMSE over the baseline by about 45–73%. It only suggests that logged commands help predict the next recorded joint state. Internal controller interpolation, true timestamps and command timing are unavailable. The coefficients mix control response, dynamics and latency. They are **not MuJoCo kp values**. The replay targets recorded observations rather than these logged commands, so substituting the fitted coefficients would change its interpretation. No controller parameter has been changed.

Reproduce the offline analysis with `.venv/bin/python -m scripts.analysis.measure_replay`. Complete coefficients and limitations: `artifacts/measurements/joint_response_surrogate.json`.

## Visual measurements added

The marker's teal cap is tracked by color segmentation and temporal association in exterior camera 1, separately in real and simulated frames. Missing detections remain missing. This tracks an appearance centroid, not the marker's center of mass. Sampled detections were visually checked in `artifacts/measurements/tracking_review.jpg`.

- 168 of 181 frames had detections in both videos.
- Mean cap error: 7.82 px; median 5.80 px; maximum 26.30 px.
- Mean before grasp: 5.73 px; grasp: 8.85 px; transport: 13.43 px; release/final: 9.00 px.
- Final cap error: 2.76 px. This does **not** imply correct final marker orientation.
- Initial median real-minus-sim cap offset: (−4.51, +3.46) px.
- Transport error after subtracting that static offset: 10.63 px. A constant camera/image offset cannot explain the transport mismatch.

These are automatic 2D estimates affected by occlusion, perspective and segmentation. They are not calibrated 3D ground truth. No image warp was applied to conceal errors.

## What a defensible physical SysID stage would require

1. Recover/refine camera calibration with independent robot landmarks and hold-out frames. Estimate marker/bowl trajectories with uncertainty, not merely a binary task outcome.
2. Fit geometry/initial pose before dynamics so geometry error is not absorbed into artificial friction or compliance.
3. Fit a small, bounded subset of effective contact parameters against observed lift, slip, rotation and release motion, with penetration penalties. Preserve the recorded trajectory.
4. Evaluate held-out parts of the motion and parameter perturbations. Mass/friction/compliance may not be separately identifiable from one low-resolution episode without force measurements.

Mass is not directly measurable from these images. Real contact forces and raw gripper widths/timestamps are absent. Friction and grip compliance trade off against geometry, opening calibration and normal force. Reporting unique identified physical values would overstate what this dataset supports.

The original **five scene-iteration limit has been reached**. No sixth physics run has been made. Further contact-parameter optimization would require a larger iteration allowance; the current additional work is offline measurement and explanation.
