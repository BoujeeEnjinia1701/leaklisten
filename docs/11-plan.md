---
doc_id: LKL-PLN-001
title: LeakListen project plan
project: LeakListen
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: First plan at stage P3 (kit 1.9.1 upgrade); P4 to P6 shown as planned work on hold
---

# LeakListen project plan

LeakListen is at stage P3 (design outputs), TRL 3. The calculation note, the D3 model of all three options, the drawing, the priced BOM and the build plan exist. The next gate, P4 (verification, TRL 4), is on hold while the portfolio stage cap is P3. The decision requested is the concept choice (LKL-DDR-004). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept choice | Amish Chadha | LKL-DEC-001 D10, LKL-DDR-004 | Proposed, awaiting Amish |
| Partner and site | Amish Chadha | A UK water company with metallic mains and district metered areas (LKL-DEC-001, 2026-10-02) | Not started |
| Requirements | Design lead | LKL-URS-001, LKL-PRS-001, LKL-RTM-001 | Done on paper; partner review pending |
| Calculations and model | Design lead | LKL-CAL-001; D3 model of options A, B and C; STEP and STL | Done 2026-11-01 |
| Drawings, BOM, build plan | Design lead | LKL-DWG-001, DWG-101 to 109, bom/bom.csv, LKL-BLD-001 | Done for option A |
| Risk, market, regulatory | Design lead | LKL-RSK-001 with design FMEA, LKL-MKT-001, LKL-REG-001 | Done 2026-11-01 |
| Renders | Coordinator | Options picture and product renders (Blender, on a Mac) | Queued |
| Verification (P4) | Partner and lab | Cover loss, shaker, noise, cell pulse and magnet pull tests | On hold (stage cap P3) |

## Resources needed

Table 2. Resources.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Design lead (Claude with Amish's review) | P1 to P3 documents | 2 sessions (done) | 0 |
| Prototype parts | One logger set (P4, on hold) | | 142 (bom/bom.csv) |
| Main board design | Board for the STM32WL core (P4, on hold) | To assess | To assess |
| Gateway | A LoRaWAN gateway near the pilot district (the lab's TwinKit) | To assess | To assess |
| Partner site survey | Cover types, neck sizes, pipe materials | 1 to 2 days | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Done 2026-11-01 (written in the kit 1.9.1 upgrade) |
| P1 Definition | URS, PRS draft, RSK, MKT, REG complete | Done 2026-11-01 |
| P2 Design inputs | PRS targets, CAL, RTM, DDR, STEM check closed by calculation | Done 2026-11-01; 13 STEM rows need field data or datasheets |
| P3 Design outputs | Model, STEP, DWG, BOM, BLD, DEC, FMEA | Done 2026-11-01 |
| P4 Verification | Cover loss, resonance and noise measurements, build | On hold |
| P5 to P6 | Field trial with a partner, launch | On hold |

## Next steps and decision requested

Requested: Amish's concept choice (LKL-DDR-004) and his view on the optional seismic mass change (LKL-DEC-001 D12). The recommended next step is a partner and, when the cap allows, TRL 4: the cover loss measurement and a shaker comparison of the sensor.

## References

Ofcom. "IR 2030 UK Interface Requirements 2030." Accessed November 1, 2026. https://www.ofcom.org.uk/__data/assets/pdf_file/0028/84970/ir-2030.pdf.

SubSurface Leak Detection. "SubSurface Enigma 3 Hybrid Logger System." Tiger Supplies. Accessed November 1, 2026. https://tigersupplies.com/products/subsurface-enigma-3-hybrid-logger-system.
