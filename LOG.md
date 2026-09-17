# droid2sim running log

## 2026-09-17 Setup
- User goal: one real episode, unmodified joint/gripper trajectory, <=5 scene iterations, total downloads strictly below 10,000,000,000 bytes.
- Initial shell command failed before execution: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Subsequent commands require escalation because sandbox startup is broken.
- Ran `pwd; df -h . /tmp; nvidia-smi; rg --files -g AGENTS.md ...`: 331 GiB free; NVIDIA RTX 3060 laptop GPU, 6144 MiB VRAM, driver 595.84. No AGENTS.md found in workspace or ancestors.
- Ran `mkdir -p droid2sim && cd droid2sim && git init && command -v uv; ls /usr/bin/python*`. Created fresh Git repository. Python 3.12 is available; choose it over default 3.14 for TensorFlow compatibility.
- Verified sample and raw prefixes against official https://github.com/droid-dataset/droid_policy_learning and schema at https://github.com/droid-dataset/droid/blob/main/droid/postprocessing/schema.py . Sample: gs://gresearch/robotics/droid_100; raw: gs://gresearch/robotics/droid_raw . Never request a full recursive raw/full-dataset download.
- Official homepage https://droid-dataset.github.io/ announces improved calibrations at https://huggingface.co/KarlP/droid . Check selected episode coverage before estimating cameras.
- Browser documentation searches preceded local setup; these return text snippets, not dataset payloads. All subsequent download commands and downloaded file bytes will be recorded locally.

- Standard venv failed (ensurepip absent); uv retry required --allow-existing for incomplete venv.
- Download command: uv pip install --python .venv/bin/python mujoco tensorflow-cpu tensorflow-datasets numpy pillow imageio imageio-ffmpeg opencv-python-headless scipy h5py requests. CPU TensorFlow chosen to limit downloads.

- 2026-09-17T18:01:04.320655+00:00 Download: `python download.py https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_100%2F&maxResults=1000 sources/sample_listing.json`

- 2026-09-17T18:01:04.579078+00:00 Download result: {'url': 'https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_100%2F&maxResults=1000', 'file': 'sources/sample_listing.json', 'bytes': 36611, 'complete': True}; cumulative payload 36,611 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:04.579488+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/dataset_info.json data/droid_100/1.0.0/dataset_info.json`

- 2026-09-17T18:01:04.852908+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/dataset_info.json', 'file': 'data/droid_100/1.0.0/dataset_info.json', 'bytes': 760, 'complete': True}; cumulative payload 37,371 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:04.853139+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/features.json data/droid_100/1.0.0/features.json`

- 2026-09-17T18:01:05.176391+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/features.json', 'file': 'data/droid_100/1.0.0/features.json', 'bytes': 18665, 'complete': True}; cumulative payload 56,036 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:05.176608+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00000-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00000-of-00031`

- 2026-09-17T18:01:12.555588+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00000-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00000-of-00031', 'bytes': 27488816, 'complete': True}; cumulative payload 27,544,852 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:12.555807+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00001-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00001-of-00031`

- 2026-09-17T18:01:21.501816+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00001-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00001-of-00031', 'bytes': 53215423, 'complete': True}; cumulative payload 80,760,275 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:21.502008+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00002-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00002-of-00031`

- 2026-09-17T18:01:23.724008+00:00 Download: `python download.py https://raw.githubusercontent.com/droid-dataset/droid/main/docs/the-droid-dataset.md sources/droid_dataset.md`

- 2026-09-17T18:01:24.006602+00:00 Download result: {'url': 'https://raw.githubusercontent.com/droid-dataset/droid/main/docs/the-droid-dataset.md', 'file': 'sources/droid_dataset.md', 'bytes': 6685, 'complete': True}; cumulative payload 80,766,960 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:24.057680+00:00 Download: `python download.py https://huggingface.co/KarlP/droid/raw/main/README.md sources/calibration_README.md`

- 2026-09-17T18:01:24.333621+00:00 Download result: {'url': 'https://huggingface.co/KarlP/droid/raw/main/README.md', 'file': 'sources/calibration_README.md', 'bytes': 7290, 'complete': True}; cumulative payload 80,774,250 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:37.644041+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00002-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00002-of-00031', 'bytes': 104176382, 'complete': True}; cumulative payload 184,936,657 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:37.654127+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00003-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00003-of-00031`

- 2026-09-17T18:01:42.081051+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00003-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00003-of-00031', 'bytes': 49407960, 'complete': True}; cumulative payload 234,344,617 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:42.081257+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00004-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00004-of-00031`

- 2026-09-17T18:01:46.986656+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00004-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00004-of-00031', 'bytes': 57059559, 'complete': True}; cumulative payload 291,404,176 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:46.986848+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00005-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00005-of-00031`

- 2026-09-17T18:01:49.661304+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00005-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00005-of-00031', 'bytes': 28932473, 'complete': True}; cumulative payload 320,336,649 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:49.661499+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00006-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00006-of-00031`

- 2026-09-17T18:01:51.330258+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00006-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00006-of-00031', 'bytes': 12745632, 'complete': True}; cumulative payload 333,082,281 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:51.330471+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00007-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00007-of-00031`

- 2026-09-17T18:01:54.958055+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00007-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00007-of-00031', 'bytes': 41133699, 'complete': True}; cumulative payload 374,215,980 bytes (+ reserved dependency allowance).

- 2026-09-17T18:01:54.958319+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00008-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00008-of-00031`

- 2026-09-17T18:02:07.203922+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00008-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00008-of-00031', 'bytes': 131132714, 'complete': True}; cumulative payload 505,348,694 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:07.204122+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00009-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00009-of-00031`

- 2026-09-17T18:02:08.531725+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00009-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00009-of-00031', 'bytes': 9541347, 'complete': True}; cumulative payload 514,890,041 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:08.532025+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00010-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00010-of-00031`

- 2026-09-17T18:02:12.124319+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00010-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00010-of-00031', 'bytes': 30130184, 'complete': True}; cumulative payload 545,020,225 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:12.124554+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00011-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00011-of-00031`

- 2026-09-17T18:02:19.620013+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00011-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00011-of-00031', 'bytes': 64826210, 'complete': True}; cumulative payload 609,846,435 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:19.620204+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00012-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00012-of-00031`

- 2026-09-17T18:02:25.658799+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00012-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00012-of-00031', 'bytes': 64716351, 'complete': True}; cumulative payload 674,562,786 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:25.659022+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00013-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00013-of-00031`

- 2026-09-17T18:02:27.797971+00:00 Download: `python download.py https://api.github.com/repos/google-deepmind/mujoco_menagerie/git/trees/main?recursive=1 sources/menagerie_tree.json`

- 2026-09-17T18:02:34.131010+00:00 Download result: {'url': 'https://api.github.com/repos/google-deepmind/mujoco_menagerie/git/trees/main?recursive=1', 'file': 'sources/menagerie_tree.json', 'bytes': 891921, 'complete': True}; cumulative payload 675,454,707 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:44.426913+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00013-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00013-of-00031', 'bytes': 184352180, 'complete': True}; cumulative payload 858,914,966 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:44.427185+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00014-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00014-of-00031`

