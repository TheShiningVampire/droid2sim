import json,pathlib,html
root=pathlib.Path(__file__).resolve().parent
states={i:json.load(open(root/f'artifacts/iteration{i}/state.json')) for i in range(1,6)}
results={i:json.load(open(root/f'artifacts/iteration{i}/success.json')) for i in range(1,6)}
summary=json.load(open(root/'artifacts/download_summary.json'));s=states[2]
notes={1:'Initial marker was too long for the bowl interior; up to 13.2 mm initial wall overlap. It rotated before grasping and stayed in the bowl.',2:'Shortened marker 140→120 mm, radius 7.5→8.4 mm, widened lower bowl 53→66 mm, shifted marker y by −11 mm and reversed cap. No initial overlap. Marker lifted and released onto table, but rotates during capture.',3:'Applied stiffer 6D marker contacts. Penetration decreased sharply; marker was pushed out of the pinch and stayed in bowl.',4:'Retained stiff contacts; moved bowl and marker (+14,−8,0) mm. Grasp still failed and bowl displacement increased; visually worse.',5:'Restored iteration-2 geometry and native pad response; stiffened marker–bowl pairs only; disabled hard shadows. Grasp still failed. Five-iteration limit reached.'}
rows='\n'.join(f'| {i} | {"PASS" if results[i]["success"] else "FAIL"} | {1000*abs(states[i]["min_pen_contact_distance_m"]):.3f} | {states[i]["frames_with_pen_gripper_contact"]} | {notes[i]} | [Compare](artifacts/iteration{i}/side_by_side.mp4) · [Sim](artifacts/iteration{i}/sim_ext1.mp4) |' for i in range(1,6))
sources='\n'.join(f'| {k} | {v:,} |' for k,v in summary.items())
report=f'''# droid2sim report

## Result

**The repository runs end to end. The retained replay (iteration 2) passes the programmatic task check and visibly lifts the marker out of its bowl and places it on the table. It is an approximate, contact-sensitive reproduction—not a validated reconstruction of real physics.** Four other scene iterations failed. Stiffer, lower-penetration contacts failed to reproduce the grasp; this is a material limitation, not a hidden failure.

- [Final real | sim video](side_by_side.mp4) · [Final sim video](sim_ext1.mp4)
- [All five videos, including failures](VIDEOS.html)
- [Running log](LOG.md) · [Run instructions](README.md) · [Selection evidence](SELECTION.md)

## Episode and selection

Instruction: **“Take the pen out of the bowl and place it on the table.”**

Sample index **6**, deterministic TFDS order, `droid_100/1.0.0`, original path:

`/nfs/kun2/datasets/r2d2/r2d2-data-full/IRIS/success/2023-05-04/Thu_May__4_13:41:33_2023/trajectory.h5`

181 samples, 15 Hz nominal control rate, 12.067-second video (last sample at 12.0 s). Success path and final reward 1, independently supported by visual review of the real outcome. The black/teal target is an opaque plastic marker, visible inside the bowl in both initial exterior views. The circular tabletop is otherwise clear. A bowl is reconstructed as a separate support body; the marker is the sole intentionally manipulated object. Small plastic highlights exist; exact material is not provable at this resolution.

All 100 episodes were decoded; 27 met success/language/duration screening before visual rejection. Top-five sheets: [6, selected](artifacts/top5/006.jpg), [74](artifacts/top5/074.jpg), [4](artifacts/top5/004.jpg), [60](artifacts/top5/060.jpg), [20](artifacts/top5/020.jpg). Reasons are in SELECTION.md. No episode was trimmed to meet the duration criterion.

Candidate 74 was provisionally selected but rejected when HD wrist video revealed glossy ceramic. **A disclosed scope deviation:** its raw data was downloaded before rejection, so raw downloads were not limited exclusively to the final selected episode. Those bytes remain counted and archived; no additional candidate raw recordings were downloaded.

## Sources and download sizes

Verified sample path and schema in the [official DROID policy repository](https://github.com/droid-dataset/droid_policy_learning) and [official dataset documentation](https://github.com/droid-dataset/droid/blob/main/docs/the-droid-dataset.md). Source snapshots, actual TFDS schema and GCS manifests are under `sources/`. Every transfer URL and payload size is recorded in [downloads.json](downloads.json) and LOG.md.

| Download group | Exact payload bytes |
|---|---:|
{sources}
| **Total audited payload** | **2,607,040,732** |

Exact origins:

- Sample: `gs://gresearch/robotics/droid_100/1.0.0/`; all 33 nonempty files verified against GCS sizes and MD5 hashes.
- Calibration maps: [KarlP/droid](https://huggingface.co/KarlP/droid): `episode_id_to_path.json`, `cam2base_extrinsics.json`, `cam2base_extrinsic_superset.json`, `cam2cam_extrinsics.json`, `intrinsics.json`. Individual exact sizes are in downloads.json.
- Robot assets: [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie), pinned tree `8161bba264d7fa7c99ca301e91e7fb44737676ad`, only `franka_emika_panda` and `robotiq_2f85` assets/XML/licenses.
- Rejected mug raw: `gs://gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02:08:20_2023/`; stereo MP4s, metadata and HDF5s, archived in `data/rejected_mug_raw/`.

Python wheels downloaded through uv add approximately 0.55 GB (install.log records displayed sizes); their original transfer sizes were not individually instrumented. Reserving **1,000,000,000 bytes** for dependencies, browser documentation and metadata overhead gives a conservative total **3,607,040,732 bytes**, comfortably below the 10 GB hard limit. No full DROID/raw/Menagerie release was downloaded. Machine initially had 331 GiB free and an RTX 3060 GPU with 6 GiB VRAM; rendering used EGL.

## Raw data and camera limitations

Final episode raw listings returned no files at the exact official `droid_raw/1.0.1/IRIS/success/2023-05-04/Thu_May__4_13:41:33_2023/` prefix. Also checked `1.0.0` and unversioned equivalents. Saved empty responses: `sources/raw_pen_listing*.json`. The episode is absent from the published ID/path map, so no improved per-episode extrinsics could be matched. **Used the explicitly permitted RLDS fallback.** No credentials were needed.

Consequently, **no HD/stereo video, raw metadata JSON, measured intrinsics/extrinsics, raw timestamps, or stereo depth is available for the final episode**. Stereo depth was computed by SGBM for the rejected mug only, then archived; it is not used or presented as depth for the marker episode. Rejected-mug MP4 headers incorrectly imply 60 fps relative to the recorded ~70 ms steps; those exploratory outputs are not the final comparison.

Both simulation cameras use estimated pinhole intrinsics/extrinsics in `cameras.json`: eight manually marked gripper pinch locations per view, Menagerie FK, a focal-length prior, and joint refinement against circular table silhouettes. Final focal lengths are 143.67 px (ext1) and 139.96 px (ext2) at 320×180. Centered principal points and zero distortion are assumed. OpenCV camera-to-world rotations are converted to MuJoCo by flipping camera Y/Z axes. Robot base is exactly the world frame; units are meters/radians/kilograms/seconds.

Final mean manual-landmark residuals are **5.39 px / 7.21 px** for ext1/ext2, maxima **10.73 / 16.24 px**. These residuals measure agreement with approximate labels, not ground-truth camera accuracy. The circular table fits more closely than the moving robot. Overlay errors are visible, especially in exterior 2.

## Robot and object reconstruction

The robot uses official Menagerie Panda dynamics, meshes and position actuators; the Panda hand is replaced by the official Robotiq 2F-85 with its articulated linkage, tendons and equality constraints. A fixed attachment uses the Panda flange offset 0.107 m, −45° hand rotation and native Robotiq mount offset. Exact hardware adapter geometry is unavailable. FK flange positions match the recorded Cartesian positions to floating-point precision. Wrist camera, adapter detail and cables are omitted. Robot gravity compensation approximates DROID controller feedforward; no object welds or scripted object motion are used.

All scene objects use generated primitives/convex geometry; Blender and learned reconstruction were not used. Full values and provenance are in `scene_parameters.json`.

| Body | Geometry and initial pose in base/world frame | Mass; sliding/torsional/rolling friction | Evidence |
|---|---|---|---|
| Table | Circular cylinder, radius 0.25743 m, thickness 0.030 m; center XY (0.65726, −0.07507), top Z −0.04011; rotation identity | Fixed/infinite support; 0.6 / 0.005 / 0.0001 | Radius/XY/Z jointly fitted from silhouettes and robot landmarks; horizontal, thickness and friction assumed. Cylinder body origin is 15 mm below top. Simplified central leg. |
| Bowl | Open tapered bowl: 32 convex wall wedges plus circular base. Lower radius 0.066 m, upper 0.083 m, height 0.055 m, wall 0.004 m, base 0.008 m. Bottom origin (0.647, −0.253, −0.04011), quaternion (1,0,0,0) | 0.18 kg; 0.5 / 0.005 / 0.0001 | Diameter/position estimated from views; interior revised to eliminate initial overlap. Thickness, mass, friction and exact taper assumed. Free dynamic body. |
| Marker | Two capsules and visual label, length 0.120 m, barrel radius 0.0084 m, cap radius 0.008736 m, cap length 0.040 m. Initial center (0.648, −0.267, −0.02328); XYZ Euler (0,0,3.08159) | 0.018 kg; 0.8 / 0.01 / 0.0001 | Dimensions estimated from images and nominal gripper gap; pose refined within calibration uncertainty. Mass/friction assumed. Free dynamic body; cap reversed to match real teal end. |

Friction mixing/priority matters: native Robotiq pad parameters override the marker's lower-priority contact settings in the retained replay. Background is a plain floor and simplified table leg, not a reconstruction of the room. Floor top Z −0.85 m is assumed and does not participate in task contacts.

## Replay and verification

`replay.py` loads `scene.xml`, uses recorded joint observations as position targets and maps recorded normalized gripper closure to Menagerie’s 0–255 actuator input. Nominal opening is `0.085*(1-closure)` m. Linear interpolation supplies 1 ms physics steps between the original 15 Hz samples. No trimming, smoothing, time warping, offsets, optimized trajectory, altered sample or scripted object force was used. Every run asserts trajectory SHA256:

`{s['trajectory_sha256']}`

Robot control parameters are identical across all five iterations. Actual simulated joints have RMS tracking error **0.02032 rad**, maximum **0.10960 rad**; replay is dynamic position control, not forced kinematic copying. This lag contributes to visual differences.

`success.py` final result: **true**. Plain predicate: the marker must have been lifted above the bowl rim with gripper contact, and end entirely outside the bowl, inside the circular tabletop boundary, nearly horizontal at tabletop height, moving slower than 4 cm/s. All component checks passed. The check does not establish exact material/contact realism.

Final marker position: **(0.51948, −0.09492, −0.03156) m**; quaternion WXYZ **(0.52716, 0.11644, 0.17809, 0.82269)**. Final bowl position: **(0.64730, −0.25368, −0.04012) m**. Full final poses are printed by replay.py and saved in `artifacts/final/state.json`.

## Five scene iterations, including every failure

| Iteration | Predicate | Max marker contact penetration (mm) | Frames with pad contact | Before/after observations and changes | Videos |
|---|---|---:|---:|---|---|
{rows}

Retained **iteration 2**, copied from its existing run to `artifacts/final/`; no sixth physics run. All failed videos remain available in [VIDEOS.html](VIDEOS.html), with both the side-by-side comparison and standalone sim. All five state histories, scene/camera snapshots, overlays and predicates are preserved. `validate.py` verifies identical recorded targets in every run, five-iteration limit, finite states, video-array dimensions, sample MD5s and budget.

## Visual and contact assessment

I inspected every iteration's real/sim/overlay sequence, then denser final contact sequences every three frames from 96–162 in both cameras (`contact_review_ext1.jpg`, `contact_review_ext2.jpg`). The retained replay visibly reproduces **remove marker → lift → transport → release onto table**. It does **not** reproduce the exact marker orientation or precise contact behavior.

- **Slip/rotation:** the marker rotates roughly 50° during simulated grasp closure, more than the real view suggests. Once lifted, sampled marker-COM drift relative to the rigid gripper frame over frames 120–150 is only **0.443 mm**; this is a proxy, not direct pad-surface slip measurement. Stable transport is visible. Final orientation differs noticeably, particularly exterior 2.
- **Penetration:** retained run reaches **4.227 mm** signed marker-contact overlap. The diagnostic is over all marker contacts, not proven to be finger-only. Initial scene has no significant interpenetration. The later low-penetration variants (0.371–0.721 mm) fail. Therefore the successful grasp is **not physically validated and may rely on excessive compliance**.
- **Instability:** all five runs have finite states and zero MuJoCo warning counts. Retained replay has no explosive launch or sustained visible chatter, but the marker rolls after release; final angular speed is about **0.272 rad/s**, with linear speed **0.00234 m/s**. “Settled” in success.py tests linear speed only.
- **Camera alignment:** table silhouette is approximately aligned, but robot/hand and bowl positions show several-pixel errors; external-2 alignment is weaker. Missing wrist camera/cables change apparent robot shape. Intrinsics/extrinsics are estimated, not recovered calibration.
- **Scale/pose:** table/bowl/marker dimensions and poses remain uncertain. Marker length changed 14→12 cm during fitting; initial pose changed by 11 mm. The real final marker orientation differs from the sim. No measured 6D object ground truth exists here.
- **Mesh/appearance:** faceted bowl, capsule marker, flat label and simplified table omit fine geometry, print, textures and material highlights. Lighting and hard shadows differ; room clutter/background is intentionally omitted.

## Files produced and how to run

Core files: `replay.py`, `success.py`, `compare.py`, `build_scene.py`, `scene.xml`, `scene_parameters.json`, `robot.xml`, `cameras.json`, `episode.json`, `README.md`, `LOG.md`, `REPORT.md`, `VIDEOS.html`, `requirements.lock.txt`, `downloads.json`, `validate.py`.

Extracted data: `data/episode/real_ext1.mp4`, `real_ext2.mp4`, `real_wrist.mp4`, three-camera start/mid/end PNGs, `trajectory.npz`, human-readable `trajectory.csv`, `sha256.json`, `timing.json`, `instruction.txt`.

Final outputs: root `sim_ext1.mp4` and `side_by_side.mp4` links; `artifacts/final/sim_ext2.mp4`; exterior-1 and exterior-2 overlays at start/mid/end; dense contact sheets; `state.json`, `history.json`, `success.json`, `contact_metrics.json`. Screening sheets: `artifacts/top5/` and all 100 `artifacts/candidates/`. Failed outputs: `artifacts/iteration1`, `iteration3`, `iteration4`, `iteration5`.

```sh
cd /home/vinit/my_things/codes/droid2sim
MUJOCO_GL=egl .venv/bin/python replay.py
.venv/bin/python compare.py
.venv/bin/python success.py
```

## Assumptions and what could not be done

Assumptions not determined by final-episode data: 15 Hz timing without raw timestamps; 85 mm maximum opening and linear normalized-width conversion; robot attachment rotation/offset and omitted hardware; native Menagerie controller gains/limits, gravity compensation and 1 ms timestep; centered square-pixel pinhole cameras with no distortion and focal prior; manually estimated pinch landmarks; horizontal circular table and its dimensions; bowl circular symmetry/taper/thickness; marker capsule geometry, cap dimensions and horizontal initial pose; all object masses, inertia inferred from geometric mass distribution, friction, contact compliance/restitution; uniform materials, lighting, background floor/leg; precise sample-index video synchronization; numerical thresholds for the language predicate. Scene-only fitting used task outcome as feedback and is not independent validation of these assumptions.

Could not obtain the selected episode's raw data, HD videos, measured camera calibration, stereo depth, exact control timestamps, exact object models, physical parameters or a robust low-penetration grasp within five iterations. Also could not keep raw downloads exclusive to the final episode because the first selected object was rejected only after HD inspection. Those limitations remain explicit. The task-level visual outcome is reproduced in one retained run; exact real-world physical behavior is not.
'''
(root/'REPORT.md').write_text(report)
items=[]
for i in [1,3,4,5,2]:
 status='PASS — retained, contact-sensitive' if i==2 else 'FAILED'
 items.append(f'<section><h2>Iteration {i}: {status}</h2><p>{html.escape(notes[i])}</p><video controls preload="metadata" src="artifacts/iteration{i}/side_by_side.mp4"></video><p><a href="artifacts/iteration{i}/side_by_side.mp4">Real | sim comparison</a> · <a href="artifacts/iteration{i}/sim_ext1.mp4">Standalone simulation</a> · <a href="artifacts/iteration{i}/success.json">Task check</a></p></section>')
(root/'VIDEOS.html').write_text('''<!doctype html><meta charset="utf-8"><title>droid2sim — all replay attempts</title><style>body{font:17px system-ui;max-width:1100px;margin:40px auto;padding:0 20px;background:#101318;color:#edf0f4}a{color:#8dcbff}section{border:1px solid #46505c;padding:20px;margin:24px 0;border-radius:8px}video{width:100%;background:black}h1{font-size:30px}h2{font-size:23px}</style><h1>DROID to MuJoCo: every attempt</h1><p>Failures are shown first and preserved. Each video is real exterior camera 1 on the left, simulation on the right. Only iteration 2 completes the task, with imperfect contact physics. <a href="REPORT.md">Full report</a></p>'''+''.join(items))
print('Wrote REPORT.md and VIDEOS.html')
