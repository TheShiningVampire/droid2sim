# Episode screening

Decoded all 100 episodes locally. The actual RLDS schema is in `sources/actual_schema.txt`; the complete index, language labels and original paths are in `artifacts/episodes.json`. Twenty-seven episodes had a nonempty instruction, a success path, and 120–375 samples (8–25 seconds at DROID's documented 15 Hz). Every episode has a start/mid/end sheet for both exterior cameras in `artifacts/candidates/`.

Top five, with saved sheets in `artifacts/top5/`:

| Index | Instruction | Duration | Decision |
|---|---|---:|---|
| **6** | Take the pen out of the bowl and place it on the table | **12.07 s** | **Final selection.** Opaque black/teal plastic marker, successful pick and place, clear circular tabletop; marker visible inside bowl in both starting views. Bowl is modeled as a separate support/contact body. The raw release is absent, so camera/geometry estimation is necessary. |
| 74 | Move the yellow mug forward | 11.13 s | Initially preferred for large object visibility. Rejected after HD wrist video revealed a glossy ceramic surface. Its 13.49 MB of raw data is retained and included in the download ledger. |
| 4 | Move the sharpie to the table | 14.20 s | Marker is largely hidden inside a mug at the start, especially exterior 1; weak initial visibility. |
| 60 | Put the green block in the bowl | 9.60 s | Simple block but absent from the initial exterior-1 image; violates visibility criterion. |
| 20 | Slide the black lid off | 12.60 s | Lid/container contact and ambiguous target outcome; less suitable than the marker episode. |

Other candidates were rejected for cloth/dusters, flexible packaging, appliances, reflective pans/pots, transparent cups, clutter or unsuitable action types. No episodes were trimmed to meet the duration requirement.

The final target is an opaque marker, not a metal or transparent pen. Small highlights on plastic and on the support bowl remain; non-reflective here means no mirror-like/transparent target surface. Exact material cannot be proven from 320×180 images.

## Raw-release checks

Final path: `IRIS/success/2023-05-04/Thu_May__4_13:41:33_2023`.

Exact-prefix public GCS listings returned no files under `robotics/droid_raw/1.0.1/`, `1.0.0/`, and the unversioned prefix. Saved responses are `sources/raw_pen_listing*.json`. The episode also has no path/ID entry in the published calibration release. No credentials were required. This activates the requested RLDS fallback; stereo depth and HD frames are unavailable for the final episode.

The raw-only-for-final-episode ideal was not fully met: one provisionally selected episode was downloaded and then rejected because HD evidence contradicted the sample-resolution material assessment. No other candidate raw recordings were fetched.