- 2026-09-17T18:02:47.362522+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00014-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00014-of-00031', 'bytes': 31864169, 'complete': True}; cumulative payload 890,779,135 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:47.362747+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00015-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00015-of-00031`

- 2026-09-17T18:02:57.471423+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00015-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00015-of-00031', 'bytes': 99620534, 'complete': True}; cumulative payload 990,399,669 bytes (+ reserved dependency allowance).

- 2026-09-17T18:02:57.471639+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00016-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00016-of-00031`

- 2026-09-17T18:03:09.790006+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00016-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00016-of-00031', 'bytes': 134703547, 'complete': True}; cumulative payload 1,125,103,216 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:09.790200+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00017-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00017-of-00031`

- 2026-09-17T18:03:12.540044+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00017-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00017-of-00031', 'bytes': 27059787, 'complete': True}; cumulative payload 1,152,163,003 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:12.540318+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00018-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00018-of-00031`

- 2026-09-17T18:03:21.538969+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00018-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00018-of-00031', 'bytes': 97615525, 'complete': True}; cumulative payload 1,249,778,528 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:21.539261+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00019-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00019-of-00031`

- 2026-09-17T18:03:23.154140+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00019-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00019-of-00031', 'bytes': 14490316, 'complete': True}; cumulative payload 1,264,268,844 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:23.154353+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00020-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00020-of-00031`

- 2026-09-17T18:03:29.838511+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00020-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00020-of-00031', 'bytes': 69822437, 'complete': True}; cumulative payload 1,334,091,281 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:29.838832+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00021-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00021-of-00031`

- 2026-09-17T18:03:34.876155+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00021-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00021-of-00031', 'bytes': 46506562, 'complete': True}; cumulative payload 1,380,597,843 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:34.876534+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00022-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00022-of-00031`

- 2026-09-17T18:03:44.253900+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00022-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00022-of-00031', 'bytes': 100973263, 'complete': True}; cumulative payload 1,481,571,106 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:44.254156+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00023-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00023-of-00031`

- Verified platform control rate 15 Hz in official `droid/robot_env.py` and `droid/robot_ik/robot_ik_solver.py` (https://github.com/droid-dataset/droid). Initial sample duration screening uses this documented rate, with raw timestamps to refine it.
- Installed TensorFlow CPU 2.21.0 and MuJoCo 3.13.0; import smoke test passed. Full dependency versions in install.log. Downloaded wheels listed there total approximately 523 MiB plus small dependencies; reserve 1 GB in the dataset budget for these and documentation overhead.
- Documentation fetch succeeded; first Menagerie manifest command hit zsh glob expansion on an unquoted question mark. Retried with URL quoted; manifest fetched successfully.
- Implementation decision: fetch only required Menagerie directories/assets at the manifest tree SHA, not the entire Menagerie repository.

- 2026-09-17T18:03:52.073504+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00023-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00023-of-00031', 'bytes': 80456132, 'complete': True}; cumulative payload 1,562,027,238 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:52.073847+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00024-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00024-of-00031`

- 2026-09-17T18:03:55.065631+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00024-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00024-of-00031', 'bytes': 25002446, 'complete': True}; cumulative payload 1,587,029,684 bytes (+ reserved dependency allowance).

- 2026-09-17T18:03:55.065838+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00025-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00025-of-00031`

- 2026-09-17T18:04:03.780613+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00025-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00025-of-00031', 'bytes': 91800923, 'complete': True}; cumulative payload 1,678,830,607 bytes (+ reserved dependency allowance).

- 2026-09-17T18:04:03.780857+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00026-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00026-of-00031`

- 2026-09-17T18:04:19.050725+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00026-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00026-of-00031', 'bytes': 173915084, 'complete': True}; cumulative payload 1,852,745,691 bytes (+ reserved dependency allowance).

- 2026-09-17T18:04:19.050931+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00027-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00027-of-00031`

- 2026-09-17T18:04:30.655153+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00027-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00027-of-00031', 'bytes': 113599658, 'complete': True}; cumulative payload 1,966,345,349 bytes (+ reserved dependency allowance).

- 2026-09-17T18:04:30.655404+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00028-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00028-of-00031`

- 2026-09-17T18:04:34.908892+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00028-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00028-of-00031', 'bytes': 29432148, 'complete': True}; cumulative payload 1,995,777,497 bytes (+ reserved dependency allowance).

- 2026-09-17T18:04:34.909118+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00029-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00029-of-00031`

- 2026-09-17T18:04:37.065504+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00029-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00029-of-00031', 'bytes': 20013917, 'complete': True}; cumulative payload 2,015,791,414 bytes (+ reserved dependency allowance).

- 2026-09-17T18:04:37.065756+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00030-of-00031 data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00030-of-00031`

- 2026-09-17T18:04:55.278357+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00030-of-00031', 'file': 'data/droid_100/1.0.0/r2d2_faceblur-train.tfrecord-00030-of-00031', 'bytes': 176860291, 'complete': True}; cumulative payload 2,192,651,705 bytes (+ reserved dependency allowance).

- Reconciled download ledger from per-transfer LOG.md entries: concurrent documentation/sample transfers could overwrite the JSON ledger; the append-only log preserved each result. Serialize future transfers.

- 2026-09-17T18:04:59.470111+00:00 Menagerie pinned tree 8161bba264d7fa7c99ca301e91e7fb44737676ad. Fetch only franka_emika_panda and robotiq_2f85 XML, mesh assets and licenses; exclude preview videos/images.

- 2026-09-17T18:04:59.470726+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/LICENSE vendor/mujoco_menagerie/franka_emika_panda/LICENSE`

- 2026-09-17T18:04:59.588775+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/LICENSE', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/LICENSE', 'bytes': 10173, 'complete': True}; cumulative payload 2,193,567,774 bytes (+ reserved dependency allowance).

- 2026-09-17T18:04:59.589231+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/README.md vendor/mujoco_menagerie/franka_emika_panda/README.md`

- 2026-09-17T18:04:59.742177+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/README.md', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/README.md', 'bytes': 2908, 'complete': True}; cumulative payload 2,193,570,682 bytes (+ reserved dependency allowance).

- 2026-09-17T18:04:59.742409+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/finger_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/finger_0.obj`

- 2026-09-17T18:04:59.895934+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/finger_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/finger_0.obj', 'bytes': 87872, 'complete': True}; cumulative payload 2,193,658,554 bytes (+ reserved dependency allowance).

- 2026-09-17T18:04:59.896232+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/finger_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/finger_1.obj`

- 2026-09-17T18:05:00.014338+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/finger_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/finger_1.obj', 'bytes': 64651, 'complete': True}; cumulative payload 2,193,723,205 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:00.014554+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand.stl vendor/mujoco_menagerie/franka_emika_panda/assets/hand.stl`

- 2026-09-17T18:05:00.157116+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand.stl', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/hand.stl', 'bytes': 10084, 'complete': True}; cumulative payload 2,193,733,289 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:00.157498+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/hand_0.obj`

- 2026-09-17T18:05:00.289856+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/hand_0.obj', 'bytes': 9091, 'complete': True}; cumulative payload 2,193,742,380 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:00.290252+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/hand_1.obj`

