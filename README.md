# LeakListen

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $130 USD · **Difficulty:** 3 of 5

An acoustic leak sensor that clamps onto water mains and valves and listens overnight for the noise signature of leaks.

![LeakListen concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement LKL-DWG-001 (PDF)](cad/drawings/LKL-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Leaks on pressurized mains make a steady hiss that travels along the pipe wall, and it is easiest to hear at night, when demand and traffic are low. A logger that listens to every valve in a district for a few minutes each night, and flags the ones whose quietest level has risen, turns a slow street-by-street survey into a short list of places to check. LeakListen does this with a magnet-on piezo sensor, a logger that hangs under the chamber cover, one primary cell for years of life and a single small LoRaWAN message a night.

It is open and garage-buildable because the utilities with the highest losses are often the least able to buy and maintain a fleet of closed commercial loggers. The parts are a turned aluminium puck, a piezo disc, a PVC tube, a standard LoRaWAN module and a lithium cell, for about $109 per logger, and the data format is documented so any network server, including the lab's TwinKit gateway, can read it.

## Burning platform

Water utilities lose an estimated 126 billion m³ of treated water a year to leaks and unbilled use, worth nearly $40 billion ([World Bank](https://blogs.worldbank.org/en/ppps/what-do-private-companies-look-performance-based-non-revenue-water-project)). In developing countries alone, about 45 million m³ a day leak from distribution networks, "enough to serve nearly 200 million people" ([Kingdom, Liemberger and Marin, World Bank, 2006](https://documents1.worldbank.org/curated/en/385761468330326484/pdf/394050Reducing1e0water0WSS81PUBLIC1.pdf)).

High-income networks are not immune. The United States still has about 240,000 water main breaks a year, costing about $2.6 billion in repairs ([ASCE 2025 Report Card](https://infrastructurereportcard.org/cat-item/drinking-water-infrastructure/)). Many leaks, though, never break the surface and run until someone listens for them.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal water utilities | Nightly screening of a district metered area, so leak crews go to flagged streets first |
| Small towns and community water schemes | A handful of loggers on the key valves of a small network without a specialist contract |
| Campuses, airports and industrial parks | Leaks on private mains after the utility meter, which the utility does not survey |
| Irrigation districts | Leaks on buried pressurized irrigation pipelines |
| Fire protection networks | Hidden leaks on private fire mains that stay pressurized but rarely flow |
| Research and education | An open logger and dataset for leak noise research and teaching |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | About 240,000 water main breaks a year ([ASCE 2025](https://infrastructurereportcard.org/cat-item/drinking-water-infrastructure/)); many small utilities cannot fund commercial logger fleets. |
| England and Wales | Companies leaked an average of 2,967 million litres a day from April 2022 to March 2025, and all have leakage reduction targets ([Discover Water](https://www.discoverwater.co.uk/leaking-pipes)). |
| Southeast Asia | A study of 47 utilities in Indonesia, Malaysia, Thailand, the Philippines and Vietnam found non-revenue water averaging 30 %, ranging from 4 to 65 % ([Kingdom et al., 2006](https://documents1.worldbank.org/curated/en/385761468330326484/pdf/394050Reducing1e0water0WSS81PUBLIC1.pdf)). |
| Developing countries generally | About 45 million m³ a day lost to leakage ([Kingdom et al., 2006](https://documents1.worldbank.org/curated/en/385761468330326484/pdf/394050Reducing1e0water0WSS81PUBLIC1.pdf)); a low-cost open logger suits utilities starting a leak program. |
| Sub-Saharan Africa | Many networks run intermittent supply. LeakListen only hears leaks on pressurized pipes, so it fits zones with continuous supply, and a pilot there would test that limit. |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. The trigger in the wider world is the ASCE 2025 Report Card's finding that the United States still has about 240,000 main breaks a year ([ASCE](https://infrastructurereportcard.org/cat-item/drinking-water-infrastructure/)), alongside the regulator-set leakage targets that water companies in England and Wales now work to ([Discover Water](https://www.discoverwater.co.uk/leaking-pipes)): even well-funded networks are still finding leaks late.

## Problem

A large share of treated city water is lost to leaks before it reaches customers, and leaks are found by slow manual surveys. Full problem statement: [docs/01-problem.md](docs/01-problem.md).

## Concept

A magnetic piezo sensor clips onto a valve spindle cap and a sealed logger hangs under the chamber cover, placed from the surface with no chamber entry. Each night between 02:00 and 04:00 the logger records twelve 20 s windows, computes levels and a 64-band spectrum from 5 Hz to 2 kHz, deletes the raw samples and sends a 24-byte summary over LoRaWAN. A server (or the lab's TwinKit gateway) flags a logger whose night-time minimum level rises and stays up, and a crew then pinpoints the leak with standard tools.

Estimated performance at TRL 3 ([LKL-CAL-001](docs/04-calcs/01-sizing.md)): about 1.2 mAh a day and 10 years or more on one C-size lithium cell; 0.93 kg; $109.00 in parts. The reference leak (5 L/min at 3 bar) is heard about 185 m along an iron main, with a wide uncertainty. Not met: detection on plastic mains (R2, a few metres with a contact sensor) and the radio link from under a cast-iron cover (R7, about 0.5 km instead of 1 km). At risk: detection on iron (R1), sensor bandwidth (R3) and noise (R4), and magnet hold on coated caps (R9). Install time and the false alarm rate need field work.

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Requirements: [docs/03-requirements.md](docs/03-requirements.md) · Decisions: [docs/decisions/0001-trl2-review-decisions.md](docs/decisions/0001-trl2-review-decisions.md) · Model: [cad/src/model.py](cad/src/model.py)

## Key components

- Aluminium sensor puck with a 32 mm pot magnet, a piezo disc under a 53 g brass mass and a charge preamplifier
- 2 m shielded sensor cable with an M12 IP68 plug
- IP68 PVC logger tube with an STM32WL LoRaWAN board (FieldNode core) and a 24-bit ADC
- Lithium thionyl chloride C cell, primary, about 7.7 Ah
- Stainless hanger that hooks over the cover frame, with a flat LoRa antenna just under the cover

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Valve chambers can be confined spaces with low oxygen or toxic gas; LeakListen is placed from the surface, and nobody should enter a chamber without a confined space permit, gas testing and a trained standby person. Covers are heavy and street work needs traffic management.
>
> The logger uses a lithium thionyl chloride primary cell: never charge it, short it, crush it or heat it, and follow the dangerous goods rules for lithium metal cells. The pot magnet can pinch fingers and affect pacemakers.
>
> Place loggers on a public water network only with the utility's written permission.

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
