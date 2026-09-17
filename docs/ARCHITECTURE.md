# Reading the pipeline

The main path is:

```text
selected RLDS episode → immutable trajectory + real frames
                                ↓
Menagerie assets → robot.xml → scene.xml + estimated cameras
                                ↓
                     position-controlled replay
                                ↓
                 rendered frames + state history
                          ↙             ↘
                   comparison       task predicate
```

Start with `droid2sim/__main__.py` for the CLI, then read:

1. `data/extract.py`: selects the exact saved episode path and exports recorded observations, frames and a checksum.
2. `trajectory.py`: verifies that checksum, makes arrays read-only, and interpolates between recorded observations.
3. `simulation/robot.py` and `simulation/scene.py`: assemble the two official robot models and generate table, bowl, marker and cameras.
4. `simulation/replay.py`: position control, physics stepping, rendering and contact diagnostics. No parameter fitting happens here.
5. `evaluation/success.py`: a pure `evaluate(state, scene)` function plus a CLI. A pass is task-level success, not physical validation.
6. `visualization/compare.py`: real/sim videos and overlays from existing image arrays.

`paths.py` keeps paths relative to the repository rather than the shell directory. The root `replay.py`, `success.py`, `compare.py`, `build_scene.py`, `download.py` and `validate.py` files are small compatibility entry points.

Supporting scripts are grouped by stage under `scripts/`; abandoned one-off workflows are under `archive/`. Inputs and fitted parameters remain at the root so experiment snapshots and historical reports retain their paths. `artifacts/iteration1` through `iteration5` are immutable experimental results; `artifacts/final` is the retained iteration-2 result.

The refactor is behavior-preserving: robot/scene generation is byte-identical, interpolation matches the original replay, and archived success/failure checks produce exactly the original results. No additional physics iteration was run during reorganization.