- 2026-09-17T18:05:00.531063+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/hand_1.obj', 'bytes': 121863, 'complete': True}; cumulative payload 2,193,864,243 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:00.531280+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/hand_2.obj`

- 2026-09-17T18:05:00.730097+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/hand_2.obj', 'bytes': 596001, 'complete': True}; cumulative payload 2,194,460,244 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:00.730302+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_3.obj vendor/mujoco_menagerie/franka_emika_panda/assets/hand_3.obj`

- 2026-09-17T18:05:01.127791+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_3.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/hand_3.obj', 'bytes': 902145, 'complete': True}; cumulative payload 2,195,362,389 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:01.128247+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_4.obj vendor/mujoco_menagerie/franka_emika_panda/assets/hand_4.obj`

- 2026-09-17T18:05:01.302075+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/hand_4.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/hand_4.obj', 'bytes': 151988, 'complete': True}; cumulative payload 2,195,514,377 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:01.302295+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0.stl vendor/mujoco_menagerie/franka_emika_panda/assets/link0.stl`

- 2026-09-17T18:05:01.396532+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0.stl', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0.stl', 'bytes': 10084, 'complete': True}; cumulative payload 2,195,524,461 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:01.396813+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_0.obj`

- 2026-09-17T18:05:01.579916+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_0.obj', 'bytes': 296497, 'complete': True}; cumulative payload 2,195,820,958 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:01.580124+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_1.obj`

- 2026-09-17T18:05:01.742866+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_1.obj', 'bytes': 103978, 'complete': True}; cumulative payload 2,195,924,936 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:01.743077+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_10.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_10.obj`

- 2026-09-17T18:05:01.938319+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_10.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_10.obj', 'bytes': 343308, 'complete': True}; cumulative payload 2,196,268,244 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:01.938572+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_11.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_11.obj`

- 2026-09-17T18:05:02.079756+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_11.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_11.obj', 'bytes': 22295, 'complete': True}; cumulative payload 2,196,290,539 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:02.080524+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_2.obj`

- 2026-09-17T18:05:02.302308+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_2.obj', 'bytes': 590892, 'complete': True}; cumulative payload 2,196,881,431 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:02.303094+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_3.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_3.obj`

- 2026-09-17T18:05:02.418376+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_3.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_3.obj', 'bytes': 47588, 'complete': True}; cumulative payload 2,196,929,019 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:02.419093+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_4.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_4.obj`

- 2026-09-17T18:05:02.621791+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_4.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_4.obj', 'bytes': 211200, 'complete': True}; cumulative payload 2,197,140,219 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:02.622387+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_5.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_5.obj`

- 2026-09-17T18:05:02.721296+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_5.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_5.obj', 'bytes': 17023, 'complete': True}; cumulative payload 2,197,157,242 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:02.721923+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_7.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_7.obj`

- 2026-09-17T18:05:02.849552+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_7.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_7.obj', 'bytes': 30699, 'complete': True}; cumulative payload 2,197,187,941 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:02.849856+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_8.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_8.obj`

- 2026-09-17T18:05:03.410437+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_8.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_8.obj', 'bytes': 3263194, 'complete': True}; cumulative payload 2,200,451,135 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:03.410755+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_9.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link0_9.obj`

- 2026-09-17T18:05:03.577581+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link0_9.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link0_9.obj', 'bytes': 105629, 'complete': True}; cumulative payload 2,200,556,764 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:03.577834+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link1.obj`

- 2026-09-17T18:05:04.079253+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link1.obj', 'bytes': 3274995, 'complete': True}; cumulative payload 2,203,831,759 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:04.079610+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link1.stl vendor/mujoco_menagerie/franka_emika_panda/assets/link1.stl`

- 2026-09-17T18:05:04.209283+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link1.stl', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link1.stl', 'bytes': 15084, 'complete': True}; cumulative payload 2,203,846,843 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:04.209625+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link2.obj`

- 2026-09-17T18:05:05.391189+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link2.obj', 'bytes': 3295608, 'complete': True}; cumulative payload 2,207,142,451 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:05.391430+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link2.stl vendor/mujoco_menagerie/franka_emika_panda/assets/link2.stl`

- 2026-09-17T18:05:05.572461+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link2.stl', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link2.stl', 'bytes': 15084, 'complete': True}; cumulative payload 2,207,157,535 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:05.572773+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3.stl vendor/mujoco_menagerie/franka_emika_panda/assets/link3.stl`

- 2026-09-17T18:05:05.685680+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3.stl', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link3.stl', 'bytes': 15084, 'complete': True}; cumulative payload 2,207,172,619 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:05.686165+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link3_0.obj`

- 2026-09-17T18:05:06.179113+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link3_0.obj', 'bytes': 3046804, 'complete': True}; cumulative payload 2,210,219,423 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:06.179363+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link3_1.obj`

- 2026-09-17T18:05:06.303691+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link3_1.obj', 'bytes': 65260, 'complete': True}; cumulative payload 2,210,284,683 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:06.304022+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3_2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link3_2.obj`

- 2026-09-17T18:05:06.455183+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3_2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link3_2.obj', 'bytes': 83591, 'complete': True}; cumulative payload 2,210,368,274 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:06.455648+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3_3.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link3_3.obj`

- 2026-09-17T18:05:06.679491+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link3_3.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link3_3.obj', 'bytes': 457684, 'complete': True}; cumulative payload 2,210,825,958 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:06.679748+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4.stl vendor/mujoco_menagerie/franka_emika_panda/assets/link4.stl`

- 2026-09-17T18:05:06.791974+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4.stl', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link4.stl', 'bytes': 15084, 'complete': True}; cumulative payload 2,210,841,042 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:06.792336+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link4_0.obj`

- 2026-09-17T18:05:06.943779+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link4_0.obj', 'bytes': 83486, 'complete': True}; cumulative payload 2,210,924,528 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:06.944438+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link4_1.obj`

- 2026-09-17T18:05:07.601382+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link4_1.obj', 'bytes': 3148001, 'complete': True}; cumulative payload 2,214,072,529 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:07.602044+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4_2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link4_2.obj`

- 2026-09-17T18:05:07.788939+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4_2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link4_2.obj', 'bytes': 455522, 'complete': True}; cumulative payload 2,214,528,051 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:07.789379+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4_3.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link4_3.obj`

- 2026-09-17T18:05:07.918918+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link4_3.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link4_3.obj', 'bytes': 67497, 'complete': True}; cumulative payload 2,214,595,548 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:07.919324+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link5_0.obj`

- 2026-09-17T18:05:08.162912+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link5_0.obj', 'bytes': 824158, 'complete': True}; cumulative payload 2,215,419,706 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:08.163162+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link5_1.obj`

- 2026-09-17T18:05:08.320094+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link5_1.obj', 'bytes': 63174, 'complete': True}; cumulative payload 2,215,482,880 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:08.320458+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link5_2.obj`

- 2026-09-17T18:05:08.835789+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link5_2.obj', 'bytes': 3856621, 'complete': True}; cumulative payload 2,219,339,501 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:08.836098+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_collision_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link5_collision_0.obj`

- 2026-09-17T18:05:08.935707+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_collision_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link5_collision_0.obj', 'bytes': 3861, 'complete': True}; cumulative payload 2,219,343,362 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:08.936052+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_collision_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link5_collision_1.obj`

