---
doc_id: LKL-FEA-001
title: LeakListen feasibility assessment
project: LeakListen
doc_type: Feasibility
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: First feasibility assessment at TRL 3, from LKL-CAL-001 v0.6 and LKL-STM-001 v0.1
---

# LeakListen feasibility assessment

**Feasible on paper for option A on metallic mains, with two weak points.** The calculations (LKL-CAL-001) show the logger runs 10 years on one cell, fits its housing and weight limits and reports a 24-byte summary a night; the reach on iron (185 m) clears the 100 m target at the central estimate; the radio under an iron cover and the sensor's mounted resonance and noise are at risk and need hardware at TRL 4, which is on hold. Plastic mains are not feasible with the contact sensor (4 m); the hydrophone variant (option B) is plausible on a first-order screen but is not sized. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | A 63 x 240 mm sealed logger and a 40 mm sensor puck, 0.96 kg; 185 m on iron; 10 years on one cell; 125 N magnet hold | Medium | Reach, resonance (676 to 1,352 Hz in band) and noise (1.03 µg/√Hz) are at risk on assumed data; plastic mains need option B | LKL-STM-001 S1 to S6; LKL-CAL-001 F, G |
| Materials | PVC pipe, acetal plugs, printed PETG, 316 and A2 fasteners, aluminium neck bar, brass mass, nitrile O-rings | High | All common; option B adds 316 stainless plate and water-contact approvals | LKL-REG-001 G4; bom/bom.csv |
| Manufacturing and assembly | Turned plugs and puck, cut tube, printed chassis, a board of the lab's own design; 13 BOM lines | Medium | The main board is not designed (TRL 4 work); turned parts need a machinist | bom/bom.csv; LKL-BLD-001 |
| Power and controls | Primary Li-SOCl2 C cell, 1.25 mAh a day, STM32WL, fixed-point spectrum in 64 kB | High | Cell passivation at the first pulse (STM S9); firmware beyond a sketch is TRL 4 work | LKL-CAL-001 A, C; LKL-STM-001 S7 to S9 |
| Supply of parts | All parts catalogue or turned; USD 142 in parts against a USD 130 target | Medium | USD 12 over the value-engineering target; prices indicative | bom/bom.csv; LKL-MKT-001 |
| Site | Metallic mains with district metering and a gateway within 0.5 km | Medium | Cover loss unmeasured; partner not yet approached; option B needs hydrants with an open valve | LKL-STM-001 S10; LKL-RSK-001 P1, P2 |

Ratings: High, Medium, Low.
