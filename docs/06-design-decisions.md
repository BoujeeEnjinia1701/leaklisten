---
doc_id: LKL-DEC-001
title: LeakListen design decisions register
project: LeakListen
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions, items to confirm, value engineering and decisions made to date
---

# LeakListen design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction as a whole: the neck bar hanger, flanged end plugs, top plug fittings, internal chassis and puck changes made under Amish's 2026-09-30 instruction | Accept, or ask for changes | Accept | Every component; nothing is bought or made before this is accepted | LKL-DDR-003, P1 to P9 |
| 2 | R12 mass limit: the set is 1.35 kg with the neck bar against 1.0 kg | (a) restate R12 as 1.0 kg for the logger, cable and sensor (0.96 kg) and count the neck bar as site hardware; (b) relax R12 to 1.5 kg in all; (c) look for a lighter hanger (1 mm wall tube saves about 55 g; still over) | (a) | The first check that weighs the set | LKL-DDR-003, A1 |
| 3 | Hanger for necks outside about 570 to 710 mm, or with poor walls | (a) neck bar as modelled, with a longer inner tube for wider necks; (b) a bracket on two concrete screws in the neck wall, with the utility's consent to drill | (a) for the prototype; confirm the pilot district's neck sizes before any deployment | Neck bar tubes and feet | LKL-DDR-003, A2 |
| 4 | First partner utility and region for co-design and a pilot district | Any utility willing to co-design | None yet | Radio band of the antenna and board; the neck sizes of item 3 | LKL-DDR-002, O1 |
| 5 | Whether a vibration calibration check belongs in LeakListen or in CalRig | LeakListen; CalRig | None yet | Not part of the TRL 3 build; needed for the sensor checks at TRL 4 | LKL-DDR-002, O2 |
| 6 | Appearance model and product renders: status light pipe on the top plug, board orientation, cable route and render context (raised 2026-09-26) | Keep or drop each, as listed in the review note | Keep the light pipe as a brief blink at power-up only; accept the other three as appearance only | Top plug (one more hole if the light pipe is kept); the renders are redone on Amish's Mac | `docs/REVIEW.md`, 2026-09-26 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The pot magnet's stud is M6 and can be cut to 6 mm | The puck base is tapped M6 for 6 mm of thread | LKL-DDR-003, P7 |
| 2 | The flat antenna's centre stud size, and that its lead ends in an SMA plug | Sets the bracket's stud hole and the top plug's connector | LKL-DDR-003, P2 and P4 |
| 3 | The SMA bulkhead's panel hole and the M12 socket's thread (M16 x 1.5 assumed) | Sets the holes in the two end plugs | LKL-DDR-003, P4 and P6 |
| 4 | The square tube inserts suit 1.5 mm wall tube and take an M10 levelling foot | The feet wedge the bar | LKL-DDR-003, P1 |
| 5 | The main board fits 38 x 110 mm with its components within 8 mm | The chassis and the tube bore are sized to it | LKL-DDR-003, P5 |
| 6 | The capacitor and cell sizes (16 x 30 mm, C size 26.2 x 50 mm) | The chassis clips are printed to them; the cell clears the bore by 0.8 mm | LKL-DDR-003, P5 |

## Value engineering

Value-engineering target: USD 130 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 141 (USD 11 over the target). Main cost drivers and savings worth trying:

- The largest lines are the main board (USD 30, a prototype price; its design is TRL 4 work), the neck bar hanger (USD 18), the logger housing with its turned plugs (USD 16), the sensor cable (USD 12) and the primary cell (USD 12).
- Making the design constructable added USD 28 to the concept's USD 113: the neck bar (USD 12 more than the strap), the turned plugs, O-rings and screws (USD 4), the internal chassis (USD 4), the eye bolt and SMA bulkhead (USD 7) and the thicker puck (USD 1).
- Savings worth trying: a fixed-length bar cut to each district's neck width, with one foot and no inner tube or pin (about USD 4 and 80 g); plugs turned in batches or moulded later; a main board price that should fall once its design is done; a cable bought by the reel with a field-fit M12 plug.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D6: nightly noise-level screening; flat antenna under the cover; piezo disc sensor with the hydrophone kept for plastic networks; reuse of the FieldNode STM32WL core; C-size cell; raw samples never leave the device | Amish: "i accept all your recommendations, go with them across all repos." | LKL-DDR-001, LKL-DDR-002 |
| 2026-09-25 | D7: measure cover loss first, then a gateway within about 0.5 km of each district with iron covers | Amish, same instruction | LKL-DDR-002 |
| 2026-09-25 | D8: the contact sensor's scope is metallic mains; the hydrophone variant answers plastic mains | Amish, same instruction | LKL-DDR-002 |
| 2026-09-25 | D9: 42 mm pot magnet with a keeper plate | Amish, same instruction | LKL-DDR-002 |
| 2026-10-01 | Budget treated as a value-engineering target, reported as over or under rather than met or not met | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | This register; LKL-CAL-001 v0.3 |
