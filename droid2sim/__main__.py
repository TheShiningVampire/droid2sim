"""Run a pipeline stage: python -m droid2sim <command> [arguments]."""

import argparse
from importlib import import_module

COMMANDS = {
    "assemble": "simulation.robot",
    "build": "simulation.scene",
    "replay": "simulation.replay",
    "compare": "visualization.compare",
    "check": "evaluation.success",
    "validate": "evaluation.validate",
    "download": "data.download",
    "extract": "data.extract",
}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=COMMANDS)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    module = import_module(f"droid2sim.{COMMANDS[args.command]}")
    return module.main(args.arguments)


if __name__ == "__main__":
    raise SystemExit(main())
