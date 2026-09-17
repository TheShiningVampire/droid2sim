"""Replay fixed recorded targets under native Menagerie position control."""

import argparse
from contextlib import ExitStack
import json
import os
from pathlib import Path
import shutil

os.environ.setdefault("MUJOCO_GL", "egl")

import imageio.v2 as imageio
import mujoco
import numpy as np
from PIL import Image

from droid2sim.paths import DEFAULT_OUTPUT, ROOT, resolve_output
from droid2sim.trajectory import load_trajectory

CAMERAS = ("ext1", "ext2")
FPS = 15


def contact_names(model, contact):
    """Return explicit geom names; some Menagerie linkage geoms are unnamed."""
    return [model.geom(int(contact.geom[index])).name or "" for index in (0, 1)]


def touches_marker(names):
    return any(name.startswith("pen_") for name in names)


def frame_state(data, frame, target, contacts):
    return {
        "frame": frame,
        "time": float(data.time),
        "pen_position": data.body("pen").xpos.copy().tolist(),
        "pen_quat": data.body("pen").xquat.copy().tolist(),
        "bowl_position": data.body("bowl").xpos.copy().tolist(),
        "q_actual": data.qpos[:7].copy().tolist(),
        "q_target": target.tolist(),
        "contacts": contacts,
    }


def run(out: str | Path = DEFAULT_OUTPUT):
    """Render a complete replay. No scene fitting or trajectory edits occur here."""
    output = resolve_output(out)
    output.mkdir(parents=True, exist_ok=True)
    trajectory = load_trajectory()
    model = mujoco.MjModel.from_xml_path(str(ROOT / "scene.xml"))
    data = mujoco.MjData(model)
    data.qpos[:7] = trajectory.joints[0]
    data.ctrl[:7] = trajectory.joints[0]
    data.ctrl[7] = trajectory.gripper[0] * 255
    mujoco.mj_forward(model, data)

    option = mujoco.MjvOption()
    option.geomgroup[3] = 0  # Hide duplicate collision meshes, not their physics.
    keyframes = {0: "start", len(trajectory.time) // 2: "mid", len(trajectory.time) - 1: "end"}
    frames = {camera: [] for camera in CAMERAS}
    history = []
    min_distance = 0.0
    worst_contact = None
    contact_substeps = 0
    max_force = 0.0
    grasp_contact_frames = 0

    with ExitStack() as resources:
        renderer = mujoco.Renderer(model, height=180, width=320)
        resources.callback(renderer.close)
        writers = {}
        for camera in CAMERAS:
            writer = imageio.get_writer(output / f"sim_{camera}.mp4", fps=FPS, macro_block_size=1)
            resources.callback(writer.close)
            writers[camera] = writer

        for frame, target_time in enumerate(trajectory.time):
            # The interpolation, timestep, actuator scaling and ordering match
            # the original experiment. Refactoring does not change its physics.
            while data.time < target_time - 1e-9:
                time = min(data.time, trajectory.time[-1])
                joints, closure = trajectory.sample(time)
                data.ctrl[:7] = joints
                data.ctrl[7] = 255 * closure
                mujoco.mj_step(model, data)
                for contact in data.contact:
                    names = contact_names(model, contact)
                    if not touches_marker(names):
                        continue
                    contact_substeps += 1
                    if float(contact.dist) < min_distance:
                        min_distance = float(contact.dist)
                        worst_contact = {
                            "time": float(data.time),
                            "distance_m": min_distance,
                            "geoms": names,
                            "bodies": [
                                model.body(model.geom_bodyid[contact.geom[index]]).name
                                for index in (0, 1)
                            ],
                        }

            marker_contacts = []
            for index, contact in enumerate(data.contact):
                names = contact_names(model, contact)
                if touches_marker(names):
                    force = np.zeros(6)
                    mujoco.mj_contactForce(model, data, index, force)
                    max_force = max(max_force, float(np.linalg.norm(force[:3])))
                    marker_contacts.append(names)
            grasp_contact_frames += int(
                any(any(name.startswith("rq_") for name in pair) for pair in marker_contacts)
            )
            history.append(frame_state(data, frame, trajectory.joints[frame], marker_contacts))

            for camera, writer in writers.items():
                renderer.update_scene(data, camera=camera, scene_option=option)
                image = renderer.render().copy()
                writer.append_data(image)
                frames[camera].append(image)
                if frame in keyframes:
                    Image.fromarray(image).save(output / f"{camera}_{keyframes[frame]}.png")

    for camera, images in frames.items():
        np.save(output / f"sim_{camera}.npy", np.array(images))
    poses = {
        name: {
            "position": data.body(name).xpos.tolist(),
            "quaternion_wxyz": data.body(name).xquat.tolist(),
        }
        for name in ("pen", "bowl")
    }
    joint_error = np.array([frame["q_actual"] for frame in history]) - trajectory.joints
    pen_dofs = model.jnt_dofadr[model.joint("pen_free").id]
    summary = {
        "final_poses": poses,
        "trajectory_sha256": trajectory.sha256,
        "position_control": "linear interpolation between original observations at their fixed 15 Hz timestamps; unchanged samples; native Menagerie actuators",
        "joint_rmse_rad": float(np.sqrt(np.mean(joint_error**2))),
        "joint_max_error_rad": float(abs(joint_error).max()),
        "min_pen_contact_distance_m": min_distance,
        "worst_pen_contact": worst_contact,
        "pen_contact_substeps": contact_substeps,
        "frames_with_pen_gripper_contact": grasp_contact_frames,
        "max_sampled_pen_contact_force_n": max_force,
        "pen_max_z": float(max(frame["pen_position"][2] for frame in history)),
        "pen_final_velocity": data.qvel[pen_dofs : pen_dofs + 6].tolist(),
        "finite": bool(np.isfinite(data.qpos).all()),
        "mujoco_warning_counts": data.warning.number.tolist(),
    }
    (output / "state.json").write_text(json.dumps(summary, indent=2))
    (output / "history.json").write_text(json.dumps(history, indent=2))
    for filename in ("scene.xml", "scene_parameters.json", "cameras.json"):
        shutil.copy(ROOT / filename, output / filename)
    print(json.dumps(summary, indent=2), flush=True)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", default="artifacts/final", help="Output directory relative to the repo"
    )
    args = parser.parse_args(argv)
    run(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