- 2026-09-17T18:05:09.037585+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_collision_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link5_collision_1.obj', 'bytes': 2412, 'complete': True}; cumulative payload 2,219,345,774 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:09.037849+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_collision_2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link5_collision_2.obj`

- 2026-09-17T18:05:09.149281+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link5_collision_2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link5_collision_2.obj', 'bytes': 3786, 'complete': True}; cumulative payload 2,219,349,560 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:09.149571+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6.stl vendor/mujoco_menagerie/franka_emika_panda/assets/link6.stl`

- 2026-09-17T18:05:09.280250+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6.stl', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6.stl', 'bytes': 10084, 'complete': True}; cumulative payload 2,219,359,644 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:09.280865+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_0.obj`

- 2026-09-17T18:05:09.476290+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_0.obj', 'bytes': 157563, 'complete': True}; cumulative payload 2,219,517,207 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:09.476593+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_1.obj`

- 2026-09-17T18:05:09.619004+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_1.obj', 'bytes': 27106, 'complete': True}; cumulative payload 2,219,544,313 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:09.619315+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_10.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_10.obj`

- 2026-09-17T18:05:09.830115+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_10.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_10.obj', 'bytes': 368502, 'complete': True}; cumulative payload 2,219,912,815 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:09.830371+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_11.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_11.obj`

- 2026-09-17T18:05:09.930979+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_11.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_11.obj', 'bytes': 32653, 'complete': True}; cumulative payload 2,219,945,468 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:09.931279+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_12.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_12.obj`

- 2026-09-17T18:05:10.037334+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_12.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_12.obj', 'bytes': 3894, 'complete': True}; cumulative payload 2,219,949,362 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:10.037607+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_13.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_13.obj`

- 2026-09-17T18:05:10.192541+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_13.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_13.obj', 'bytes': 3798, 'complete': True}; cumulative payload 2,219,953,160 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:10.192882+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_14.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_14.obj`

- 2026-09-17T18:05:10.436180+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_14.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_14.obj', 'bytes': 444469, 'complete': True}; cumulative payload 2,220,397,629 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:10.436655+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_15.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_15.obj`

- 2026-09-17T18:05:10.705670+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_15.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_15.obj', 'bytes': 668552, 'complete': True}; cumulative payload 2,221,066,181 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:10.705998+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_16.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_16.obj`

- 2026-09-17T18:05:11.372808+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_16.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_16.obj', 'bytes': 3675358, 'complete': True}; cumulative payload 2,224,741,539 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:11.373211+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_2.obj`

- 2026-09-17T18:05:11.475936+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_2.obj', 'bytes': 9916, 'complete': True}; cumulative payload 2,224,751,455 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:11.476257+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_3.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_3.obj`

- 2026-09-17T18:05:11.573870+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_3.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_3.obj', 'bytes': 11943, 'complete': True}; cumulative payload 2,224,763,398 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:11.574167+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_4.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_4.obj`

- 2026-09-17T18:05:11.694150+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_4.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_4.obj', 'bytes': 13846, 'complete': True}; cumulative payload 2,224,777,244 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:11.694629+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_5.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_5.obj`

- 2026-09-17T18:05:11.795398+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_5.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_5.obj', 'bytes': 11841, 'complete': True}; cumulative payload 2,224,789,085 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:11.795892+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_6.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_6.obj`

- 2026-09-17T18:05:11.918522+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_6.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_6.obj', 'bytes': 12597, 'complete': True}; cumulative payload 2,224,801,682 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:11.918852+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_7.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_7.obj`

- 2026-09-17T18:05:12.015136+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_7.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_7.obj', 'bytes': 4382, 'complete': True}; cumulative payload 2,224,806,064 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:12.015421+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_8.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_8.obj`

- 2026-09-17T18:05:12.107935+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_8.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_8.obj', 'bytes': 9131, 'complete': True}; cumulative payload 2,224,815,195 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:12.108218+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_9.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link6_9.obj`

- 2026-09-17T18:05:12.226145+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link6_9.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link6_9.obj', 'bytes': 17616, 'complete': True}; cumulative payload 2,224,832,811 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:12.226454+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7.stl vendor/mujoco_menagerie/franka_emika_panda/assets/link7.stl`

- 2026-09-17T18:05:12.342326+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7.stl', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7.stl', 'bytes': 10084, 'complete': True}; cumulative payload 2,224,842,895 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:12.342705+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_0.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link7_0.obj`

- 2026-09-17T18:05:12.625949+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_0.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7_0.obj', 'bytes': 1362355, 'complete': True}; cumulative payload 2,226,205,250 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:12.626264+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_1.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link7_1.obj`

- 2026-09-17T18:05:12.787354+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_1.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7_1.obj', 'bytes': 121358, 'complete': True}; cumulative payload 2,226,326,608 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:12.787959+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_2.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link7_2.obj`

- 2026-09-17T18:05:12.982809+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_2.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7_2.obj', 'bytes': 208907, 'complete': True}; cumulative payload 2,226,535,515 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:12.983155+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_3.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link7_3.obj`

- 2026-09-17T18:05:13.172845+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_3.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7_3.obj', 'bytes': 123684, 'complete': True}; cumulative payload 2,226,659,199 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:13.173403+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_4.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link7_4.obj`

- 2026-09-17T18:05:13.313135+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_4.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7_4.obj', 'bytes': 85732, 'complete': True}; cumulative payload 2,226,744,931 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:13.313656+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_5.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link7_5.obj`

- 2026-09-17T18:05:13.546328+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_5.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7_5.obj', 'bytes': 226402, 'complete': True}; cumulative payload 2,226,971,333 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:13.546606+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_6.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link7_6.obj`

- 2026-09-17T18:05:13.662772+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_6.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7_6.obj', 'bytes': 99900, 'complete': True}; cumulative payload 2,227,071,233 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:13.663188+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_7.obj vendor/mujoco_menagerie/franka_emika_panda/assets/link7_7.obj`

- 2026-09-17T18:05:13.886208+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/assets/link7_7.obj', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/assets/link7_7.obj', 'bytes': 792162, 'complete': True}; cumulative payload 2,227,863,395 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:13.886586+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/hand.xml vendor/mujoco_menagerie/franka_emika_panda/hand.xml`

- 2026-09-17T18:05:13.996259+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/hand.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/hand.xml', 'bytes': 4547, 'complete': True}; cumulative payload 2,227,867,942 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:13.996750+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_hand.xml vendor/mujoco_menagerie/franka_emika_panda/mjx_hand.xml`

- 2026-09-17T18:05:14.130470+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_hand.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/mjx_hand.xml', 'bytes': 4222, 'complete': True}; cumulative payload 2,227,872,164 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:14.130801+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_panda.xml vendor/mujoco_menagerie/franka_emika_panda/mjx_panda.xml`

- 2026-09-17T18:05:14.244484+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_panda.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/mjx_panda.xml', 'bytes': 14387, 'complete': True}; cumulative payload 2,227,886,551 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:14.244754+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_panda_nohand.xml vendor/mujoco_menagerie/franka_emika_panda/mjx_panda_nohand.xml`

