# Digital Electronics Roundabout Traffic-Light Controller

<p align="center">
  <a href="https://github.com/lhlizdabezt/DienTuSo/releases/latest"><img src="https://img.shields.io/github/v/release/lhlizdabezt/DienTuSo?style=for-the-badge&logo=github&label=Release" alt="Latest release for DienTuSo" /></a>
  <a href="https://github.com/lhlizdabezt/DienTuSo/tags"><img src="https://img.shields.io/github/v/tag/lhlizdabezt/DienTuSo?style=for-the-badge&logo=git&label=Tag" alt="Latest tag for DienTuSo" /></a>
  <img src="https://img.shields.io/badge/Portfolio-English%20review%20ready-0f766e?style=for-the-badge" alt="English portfolio ready" />
</p>

<p align="center">
  <img src="assets/portfolio-motion.svg" alt="Animated engineering portfolio visual for DienTuSo" width="100%" />
</p>

## Overview

`DienTuSo` documents a digital electronics course project for a roundabout traffic-light controller. The repository presents the controller as a sequential digital-logic artifact with a mod-12 timing cycle, JK flip-flop concepts, state decoding, CircuitJS/Falstad simulation material and Node.js logic checks.

The project is packaged for recruiter and engineering review. It demonstrates logic-design reasoning and simulation discipline, not a field-deployed traffic-control product.

## Repository Status

| Field | Status |
|---|---|
| Repository | [github.com/lhlizdabezt/DienTuSo](https://github.com/lhlizdabezt/DienTuSo) |
| Portfolio category | Digital electronics, sequential logic, traffic-light controller simulation |
| Review status | Portfolio-ready academic project snapshot |
| Latest release | [GitHub Releases](https://github.com/lhlizdabezt/DienTuSo/releases/latest) |
| Version tags | [Repository tags](https://github.com/lhlizdabezt/DienTuSo/tags) |
| Visual policy | English labels, ASCII-safe SVG text, no moving connector-line patterns |
| Simulation dependency | Local CircuitJS/Falstad bundle under `tools/circuitjs-local/` |
| Verification dependency | Node.js for `verify-roundabout-logic.js` |

## Controller Model

| Concept | Evidence in Repository | Engineering Point |
|---|---|---|
| Timing cycle | `tools/circuitjs-local/verify-roundabout-logic.js` | Encodes the 12-state green, yellow and all-red guard sequence |
| Logic simulation | `roundabout_traffic_light_controller_falstad_demo_clean.txt` | Stores a reviewable Falstad/CircuitJS simulation description |
| Stable counter simulation | `roundabout_stable_counter_falstad_url.txt` and `roundabout_traffic_light_controller_falstad_stable_counter.txt` | Preserves a counter-focused simulation path |
| Local demo launcher | `start-circuitjs-demo.cmd` | Opens the curated local CircuitJS demo through Node.js |
| Stable counter launcher | `start-circuitjs-stable-counter.cmd` | Opens the stable counter variant |
| Portfolio visual | `assets/roundabout-motion.gif` | Shows the state cycle without moving connector lines |

## Evidence Highlights

- Mod-12 state cycle with normal green, yellow and all-red guard states.
- JK flip-flop and sequential-logic framing for digital-electronics review.
- Emergency mode and night mode behavior captured in the Node.js verifier.
- Falstad/CircuitJS simulation material kept in text form for reproducible inspection.
- Release-backed SVG, GIF and preview assets for quick portfolio screening.

## Repository Structure

| Path | Purpose |
|---|---|
| `assets/` | README-ready SVG, GIF and PNG visuals |
| `scripts/render_assets.py` | Repeatable renderer for the English motion GIF |
| `tools/circuitjs-local/` | Local CircuitJS/Falstad review bundle and Node.js helper scripts |
| `tools/circuitjs-local/verify-roundabout-logic.js` | Logic verifier for normal, emergency and night modes |
| `roundabout_traffic_light_controller_falstad_demo_clean.txt` | Main simulation text artifact |
| `roundabout_traffic_light_controller_falstad_stable_counter.txt` | Stable counter simulation text artifact |
| `start-circuitjs-demo.cmd` | Windows launcher for the main local simulation |
| `start-circuitjs-stable-counter.cmd` | Windows launcher for the stable counter simulation |

## How to Review

1. Start with this README to understand the project boundary and evidence map.
2. Open the latest release to confirm the preserved review snapshot and visual assets.
3. Run the Node.js verifier to inspect the logical state sequence.
4. Open the CircuitJS/Falstad simulation files or launch the local demo.
5. Review the GIF and SVG assets to see the portfolio-facing explanation.
6. Use the release notes and tags to audit how the repository changed over time.

## Run or Inspect Locally

### Logic Verifier

```powershell
cd tools\circuitjs-local
npm install
node verify-roundabout-logic.js
```

Expected result: the script prints the 12 normal states, checks emergency mode, checks night mode, and ends with an `OK` line when the model passes.

### CircuitJS Demo

From the repository root:

```powershell
.\start-circuitjs-demo.cmd
```

For the stable counter variant:

```powershell
.\start-circuitjs-stable-counter.cmd
```

The local launchers enter `tools/circuitjs-local/` and start the selected simulation through `node start-demo.js`.

## FAQ

| Question | Answer |
|---|---|
| Is this a deployed traffic controller? | No. It is a digital-electronics coursework prototype and portfolio evidence package. |
| What should a reviewer inspect first? | `verify-roundabout-logic.js`, the CircuitJS simulation text files and the release-backed motion GIF. |
| What does the all-red state do? | It acts as a guard state between lane transitions in the 12-state cycle. |
| Why include Node.js in a digital logic repo? | It provides a compact, repeatable logic check for the expected state decoder behavior. |
| Why avoid connector-line animation? | Dense line motion can hide labels in small GitHub cards. The current visual uses card-based state changes instead. |

## Scope and Boundaries

This repository demonstrates logic design, state-machine reasoning, simulation packaging and reviewer-facing documentation. It does not claim road-safety certification, hardware deployment, production timing validation, redundancy design, or field installation.

## Professional Links

| Channel | Link |
|---|---|
| GitHub profile | [github.com/lhlizdabezt](https://github.com/lhlizdabezt) |
| Resume | [Luong Hai Long CV](https://github.com/lhlizdabezt/lhlizdabezt/blob/main/resume/Luong_Hai_Long_CV.pdf) |
| LinkedIn | [linkedin.com/in/lhlizdabezt](https://www.linkedin.com/in/lhlizdabezt) |
| Work email | [luonghailong.work@gmail.com](mailto:luonghailong.work@gmail.com) |
| Student email | [22207056@student.hcmus.edu.vn](mailto:22207056@student.hcmus.edu.vn) |
| Phone | [+84 988 114 708](tel:+84988114708) |
| Facebook | [facebook.com/wageseadrake](https://www.facebook.com/wageseadrake) |
| Instagram | [instagram.com/lhlizdabezt](https://www.instagram.com/lhlizdabezt) |
| YouTube | [youtube.com/@lhlizdabezt](https://www.youtube.com/@lhlizdabezt) |
| TikTok | [tiktok.com/@wageseadrake](https://www.tiktok.com/@wageseadrake) |

## Writing Standard

The README follows an evidence-first style: direct technical nouns, clear academic boundaries, release-backed artifacts, reproducible commands and no inflated claims beyond what the repository can support.
