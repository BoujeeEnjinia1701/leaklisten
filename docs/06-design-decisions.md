---
doc_id: LKL-DEC-001
title: LeakListen design decisions register
project: LeakListen
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions, items to confirm, value engineering and decisions made to date
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all six open decisions on 2026-10-02 (LKL-DDR-003 accepted); moved to decisions made"
---

# LeakListen design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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
| 2026-10-02 | Design for construction accepted as a whole: the changes P1 to P9 of LKL-DDR-003 (neck bar hanger, flanged end plugs, top plug fittings, internal chassis, puck changes) and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | LKL-DDR-003, P1 to P9 |
| 2026-10-02 | R12 restated as 1.0 kg for the logger, cable and sensor (0.96 kg estimated); the 0.32 kg neck bar is site hardware that stays in the chamber; the logger set is weighed at TRL 4 because the margin is 0.04 kg | Amish: "i approve your recommendations for all 555 open decisions." | LKL-DDR-003, A1 |
| 2026-10-02 | Neck bar for the prototype; the pilot utility is asked for its range of chamber neck sizes before any deployment, and a longer inner tube is designed only if that range goes past 710 mm; a drilled bracket stays the fallback for poor or out-of-range necks | Amish: "i approve your recommendations for all 555 open decisions." | LKL-DDR-003, A2 |
| 2026-10-02 | First partner: a water utility with metallic mains, district metered areas and a leakage target it reports against. First candidate region to approach: the UK, where water companies run district metered areas and report leakage to the regulator; that would set the radio band to EU868 | Amish: "i approve your recommendations for all 555 open decisions." | LKL-DDR-002, O1 |
| 2026-10-02 | The vibration calibration check goes in CalRig as a small shaker bay; LeakListen defines the acceptance test (frequency range, level and pass band) in its own repo | Amish: "i approve your recommendations for all 555 open decisions." | LKL-DDR-002, O2 |
| 2026-10-02 | Light pipe on the top plug kept, lit only for a brief blink at power-up or magnet swipe and added to BOM line 7; board orientation, cable route and render context accepted as appearance only | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26 |