- 2026-09-17T18:05:14.366900+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_panda_nohand.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/mjx_panda_nohand.xml', 'bytes': 10468, 'complete': True}; cumulative payload 2,227,897,019 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:14.367209+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_scene.xml vendor/mujoco_menagerie/franka_emika_panda/mjx_scene.xml`

- 2026-09-17T18:05:14.473097+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_scene.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/mjx_scene.xml', 'bytes': 1163, 'complete': True}; cumulative payload 2,227,898,182 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:14.473388+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_single_cube.xml vendor/mujoco_menagerie/franka_emika_panda/mjx_single_cube.xml`

- 2026-09-17T18:05:14.497957+00:00 Decoded all 100 episodes with TFDS. Saved actual schema and exterior start/mid/end contact sheets. Screening durations initially assume 15 Hz, to be verified against platform code/raw timestamps. No trajectory filtering or trimming.

- 2026-09-17T18:05:14.599814+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/mjx_single_cube.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/mjx_single_cube.xml', 'bytes': 1180, 'complete': True}; cumulative payload 2,227,899,362 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:14.600080+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/panda.png vendor/mujoco_menagerie/franka_emika_panda/panda.png`

- 2026-09-17T18:05:15.073776+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/panda.png', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/panda.png', 'bytes': 2192427, 'complete': True}; cumulative payload 2,230,091,789 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:15.074114+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/panda.xml vendor/mujoco_menagerie/franka_emika_panda/panda.xml`

- 2026-09-17T18:05:15.272071+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/panda.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/panda.xml', 'bytes': 14438, 'complete': True}; cumulative payload 2,230,106,227 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:15.272480+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/panda_nohand.xml vendor/mujoco_menagerie/franka_emika_panda/panda_nohand.xml`

- 2026-09-17T18:05:15.389223+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/panda_nohand.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/panda_nohand.xml', 'bytes': 11246, 'complete': True}; cumulative payload 2,230,117,473 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:15.389582+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/scene.xml vendor/mujoco_menagerie/franka_emika_panda/scene.xml`

- 2026-09-17T18:05:15.503352+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/franka_emika_panda/scene.xml', 'file': 'vendor/mujoco_menagerie/franka_emika_panda/scene.xml', 'bytes': 819, 'complete': True}; cumulative payload 2,230,118,292 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:15.503972+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/2f85.png vendor/mujoco_menagerie/robotiq_2f85/2f85.png`

- 2026-09-17T18:05:15.776456+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/2f85.png', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/2f85.png', 'bytes': 1140430, 'complete': True}; cumulative payload 2,231,258,722 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:15.776738+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/2f85.xml vendor/mujoco_menagerie/robotiq_2f85/2f85.xml`

- 2026-09-17T18:05:15.892279+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/2f85.xml', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/2f85.xml', 'bytes': 9540, 'complete': True}; cumulative payload 2,231,268,262 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:15.892631+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/LICENSE vendor/mujoco_menagerie/robotiq_2f85/LICENSE`

- 2026-09-17T18:05:15.987200+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/LICENSE', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/LICENSE', 'bytes': 1297, 'complete': True}; cumulative payload 2,231,269,559 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:15.987442+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/README.md vendor/mujoco_menagerie/robotiq_2f85/README.md`

- 2026-09-17T18:05:16.080764+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/README.md', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/README.md', 'bytes': 1367, 'complete': True}; cumulative payload 2,231,270,926 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:16.081042+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/base.stl vendor/mujoco_menagerie/robotiq_2f85/assets/base.stl`

- 2026-09-17T18:05:16.420509+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/base.stl', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/assets/base.stl', 'bytes': 1712484, 'complete': True}; cumulative payload 2,232,983,410 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:16.420819+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/base_mount.stl vendor/mujoco_menagerie/robotiq_2f85/assets/base_mount.stl`

- 2026-09-17T18:05:16.690714+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/base_mount.stl', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/assets/base_mount.stl', 'bytes': 1091784, 'complete': True}; cumulative payload 2,234,075,194 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:16.690973+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/coupler.stl vendor/mujoco_menagerie/robotiq_2f85/assets/coupler.stl`

- 2026-09-17T18:05:16.850992+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/coupler.stl', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/assets/coupler.stl', 'bytes': 89084, 'complete': True}; cumulative payload 2,234,164,278 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:16.851266+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/driver.stl vendor/mujoco_menagerie/robotiq_2f85/assets/driver.stl`

- 2026-09-17T18:05:16.970044+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/driver.stl', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/assets/driver.stl', 'bytes': 67084, 'complete': True}; cumulative payload 2,234,231,362 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:16.970315+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/follower.stl vendor/mujoco_menagerie/robotiq_2f85/assets/follower.stl`

- 2026-09-17T18:05:17.141126+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/follower.stl', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/assets/follower.stl', 'bytes': 110484, 'complete': True}; cumulative payload 2,234,341,846 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:17.141441+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/pad.stl vendor/mujoco_menagerie/robotiq_2f85/assets/pad.stl`

- 2026-09-17T18:05:17.275185+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/pad.stl', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/assets/pad.stl', 'bytes': 15084, 'complete': True}; cumulative payload 2,234,356,930 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:17.275439+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/silicone_pad.stl vendor/mujoco_menagerie/robotiq_2f85/assets/silicone_pad.stl`

- 2026-09-17T18:05:17.381346+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/silicone_pad.stl', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/assets/silicone_pad.stl', 'bytes': 15084, 'complete': True}; cumulative payload 2,234,372,014 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:17.381700+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/spring_link.stl vendor/mujoco_menagerie/robotiq_2f85/assets/spring_link.stl`

- 2026-09-17T18:05:17.522703+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/assets/spring_link.stl', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/assets/spring_link.stl', 'bytes': 84884, 'complete': True}; cumulative payload 2,234,456,898 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:17.522956+00:00 Download: `python download.py https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/scene.xml vendor/mujoco_menagerie/robotiq_2f85/scene.xml`

- 2026-09-17T18:05:17.614899+00:00 Download result: {'url': 'https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/8161bba264d7fa7c99ca301e91e7fb44737676ad/robotiq_2f85/scene.xml', 'file': 'vendor/mujoco_menagerie/robotiq_2f85/scene.xml', 'bytes': 1393, 'complete': True}; cumulative payload 2,234,458,291 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:17.659761+00:00 Download: `python download.py https://huggingface.co/KarlP/droid/resolve/main/episode_id_to_path.json data/calibration/episode_id_to_path.json`

- 2026-09-17T18:05:19.014440+00:00 Download result: {'url': 'https://huggingface.co/KarlP/droid/resolve/main/episode_id_to_path.json', 'file': 'data/calibration/episode_id_to_path.json', 'bytes': 7237770, 'complete': True}; cumulative payload 2,241,696,061 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:19.014775+00:00 Download: `python download.py https://huggingface.co/KarlP/droid/resolve/main/cam2base_extrinsics.json data/calibration/cam2base_extrinsics.json`

