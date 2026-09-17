"""Assemble the official Menagerie Panda and Robotiq 2F-85 without new links."""

import pathlib
import xml.etree.ElementTree as ET
from droid2sim.paths import ROOT


def assemble():
    """Replace the Panda hand with the native articulated Robotiq model."""
    vendor = ROOT / "vendor/mujoco_menagerie"
    panda = ET.parse(vendor / "franka_emika_panda/panda.xml").getroot()
    gripper = ET.parse(vendor / "robotiq_2f85/2f85.xml").getroot()
    # Prefix every gripper name/reference to avoid default class and asset collisions.
    refs = {
        "name",
        "class",
        "childclass",
        "mesh",
        "material",
        "joint",
        "joint1",
        "joint2",
        "body1",
        "body2",
        "tendon",
    }
    for element in gripper.iter():
        if element.tag == "mesh" and "file" in element.attrib and "name" not in element.attrib:
            element.set("name", pathlib.Path(element.get("file")).stem)
        for attribute, value in list(element.attrib.items()):
            if attribute in refs:
                element.set(attribute, "rq_" + value)
    for model, folder in [(panda, "franka_emika_panda"), (gripper, "robotiq_2f85")]:
        for element in model.findall("asset/mesh"):
            if "file" in element.attrib:
                element.set(
                    "file",
                    str(
                        pathlib.Path("vendor/mujoco_menagerie")
                        / folder
                        / "assets"
                        / element.get("file")
                    ),
                )
    panda.find("compiler").attrib.pop("meshdir", None)
    for tag in ["tendon", "equality", "keyframe"]:
        panda.remove(panda.find(tag))
    actuators = panda.find("actuator")
    actuators.remove(list(actuators)[-1])
    link7 = panda.find('.//body[@name="link7"]')
    link7.remove(link7.find('body[@name="hand"]'))
    flange = ET.SubElement(
        link7, "body", name="tool_flange", pos="0 0 0.107", quat="0.9238795325 0 0 -0.3826834324"
    )
    ET.SubElement(flange, "site", name="flange_site", size=".003")
    mount = gripper.find("worldbody/body")
    flange.append(mount)
    # End-effector hardware attachment: keep Menagerie native base offset and rotate its grasp axis with Panda hand frame.
    for tag in ["default", "asset", "contact", "tendon", "equality", "actuator"]:
        target = panda.find(tag)
        if target is None:
            target = ET.SubElement(panda, tag)
        source = gripper.find(tag)
        if source is not None:
            for element in list(source):
                target.append(element)
    panda.find("option").set("timestep", "0.001")
    panda.find("option").set("cone", "elliptic")
    panda.find("option").set("impratio", "10")
    # Use Menagerie controls unmodified; gravity compensation approximates DROID torque controller's feedforward.
    for b in panda.findall(".//body"):
        b.set("gravcomp", "1")
    ET.indent(panda)
    ET.ElementTree(panda).write(ROOT / "robot.xml")


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    assemble()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
