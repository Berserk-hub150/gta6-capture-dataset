# Capture Dataset

Extract labelled image frames from GTA VI recordings with source hashes and timestamps in JSON Lines.

## Quick start

Install FFmpeg and Python 3.11+, then run:

```sh
python extract.py demo/clip.mp4 demo/labels.csv output --fps 2
```

## Using your own material

Label intervals are [start,end) in seconds. Gaps yield null labels, overlaps fail validation. Clip SHA-256 lets you group frames by recording. RGB frames come from ordinary exported videos. Engine depth, segmentation and game telemetry require separate ground truth.

Independent fan project. Grand Theft Auto is a trademark of its respective owners.
