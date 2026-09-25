# LeakListen

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $130 USD · **Difficulty:** 3 of 5

An acoustic leak sensor that clamps onto water mains and valves and listens overnight for the noise signature of leaks.

## Concept rationale

Continuous, cheap listening finds leaks earlier than periodic surveys.

## Burning platform

Non-revenue water wastes supply and money in water-stressed cities.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab.

## Problem

A large share of treated city water is lost to leaks before it reaches customers, and leaks are found by slow manual surveys.

## Concept

An acoustic leak sensor that clamps onto water mains and valves and listens overnight for the noise signature of leaks.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Contact piezo sensor with magnetic clamp
- Low-noise amplifier
- Microcontroller with overnight recording and spectral analysis
- Battery and LoRa radio
- Valve chamber enclosure

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Valve chambers can be confined spaces; follow confined space entry rules.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (LKL-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `LKL-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
