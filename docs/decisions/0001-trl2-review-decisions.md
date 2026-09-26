---
doc_id: LKL-DDR-001
title: LeakListen TRL 2 review decisions
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
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations for items D1 to D6 are adopted for TRL 3 work, pending Amish's review; items O1 and O2 remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish". On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Items without a recommendation stay open. Nothing in this record is a decision made by Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in LKL-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3.*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| D1 | Screening versus correlation (pitch-level) | Option A: nightly noise-level screening only. Time-synchronized correlation between loggers (option B) is recorded as a later variant. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D2 | Radio from under covers | Option A: flat antenna under the cover, with the TRL 3 link budget deciding whether a through-cover antenna (B) or a nearby gateway (C) is needed. LKL-CAL-001 section D finds that it is needed under iron covers; the choice is a new item in `docs/REVIEW.md`. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D3 | Sensor type | Piezo disc with a charge amplifier, with a hydrophone on hydrants kept as an option for plastic networks. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D4 | Reuse of the FieldNode radio core | Yes: the STM32WL module and payload conventions are shared with FieldNode; FieldNode's solar power is not used. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D5 | Primary cell size | C size, about 7.7 Ah. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D6 | Privacy rule | Raw samples never leave the device; R8 is kept as a fixed requirement. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |

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
- LKL-CAL-001 shows R2 and R7 not met and R1, R3, R4 and R9 at risk. The responses (radio option, scope for plastic mains, a larger magnet) are proposed in `docs/REVIEW.md` and await Amish; this record does not decide them.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
