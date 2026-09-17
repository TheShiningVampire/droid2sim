# Supporting workflows

Run these modules from the repository root, for example:

```sh
.venv/bin/python -m scripts.data.fetch_models
```

These are explicit one-shot workflows, not library APIs. Some stages write data or overwrite calibration, so run only the stage you need.

| Directory | Modules | Purpose |
|---|---|---|
| `data/` | `fetch_models`, `fetch_calibration`, `inspect_sample`, `shortlist` | Audited targeted downloads and candidate screening |
| `calibration/` | `annotation_sheet`, `calibrate`, `fit_table` | Image landmarks, camera fitting and table fitting |
| `analysis/` | `measure_replay`, `summarize_sources` | Offline visual/response diagnostics and source accounting |
| `media/` | `make_gifs`, `make_explainer` | GIFs and captioned explainer from existing outputs |

Downloads should run sequentially because they share an audit ledger. The retained camera and scene files are already fitted; calibration is not required to replay the final result. `make_gifs` reads archived MP4s and does not require the dataset, meshes, or a new simulation.
