---
doc_id: LKL-DDR-001
title: LeakListen TRL 2 review decisions
project: LeakListen
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002): D1 to D6 decided; O1 and O2 still open"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for D1 to D6. On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos", so D1 to D6 are "Decided by Amish, 2026-09-25: go with recommendation" (see LKL-DDR-002). Items O1 and O2 had no recommendation and remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish". On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Items without a recommendation stay open. Version 0.1 of this record contained no decision made by Amish; version 0.2 records his acceptance of D1 to D6 on 2026-09-25.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in LKL-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items decided.*

| # | Item | Recommendation (now the decision) | Status |
| --- | --- | --- | --- |
| D1 | Screening versus correlation (pitch-level) | Option A: nightly noise-level screening only. Time-synchronized correlation between loggers (option B) is recorded as a later variant. | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Radio from under covers | Option A: flat antenna under the cover, with the TRL 3 link budget deciding whether a through-cover antenna (B) or a nearby gateway (C) is needed. LKL-CAL-001 section D finds that it is needed under iron covers; the response is decided in LKL-DDR-002. | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Sensor type | Piezo disc with a charge amplifier, with a hydrophone on hydrants kept as an option for plastic networks. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Reuse of the FieldNode radio core | Yes: the STM32WL module and payload conventions are shared with FieldNode; FieldNode's solar power is not used. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Primary cell size | C size, about 7.7 Ah. | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Privacy rule | Raw samples never leave the device; R8 is kept as a fixed requirement. | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner utility and region for co-design and a pilot district. No recommendation was made. | Proposed, awaiting Amish |
| O2 | Whether a vibration calibration check belongs in LeakListen or in CalRig (CalRig covers temperature, humidity and particles only). No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: unchanged apart from the TRL fields. No new budget, pitch or problem wording was recommended, so `budget_usd` stays at $130 and the pitch and problem lines are unchanged.
- LKL-PRB-001, LKL-PRC-001 and LKL-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed". R8 is marked as a fixed requirement (D6). No requirement target is relaxed or redefined by these decisions.
- D4 aligns the radio with FieldNode (FND-CAL-001): +14 dBm in EU868 and the same link budget method. LKL-CAL-001 found that the TRL 2 assumption of +20 dBm is not permitted in EU868; the design now uses +14 dBm there and up to +20 dBm in US915.
- The TRL 3 calculations (LKL-CAL-001) led to four design changes within these decisions: a 53 g seismic mass in a 42 mm tall puck, a 24-byte summary, regional transmit power and a weekly network time correction. They add $1 to the parts cost, now $109.00.
- LKL-CAL-001 v0.1 showed R2 and R7 not met and R1, R3, R4 and R9 at risk. The responses (radio option, scope for plastic mains, a larger magnet) were decided by Amish on 2026-09-25 and are recorded in LKL-DDR-002.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