- 2026-09-17T18:05:20.740171+00:00 Download result: {'url': 'https://huggingface.co/KarlP/droid/resolve/main/cam2base_extrinsics.json', 'file': 'data/calibration/cam2base_extrinsics.json', 'bytes': 16236005, 'complete': True}; cumulative payload 2,257,932,066 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:20.740740+00:00 Download: `python download.py https://huggingface.co/KarlP/droid/resolve/main/cam2base_extrinsic_superset.json data/calibration/cam2base_extrinsic_superset.json`

- 2026-09-17T18:05:22.836460+00:00 Download result: {'url': 'https://huggingface.co/KarlP/droid/resolve/main/cam2base_extrinsic_superset.json', 'file': 'data/calibration/cam2base_extrinsic_superset.json', 'bytes': 20310686, 'complete': True}; cumulative payload 2,278,242,752 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:22.836900+00:00 Download: `python download.py https://huggingface.co/KarlP/droid/resolve/main/cam2cam_extrinsics.json data/calibration/cam2cam_extrinsics.json`

- 2026-09-17T18:05:39.949381+00:00 Download result: {'url': 'https://huggingface.co/KarlP/droid/resolve/main/cam2cam_extrinsics.json', 'file': 'data/calibration/cam2cam_extrinsics.json', 'bytes': 189389442, 'complete': True}; cumulative payload 2,467,632,194 bytes (+ reserved dependency allowance).

- 2026-09-17T18:05:39.949672+00:00 Download: `python download.py https://huggingface.co/KarlP/droid/resolve/main/intrinsics.json data/calibration/intrinsics.json`

- 2026-09-17T18:05:51.839303+00:00 Download result: {'url': 'https://huggingface.co/KarlP/droid/resolve/main/intrinsics.json', 'file': 'data/calibration/intrinsics.json', 'bytes': 125812944, 'complete': True}; cumulative payload 2,593,445,138 bytes (+ reserved dependency allowance).

- 2026-09-17T18:06:59.239737+00:00 Selected episode 74, Move the yellow mug forward: 167 frames / 15 Hz = 11.13 s; success path and reward=1; a single opaque yellow-green mug, visible at start in both exterior views, on mostly clear white tabletop. Surface looks diffuse at RLDS resolution; fine ceramic glaze cannot be ruled out. Two distant background items are not manipulated. Prefer this over 6 (small pen in bowl, difficult contact/visibility), 4 (marker partly hidden in cup), 60 (block outside ext1 initial view), 20 (lid removal/contact with second object, less clear instruction). Top-five sheets copied to artifacts/top5; all 100 sheets retained.

- 2026-09-17T18:07:01.876134+00:00 Download: `python download.py https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_raw%2F1.0.1%2FCLVR%2Fsuccess%2F2023-05-09%2FTue_May__9_02%3A08%3A20_2023%2F&maxResults=1000 sources/raw_listing.json`

- 2026-09-17T18:07:02.013444+00:00 Download result: {'url': 'https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_raw%2F1.0.1%2FCLVR%2Fsuccess%2F2023-05-09%2FTue_May__9_02%3A08%3A20_2023%2F&maxResults=1000', 'file': 'sources/raw_listing.json', 'bytes': 15358, 'complete': True}; cumulative payload 2,593,460,496 bytes (+ reserved dependency allowance).

- 2026-09-17T18:07:02.085927+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/metadata_CLVR%2B236539bc%2B2023-05-09-02h-08m-20s.json data/raw/metadata_CLVR+236539bc+2023-05-09-02h-08m-20s.json`

- 2026-09-17T18:07:02.249281+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/metadata_CLVR%2B236539bc%2B2023-05-09-02h-08m-20s.json', 'file': 'data/raw/metadata_CLVR+236539bc+2023-05-09-02h-08m-20s.json', 'bytes': 1770, 'complete': True}; cumulative payload 2,593,462,266 bytes (+ reserved dependency allowance).

- 2026-09-17T18:07:02.249809+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/recordings/MP4/16787047-stereo.mp4 data/raw/recordings/MP4/16787047-stereo.mp4`

- 2026-09-17T18:07:03.118169+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/recordings/MP4/16787047-stereo.mp4', 'file': 'data/raw/recordings/MP4/16787047-stereo.mp4', 'bytes': 2705268, 'complete': True}; cumulative payload 2,596,167,534 bytes (+ reserved dependency allowance).

- 2026-09-17T18:07:03.118716+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/recordings/MP4/20103212-stereo.mp4 data/raw/recordings/MP4/20103212-stereo.mp4`

- 2026-09-17T18:07:03.781139+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/recordings/MP4/20103212-stereo.mp4', 'file': 'data/raw/recordings/MP4/20103212-stereo.mp4', 'bytes': 3633005, 'complete': True}; cumulative payload 2,599,800,539 bytes (+ reserved dependency allowance).

- 2026-09-17T18:07:03.781599+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/recordings/MP4/20655732-stereo.mp4 data/raw/recordings/MP4/20655732-stereo.mp4`

- 2026-09-17T18:07:04.460873+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/recordings/MP4/20655732-stereo.mp4', 'file': 'data/raw/recordings/MP4/20655732-stereo.mp4', 'bytes': 4554522, 'complete': True}; cumulative payload 2,604,355,061 bytes (+ reserved dependency allowance).

- 2026-09-17T18:07:04.461263+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/trajectory.h5 data/raw/trajectory.h5`

- 2026-09-17T18:07:04.771401+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/trajectory.h5', 'file': 'data/raw/trajectory.h5', 'bytes': 1071936, 'complete': True}; cumulative payload 2,605,426,997 bytes (+ reserved dependency allowance).

- 2026-09-17T18:07:04.771715+00:00 Download: `python download.py https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/trajectory_im128.h5 data/raw/trajectory_im128.h5`

- 2026-09-17T18:07:05.189458+00:00 Download result: {'url': 'https://storage.googleapis.com/gresearch/robotics/droid_raw/1.0.1/CLVR/success/2023-05-09/Tue_May__9_02%3A08%3A20_2023/trajectory_im128.h5', 'file': 'data/raw/trajectory_im128.h5', 'bytes': 1525856, 'complete': True}; cumulative payload 2,606,952,853 bytes (+ reserved dependency allowance).

- 2026-09-17T18:07:36.297349+00:00 Extracted chosen RLDS episode without trimming/resampling/filtering: 167 recorded joint and gripper samples, three 15 Hz videos and start/mid/end frames. trajectory.npz SHA256 saved. Gripper opening initially computed as 0.085*(1-normalized closure); verify against raw platform convention. Observed states are fixed position-control targets for every iteration.

- 2026-09-17T18:08:35.734247+00:00 Raw release reachable: fetched all three stereo MP4s, metadata and HDF5 for chosen episode only. Extracted HD monocular videos and keyframes. Cameras use released per-camera intrinsics; published cam2base covers ext1 but source=GT and equals raw calibration; no superset entry; ext2 initially uses raw calibration. SGBM depth at first frame for all three pairs; nominal ZED2 baseline 0.12 m / ZED Mini 0.063 m assumed because exact rectified baseline not in metadata. Raw timing statistics saved; RLDS omits final raw sample, preserve RLDS trajectory exactly.

- 2026-09-17T18:08:48.315950+00:00 Download: `python download.py https://raw.githubusercontent.com/droid-dataset/droid/main/droid/robot_ik/franka/panda.xml sources/droid_panda.xml`

