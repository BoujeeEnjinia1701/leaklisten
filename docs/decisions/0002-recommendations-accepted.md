---
doc_id: LKL-DDR-002
title: LeakListen recommendations accepted
project: LeakListen
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below marked "Decided by Amish, 2026-09-25: go with recommendation" is a decision by Amish. Items without a recommendation stay "Proposed, awaiting Amish".

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Before that, LeakListen carried two groups of items: D1 to D6 in LKL-DDR-001, adopted as recommended for TRL 3 and open for his review, and three new items raised by the TRL 3 calculations in `docs/REVIEW.md` (radio under iron covers, plastic mains, a larger magnet), each with a recommendation. Two items (O1, O2) never had a recommendation. TRL 4 remains on hold by Amish's instruction, so any part of a decision that needs a build, test, measurement or trial is recorded as decided but on hold.

## Options considered

The options for D1 to D6 are in LKL-DDR-001 and the TRL 2 section of `docs/REVIEW.md`. The options for D7 to D9 are in the TRL 3 section of `docs/REVIEW.md` ("Still awaiting Amish", items 3 to 5) and in LKL-CAL-001 v0.1, sections D, G and I.

## Decision

*Table 1. Items decided by Amish on 2026-09-25.*

| # | Item | Decision (the recommendation) | Status | What changed in the repo |
| --- | --- | --- | --- | --- |
| D1 | Screening versus correlation | Nightly noise-level screening; correlation is a later variant | Decided by Amish, 2026-09-25: go with recommendation | Already reflected at TRL 3; LKL-DDR-001 v0.2 status wording |
| D2 | Radio from under covers | Flat antenna under the cover, with the link budget deciding whether more is needed | Decided by Amish, 2026-09-25: go with recommendation | Already reflected; the link budget's answer is D7 |
| D3 | Sensor type | Piezo disc with a charge amplifier; hydrophone kept for plastic networks | Decided by Amish, 2026-09-25: go with recommendation | Already reflected; D8 gives the hydrophone variant its requirement |
| D4 | FieldNode radio core | Reuse the STM32WL core and payload conventions, without FieldNode's solar power | Decided by Amish, 2026-09-25: go with recommendation | Already reflected; no FieldNode change needed |
| D5 | Primary cell size | C size, about 7.7 Ah | Decided by Amish, 2026-09-25: go with recommendation | Already reflected |
| D6 | Privacy rule | Raw samples never leave the device; R8 fixed | Decided by Amish, 2026-09-25: go with recommendation | Already reflected |
| D7 | Radio under iron covers (R7) | Measure cover loss first; then plan a gateway within about 0.5 km of each district with iron covers as the default, with a through-cover antenna or composite cover where a utility agrees | Decided by Amish, 2026-09-25: go with recommendation. The cover loss measurement is TRL 4 work and on hold | R7 restated in LKL-REQ-001 v0.4 against a gateway within 0.5 km under iron covers (1 km where a composite cover or through-cover antenna is agreed); LKL-CAL-001 v0.2 adds the 0.5 km margin [D5]: +0.9 dB EU868 SF12, -1.2 dB US915 SF9. R7 moves from not met to at risk. Gateway density raised with TwinKit as a cross-repo action |
| D8 | Plastic mains (R2) | Restate the contact sensor's scope as metallic mains; the hydrophone variant (D3) is the answer for plastic networks | Decided by Amish, 2026-09-25: go with recommendation. Sizing the hydrophone variant is later TRL 3 work, not done here | R1 and R2 restated in LKL-REQ-001 v0.4; R2 moves from not met to open (variant not sized). Pitch and problem lines unchanged, since hydrophones also mount on existing fittings |
| D9 | Magnet (R9) | Fit a 42 mm pot magnet, about 600 N rated, with a keeper plate | Decided by Amish, 2026-09-25: go with recommendation | `cad/src/model.py` magnet 32 to 42 mm; STEP and STL re-exported; `bom/bom.csv` line 2 $5 to $9, total $109.00 to $113.00; LKL-DWG-001 Rev P1 to P2; LKL-CAL-001 v0.2: hold at a 0.5 mm coating 60 N to 125 N (R9 at risk to met on paper), mounted resonance 776 to 1,553 Hz to 695 to 1,389 Hz, mass 0.93 to 0.98 kg; LKL-PRC-001 v0.4 and media re-rendered |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner utility and region for co-design and a pilot district. No recommendation was made. | Proposed, awaiting Amish |
| O2 | Whether a vibration calibration check belongs in LeakListen or in CalRig. No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: no budget, pitch or problem change was recommended. `budget_usd` stays at $130; parts cost is now $113.00, a margin of $17.00. `trl` and `trl_target` stay at 3.
- Requirement status (LKL-CAL-001 v0.2): none not met (was 2), 4 at risk (R1, R3, R4, R7), 1 open (R2), 2 not verifiable at TRL 3 (R10, R13), 5 met on paper (R5, R6, R9, R12, R15) and 3 met by design (R8, R11, R14).
- R3 gets slightly worse with the heavier magnet (flat to about 376 to 752 Hz instead of 420 to 840 Hz), and R12 keeps only 20 g of margin.
- Documents revised: LKL-PRB-001 v0.4, LKL-PRC-001 v0.4, LKL-REQ-001 v0.4, LKL-CAL-001 v0.2, LKL-DDR-001 v0.2, LKL-DWG-001 Rev P2.
- Cross-repo action: TwinKit's gateway sizing should allow for about 0.5 km spacing in districts with cast-iron covers. Recorded in `docs/REVIEW.md`; TwinKit is not edited here.
- On hold (TRL 4): measuring cover loss through cast-iron and composite covers, and any field check of the link. Nothing in this record authorizes building, testing or purchasing.
