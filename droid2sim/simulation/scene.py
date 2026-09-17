"""Generate the recorded experiment's table, bowl, marker and cameras."""

import json
import xml.etree.ElementTree as ET
import math
import numpy as np
from scipy.spatial.transform import Rotation
from droid2sim.paths import ROOT


def fmt(v):
    return " ".join(f"{float(x):.9g}" for x in v)


def build():
    config = json.load(open(ROOT / "scene_parameters.json"))
    cameras = json.load(open(ROOT / "cameras.json"))
    scene = ET.parse(ROOT / "robot.xml").getroot()
    world = scene.find("worldbody")
    asset = scene.find("asset")
    v = ET.SubElement(scene, "visual")
    ET.SubElement(v, "global", offwidth="640", offheight="360")
    ET.SubElement(v, "quality", shadowsize="2048")
    ET.SubElement(v, "headlight", ambient=".5 .5 .5", diffuse=".6 .6 .6", specular="0 0 0")
    ET.SubElement(world, "light", pos=".4 -.1 2", dir="0 0 -1", diffuse=".65 .65 .65")
    ET.SubElement(
        world,
        "geom",
        name="floor",
        type="plane",
        size="3 3 .1",
        pos="0 0 -.85",
        rgba=".12 .13 .14 1",
    )
    for name, camera in cameras.items():
        camera_to_world = np.array(camera["cam_to_world"])
        rotation = camera_to_world[:3, :3] @ np.diag([1, -1, -1])
        quaternion = Rotation.from_matrix(rotation).as_quat()
        intrinsics = np.array(camera["K"])
        width = camera["width"]
        height = camera["height"]
        # focalpixel/principalpixel use optical offsets from center; sign verified by rendered landmark projection.
        ET.SubElement(
            world,
            "camera",
            name=name,
            pos=fmt(camera_to_world[:3, 3]),
            quat=fmt(quaternion[[3, 0, 1, 2]]),
            resolution=f"{width} {height}",
            sensorsize=f"{width} {height}",
            focalpixel=fmt([intrinsics[0, 0], intrinsics[1, 1]]),
            principalpixel=fmt([intrinsics[0, 2] - width / 2, intrinsics[1, 2] - height / 2]),
        )
    table = config["table"]
    body = ET.SubElement(
        world, "body", name="table", pos=fmt([*table["center_xy"], table["top_z"] - 0.015])
    )
    ET.SubElement(
        body,
        "geom",
        name="table_top",
        type="cylinder",
        size=fmt([table["radius"], 0.015]),
        rgba=".92 .92 .9 1",
        friction=fmt(table["friction"]),
    )
    ET.SubElement(body, "geom", type="cylinder", pos="0 0 -.35", size=".035 .35", rgba=".8 .8 .8 1")
    bowl = config["bowl"]
    body = ET.SubElement(
        world, "body", name="bowl", pos=fmt(bowl["position"]), quat=fmt(bowl["quaternion_wxyz"])
    )
    ET.SubElement(body, "freejoint", name="bowl_free")
    ET.SubElement(
        body,
        "geom",
        name="bowl_base",
        type="cylinder",
        pos=fmt([0, 0, bowl["base_thickness"] / 2]),
        size=fmt([bowl["bottom_radius"], bowl["base_thickness"] / 2]),
        mass=str(bowl["mass"] * 0.35),
        rgba=".65 .66 .65 1",
        friction=fmt(bowl["friction"]),
    )
    # Truncated-cone wall as 32 convex wedges; each mesh is one collision element.
    wall_segments = 32
    for i in range(wall_segments):
        start_angle = i * 2 * math.pi / wall_segments
        end_angle = (i + 1) * 2 * math.pi / wall_segments
        vertices = []
        for z, radius in [(0, bowl["bottom_radius"]), (bowl["height"], bowl["top_radius"])]:
            for wall_radius in [radius - bowl["wall_thickness"], radius]:
                for a in [start_angle, end_angle]:
                    vertices.append([wall_radius * math.cos(a), wall_radius * math.sin(a), z])
        name = f"bowl_wall_{i}"
        ET.SubElement(asset, "mesh", name=name, vertex=fmt(np.array(vertices).ravel()))
        ET.SubElement(
            body,
            "geom",
            name=name,
            type="mesh",
            mesh=name,
            mass=str(bowl["mass"] * 0.65 / wall_segments),
            rgba=".68 .69 .68 1",
            friction=fmt(bowl["friction"]),
        )
    pen = config["pen"]
    quaternion = Rotation.from_euler("xyz", pen["euler_xyz"]).as_quat()
    body = ET.SubElement(
        world, "body", name="pen", pos=fmt(pen["position"]), quat=fmt(quaternion[[3, 0, 1, 2]])
    )
    ET.SubElement(body, "freejoint", name="pen_free")
    length = pen["length"]
    radius = pen["radius"]
    cap = pen["cap_length"]
    ET.SubElement(
        body,
        "geom",
        name="pen_barrel",
        type="capsule",
        fromto=fmt([-length / 2 + radius, 0, 0, length / 2 - cap, 0, 0]),
        size=str(radius),
        mass=str(pen["mass"] * 0.72),
        rgba=".12 .14 .15 1",
        friction=fmt(pen["friction"]),
        condim="4",
        solref=".004 1",
    )
    ET.SubElement(
        body,
        "geom",
        name="pen_cap",
        type="capsule",
        fromto=fmt([length / 2 - cap, 0, 0, length / 2 - radius, 0, 0]),
        size=str(radius * 1.04),
        mass=str(pen["mass"] * 0.28),
        rgba=".01 .30 .29 1",
        friction=fmt(pen["friction"]),
        condim="4",
        solref=".004 1",
    )
    for geom in body.findall("geom"):
        if geom.get("name") in ["pen_barrel", "pen_cap"] and pen.get("contact_override"):
            for k, v in pen["contact_override"].items():
                geom.set(k, str(v))
    # Add a light label band purely for appearance; collision remains the opaque barrel/cap.
    ET.SubElement(
        body,
        "geom",
        name="pen_label",
        type="cylinder",
        pos="-.018 0 0",
        quat=".70710678 0 .70710678 0",
        size=fmt([radius * 1.002, 0.018]),
        rgba=".62 .63 .59 1",
        contype="0",
        conaffinity="0",
        mass="0",
    )
    if pen.get("bowl_contact_override"):
        contact = scene.find("contact")
        for pen_geom in ["pen_barrel", "pen_cap"]:
            for bowl_geom in ["bowl_base"] + [f"bowl_wall_{i}" for i in range(wall_segments)]:
                ET.SubElement(
                    contact,
                    "pair",
                    geom1=pen_geom,
                    geom2=bowl_geom,
                    condim="3",
                    friction=".8 .8 .005 .0001 .0001",
                    solimp=".98 .995 .001",
                    solref=".004 1",
                )
    if config.get("disable_shadows", False):
        for light in world.findall("light"):
            light.set("castshadow", "false")
    ET.indent(scene)
    ET.ElementTree(scene).write(ROOT / "scene.xml")


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