- 2026-09-17T18:08:48.476691+00:00 Download result: {'url': 'https://raw.githubusercontent.com/droid-dataset/droid/main/droid/robot_ik/franka/panda.xml', 'file': 'sources/droid_panda.xml', 'bytes': 5594, 'complete': True}; cumulative payload 2,606,958,447 bytes (+ reserved dependency allowance).

- 2026-09-17T18:08:48.519461+00:00 Download: `python download.py https://api.github.com/repos/droid-dataset/droid/git/trees/main?recursive=1 sources/droid_tree.json`

- 2026-09-17T18:08:48.881790+00:00 Download result: {'url': 'https://api.github.com/repos/droid-dataset/droid/git/trees/main?recursive=1', 'file': 'sources/droid_tree.json', 'bytes': 71087, 'complete': True}; cumulative payload 2,607,029,534 bytes (+ reserved dependency allowance).

- 2026-09-17T18:09:02.803001+00:00 Download: `python download.py https://raw.githubusercontent.com/droid-dataset/droid/main/droid/franka/robot.py sources/droid_robot.py`

- 2026-09-17T18:09:02.917102+00:00 Download result: {'url': 'https://raw.githubusercontent.com/droid-dataset/droid/main/droid/franka/robot.py', 'file': 'sources/droid_robot.py', 'bytes': 11102, 'complete': True}; cumulative payload 2,607,040,636 bytes (+ reserved dependency allowance).

- 2026-09-17T18:12:45.763851+00:00 Download: `python download.py https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_raw%2F1.0.1%2FIRIS%2Fsuccess%2F2023-05-04%2FThu_May__4_13%3A41%3A33_2023%2F&maxResults=1000 sources/raw_pen_listing.json`

- 2026-09-17T18:12:45.893347+00:00 Download result: {'url': 'https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_raw%2F1.0.1%2FIRIS%2Fsuccess%2F2023-05-04%2FThu_May__4_13%3A41%3A33_2023%2F&maxResults=1000', 'file': 'sources/raw_pen_listing.json', 'bytes': 32, 'complete': True}; cumulative payload 2,607,040,668 bytes (+ reserved dependency allowance).

- 2026-09-17T18:12:48.473109+00:00 HD review REJECTED candidate 74: wrist view reveals glossy ceramic mug, violating non-shiny criterion. Candidate 6 becomes selected: 181 frames, successful, opaque pen/marker in a bowl on clear circular table, visible both initial exterior views. Raw downloads of rejected mug retained and charged to budget; this is a disclosed departure from only-one-final-episode raw fetching, caused by HD-only evidence. No other episode raw data fetched. Candidate 6 raw listing and calibration coverage recorded.

- 2026-09-17T18:13:11.301826+00:00 Extracted chosen RLDS episode without trimming/resampling/filtering: 167 recorded joint and gripper samples, three 15 Hz videos and start/mid/end frames. trajectory.npz SHA256 saved. Gripper opening initially computed as 0.085*(1-normalized closure); verify against raw platform convention. Observed states are fixed position-control targets for every iteration.

- 2026-09-17T18:13:52.629436+00:00 Download: `python download.py https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_raw%2F1.0.0%2FIRIS%2Fsuccess%2F2023-05-04%2FThu_May__4_13%3A41%3A33_2023%2F&maxResults=1000 sources/raw_pen_listing_1.0.0.json`

- 2026-09-17T18:13:52.751864+00:00 Download result: {'url': 'https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_raw%2F1.0.0%2FIRIS%2Fsuccess%2F2023-05-04%2FThu_May__4_13%3A41%3A33_2023%2F&maxResults=1000', 'file': 'sources/raw_pen_listing_1.0.0.json', 'bytes': 32, 'complete': True}; cumulative payload 2,607,040,700 bytes (+ reserved dependency allowance).

- 2026-09-17T18:13:52.752421+00:00 Download: `python download.py https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_raw%2FIRIS%2Fsuccess%2F2023-05-04%2FThu_May__4_13%3A41%3A33_2023%2F&maxResults=1000 sources/raw_pen_listing_unversioned.json`

- 2026-09-17T18:13:52.864615+00:00 Download result: {'url': 'https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics%2Fdroid_raw%2FIRIS%2Fsuccess%2F2023-05-04%2FThu_May__4_13%3A41%3A33_2023%2F&maxResults=1000', 'file': 'sources/raw_pen_listing_unversioned.json', 'bytes': 32, 'complete': True}; cumulative payload 2,607,040,732 bytes (+ reserved dependency allowance).

- 2026-09-17T18:13:52.864778+00:00 Selected pen episode exact raw prefix is empty in official 1.0.1, alternative 1.0.0 and unversioned prefixes also checked. Episode absent from published ID/path map and all calibration coverage. Activate user-authorized RLDS fallback: no stereo/depth for final episode; estimate cameras from known robot kinematics and manually annotated image correspondences; 15 Hz documented control rate assumed because raw timestamps unavailable.

- 2026-09-17T18:16:13.665268+00:00 Fallback camera estimates: manually annotated eight pinch locations per exterior camera; solvePnP then robust refinement with focal prior 135 px +/-15 (320x180). Principal point at image center, zero lens distortion assumed. Save correspondences and reprojection overlays. This estimates calibration; it is not released ground truth.

## Reconstruction and iteration 1
- Selected final episode 6: IRIS/success/2023-05-04/Thu_May__4_13:41:33_2023, 181 samples at documented 15 Hz = 12.07 seconds. Real video shows a black/teal opaque marker removed from an open bowl and placed on a clear circular table. Bowl has some highlights but the manipulated marker is opaque plastic, not transparent or mirror-reflective. Only the marker is intentionally manipulated; bowl is a separate dynamic support and may be touched.
- Initial cameras: PnP on eight manually marked pinch locations each, robust fit with 135 px focal prior; then jointly refine with white circular table silhouettes. Fitted table radius 0.2574 m, top z=-0.0401 m. These are estimates, not depth measurements. A horizontal table, centered principal points, square pixels, zero distortion are assumptions.
- Robot: official Menagerie tree 8161bba264d7fa7c99ca301e91e7fb44737676ad; Panda arm with original Panda hand removed, official Robotiq 2F-85 attached at 0.107 m flange and Panda hand -45 degree rotation. Native Robotiq mount offset retained. Names prefixed to avoid asset/default collisions. No invented robot links. FK flange agrees with recorded Cartesian positions to floating-point precision. Hardware adapter/camera/cables omitted; exact mount orientation remains an assumption to review visually.
- Native Menagerie position actuators retained; gravity compensation enabled on robot bodies to approximate DROID controller feedforward, not objects. No kinematic welds, scripted object motion, or grasp attachment.
- Gripper convention verified in official droid/franka/robot.py: normalized position is closure, width=max_width*(1-command). Max width assumed 85 mm from required model. Control converts recorded closure to Menagerie 0..255 native position range.
- Scene: primitive circular table; open tapered bowl represented by 32 convex wall wedges plus base; capsule marker with teal cap and visual label. Separate bowl and marker free bodies. Dimensions/poses/provenance in scene_parameters.json. Masses/friction assumed (marker 18g, bowl 180g). Background simplified to floor.
- Ran build_scene.py, replay.py --out artifacts/iteration1, compare.py and success.py. Position targets interpolate between unchanged recorded observations at 15 Hz; trajectory SHA256 asserted every run. No filtering, trimming or retiming for final episode. Render all 181 frames from both exterior cameras; comparison uses sample-index alignment.

