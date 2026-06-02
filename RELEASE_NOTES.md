# English GIF Visual Safety Pass - 2026-06-02

## Scope

This release refreshes the `DienTuSo` featured GIF so the profile visual is English-facing, readable and free of moving connector-line patterns.

## Changes

- Rebuilt `assets/roundabout-motion.gif` with English lane, state and cycle labels.
- Removed Vietnamese labels from the featured GIF used by the profile README.
- Removed connector-line, dashed-line, dotted-line and scan-line patterns from the GIF.
- Updated `scripts/render_assets.py` so future generated GIFs remain English and ASCII-safe.
- Replaced truncated SVG chip labels with short English labels.

## Review Context

The updated visual is designed for GitHub README rendering, mobile review and HR or engineering portfolio screening.
