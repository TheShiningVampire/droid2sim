# Sources and third-party notices

DROID images, trajectory metadata and example media originate from the [DROID dataset](https://droid-dataset.github.io/) by Khazatsky et al., *DROID: A Large-Scale In-the-Wild Robot Manipulation Dataset* (2024). The GIFs and videos show a short episode excerpt with attribution; the full dataset is not included. Dataset terms remain those of the upstream release.

`robot.xml`, `scene.xml` and the corresponding archived scene snapshots contain modified MuJoCo Menagerie model definitions, pinned to tree `8161bba264d7fa7c99ca301e91e7fb44737676ad`:

- `franka_emika_panda`: Apache License 2.0, reproduced in `licenses/franka_emika_panda.txt`.
- `robotiq_2f85`: ROS-Industrial BSD license, copyright (c) 2013 ROS-Industrial, reproduced in `licenses/robotiq_2f85.txt`.

Modifications replace the Panda hand with the official articulated Robotiq model, prefix gripper identifiers, set the attachment and integration options, enable robot gravity compensation, and add the reconstructed scene/cameras. Downloaded mesh assets are excluded from this repository and retain upstream licenses. Their source URLs and exact downloaded bytes are recorded in `downloads.json`.

No new license grant is asserted for third-party data or assets by this project.
