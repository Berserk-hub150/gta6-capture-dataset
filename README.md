# GTA VI Capture Dataset

**Turn a driving clip into labelled training frames.** Each exported image keeps its capture time, interval label and source-video hash, so you can trace it back to the recording.

## From one clip to twelve frames

The [example labels](demo/labels.csv) mark driving from 0–2 seconds and turning from 2–3 seconds. Seconds 3–4 are deliberately unlabelled. Install Python 3.11+ and FFmpeg, then run from the repository root.

```sh
python extract.py demo/clip.mp4 demo/labels.csv output --fps 2
```

Open `output/manifest.jsonl` beside `output/frames/`. The six-second sample yields 12 JPEGs. These three rows show what happens at a boundary.

| Time | Label |
|---:|---|
| 1.5 s | `driving` |
| 2.0 s | `turning` |
| 3.0 s | `null` |

## Label your own footage

Create a CSV with `start,end,label` in seconds. Intervals include the start and exclude the end. Gaps stay unlabelled and overlaps trigger a validation error. Choose a new output directory for each extraction.

The source SHA-256 lets you keep whole clips together when splitting training and evaluation sets. This pipeline extracts RGB frames. Depth maps, segmentation and steering values need their own labels.

---

[Explore the GTA VI project collection](https://github.com/Berserk-hub150/gta6-resource-index) · Independent fan project. Grand Theft Auto is a trademark of its respective owners.
