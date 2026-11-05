---
doc_id: LKL-DDR-004
title: LeakListen concept selection
project: LeakListen
doc_type: Design decision record
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: Concept selection proposed in the kit 1.9.1 upgrade; awaiting Amish
---

# 0004: Concept selection

- **Date:** 2026-11-01
- **Status:** Proposed, awaiting Amish. Nothing in this record has been decided.

## Context

Kit 1.8 asks every design to compare at least two working principles before it commits (STANDARDS section 21). LeakListen was designed before that rule, so the existing design (a magnet-on contact sensor on a valve spindle cap) is option A and does not change without Amish's go. Two more options with different working principles were added and scored against the user requirements (LKL-URS-001) in LKL-OPT-001, and their STEM checks are in LKL-STM-001. Each option is modelled to detail level D3 in `cad/src/model.py` ("Detail every option", Amish, 2026-10-24).

## Options considered

1. **Option A, magnet-on contact sensor.** Score 155 of 205. Light (0.96 kg for logger, cable and sensor), placed from the surface, touches no water, USD 142 in parts (priced). Hears about 185 m along iron mains but about 4 m along PVC; the radio is at risk under an iron cover.
2. **Option B, hydrant cap hydrophone.** Score 127. Hears the leak noise in the water column on any pipe material (54 m on PVC at an assumed background). Sits in drinking water, weighs 6.0 kg in the model, has an unpriced stainless cap and an assumed cap interface.
3. **Option C, ground spike geophone.** Score 123. No access to the pipe needed and a plastic lid over the antenna, but the leak is heard only a few metres from the spike and the ground box weighs 15.3 kg.

## Decision

**Proposed, awaiting Amish:** keep option A as the product, and keep option B as the plastic-main variant (the hydrophone variant that LKL-DDR-002 D8 already names), not as a replacement. Option A leads B by 18 %, outside the 10 % band that would send two options to Amish without a pick. Alternatives for Amish: (a) choose option B as the single product, which has the stronger acoustics and gives up the weight, price and water-contact advantages of A; (b) choose option C, which the first-order numbers do not support. `concept_chosen` in `project.yaml` reads "A (proposed)" until he decides.

## Consequences

- If Amish agrees, the precis (LKL-PRC-001), the product requirements (LKL-PRS-001), the calculation note (LKL-CAL-001), the drawing (LKL-DWG-001), the BOM and the build plan stay as they are: they already describe option A.
- Option B would need its own sizing (LKL-CAL-001 does not size the hydrophone variant; PR-002 stays open), a hydrant outlet survey and a water-contact approval route before it is priced.
- If he chooses B, the cap interface is redesigned for the partner's hydrant outlet type (LKL-STM-001 SB4).