- 2026-09-17T18:22:16.200828+00:00 Iteration1 FAILED: pen stayed in bowl; 12 contact frames, max z=-20.3mm; initial marker-wall penetration up to13.2mm; object drift/rotation before grasp; no solver warnings. Visuals show similar table silhouette but absent wrist camera/cables, elbow alignment errors, harsh shadows, smooth faceted bowl. Iteration2 scene-only changes: marker length140->120mm, radius7.5->8.4mm, initial y -256->-267mm, reverse cap orientation; bowl bottom radius53->66mm. All changes disclosed as estimated scene geometry/pose, not trajectory optimization. Native robot and controls unchanged.

- 2026-09-17T18:24:14.273045+00:00 Iteration2 PASSED predicate and visual review: marker lifted to z=0.1267m, 47 sampled gripper contact frames, released onto table at (0.5195,-0.0949,-0.0316)m; no initial collision or solver warnings. Grasp rotates marker about50deg before stable transport; real final orientation differs. Max contact penetration4.23mm; end translation speed2.3mm/s but residual roll0.27rad/s. Iteration3 changes only marker contact parameters: priority2, condim6, friction0.8/0.002/0.0001, impedance0.98/0.995, time constant0.004s; add diagnostics for worst contact. Robot control/recorded trajectory identical.

- 2026-09-17T18:25:48.288189+00:00 Iteration3 FAILED: stiffer contacts reduce maximum penetration to0.371mm but marker is pushed sideways out of the pinch before lift; only9 contact frames. This demonstrates iteration2 success was contact-sensitive. Iteration4 retains stiff contacts and shifts bowl+marker by(+14,-8,0)mm to align estimated grasp position with recorded pad path; plausible few-pixel camera/pose uncertainty, explicitly a scene fit not a measurement. Robot model, control and trajectory unchanged.

- 2026-09-17T18:27:34.055038+00:00 Iteration4 FAILED: shifted objects still pushed rather than lifted; bowl additionally displaced about18mm, visually worse. Max penetration0.513mm. Iteration5 (last allowed): restore iteration2 geometry/poses/native grip contact response; stiffen only explicit marker-bowl contact pairs to reduce support penetration without changing pad contacts. Disable cast shadows for closer diffuse real lighting. Recorded trajectory and robot controller remain unchanged. Will retain best visually verified outcome and document physical sensitivity.

- 2026-09-17T18:29:37.100209+00:00 Iteration5 FAILED despite restoring iteration2 poses/native grip: stiffer bowl contacts prevent successful capture; max penetration0.721mm,11 contact frames, marker remains in bowl. Five-iteration limit reached. Visually reviewed every iteration. Selected iteration2 as best qualitative outcome; copied its existing outputs and exact scene snapshots to artifacts/final and root. No sixth physics run. Report explicitly notes success sensitivity to soft contacts, up-to4.23mm interpenetration, grasp rotation, imperfect cameras. Final links sim_ext1.mp4 and side_by_side.mp4 created. Dense real/sim contact sheets produced for additional review.

## Follow-up request: keep failures visible; explain method and SysID
- User asked to keep showing failed simulation videos. Linked all four failures directly and created VIDEOS.html with failures first, separate standalone sim and real|sim links, and clear PASS/FAIL labels. No failed run was removed or relabeled.
- User asked for the current input/method, a short video, continued improvement and SysID status. Answered immediately: real-to-sim from three RLDS image streams, 181 recorded joint/gripper observations and language; Menagerie robot, estimated cameras, primitive collision scene and position-control replay. No physical SysID had been performed.
- Execution permissions were updated to unrestricted; subsequent shell/image checks no longer need sandbox escalation. Subscription change itself was not inspected or used as evidence about model capability.
- Ran make_explainer.py: generated pipeline_explainer.mp4, 42 seconds, 1280x720, 15fps, silent captions, seven chapters, using only local artifacts. Clearly labels illustrative episode playback at ~2x. Includes all four failures and physical-SysID limitations. Viewed chapter stills for layout and readability.
- Ran measure_replay.py (offline, no physics): fitted first-order per-joint command-response surrogate using first120 samples for training and final60 transitions held out. Lag chosen from0/1/2 using training data. Held-out RMSE0.00460–0.01218rad, better than hold-state baseline; these are one-step surrogate coefficients, not identified MuJoCo gains or physical parameters. No application to controller/scene.
- Added teal-cap image tracking for real/sim ext1;168/181 jointly detected frames. Mean7.823px, transport13.430px, final2.762px. Reviewed sampled detections. Missing detections kept missing. Static-bias correction diagnostic leaves10.626px mean transport error; no image warp applied.
- Wrote SYSID.md and report addendum describing identifiability limits and next useful work. Original five-scene-iteration cap retained. No sixth physics run, no trajectory edit and no new downloads.
- Final scene regeneration was byte-identical to retained iteration2. Python sources compile; model has8 actuators; all five sets of videos and final symlinks exist. Sample33file MD5 verification, budget and identical recorded joint targets in all five iterations passed. Final success.py passes while report explicitly states contact sensitivity and physical-fidelity failures.

- 2026-09-17T18:42:03.799524+00:00 Local Git repository is initialized, but no commit was made: git var GIT_AUTHOR_IDENT reports no configured author name/email. Kept all deliverables in place without inventing a user identity or asking a nonessential question.

## Repository organization and GitHub publication
- User authorized organizing the code and pushing droid2sim with GIFs to their GitHub. Authenticated account: TheShiningVampire (Vinit Awale). Use a private repository by default. Preserve all five existing scene runs and the recorded trajectory.
- Developer-tool download command: uv pip install --python .venv/bin/python ruff; formatter only, no simulation dependency changes. This small download remains within the original 1 GB software allowance.

- Reorganized active code into droid2sim/{data,simulation,visualization,evaluation}, with shared immutable trajectory loading and a module CLI; retained root compatibility wrappers. Supporting tools moved under scripts/, historical one-off tools under archive/. Added architecture documentation, upstream notices and model licenses.
- Generated docs/media/iteration-{1..5}.gif from existing videos with local ffmpeg: each 121 frames, 12.1 seconds, 640 pixels wide, 10 fps. Viewed start/grasp/end samples of every GIF. All four failures stay visible alongside the retained iteration2 result. Included the comparison/simulation MP4s and captioned explainer in Git.
- Verification: six unittest regressions pass; ruff lint/format and compile checks pass; regenerated scene/robot XML byte-identical; all six rebuilt overlays pixel-identical. Full audit verified 33 dataset-file MD5s, five iterations, download allowance, and unchanged recorded targets. No additional physics simulation or dataset download.
- Publish using verified GitHub account name Vinit Awale and account-specific GitHub noreply email as repository-local Git identity. Exclude data/, vendor/, .venv/ and NumPy arrays while keeping package data modules. Private GitHub repository requested through authenticated gh; publication result recorded below after verification.
