---
doc_id: LKL-DDR-003
title: LeakListen design for construction
project: LeakListen
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish on 2026-10-02 (Tables 1 to 3); record stays Draft"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Every change in Table 1 was made under Amish's 2026-09-30 instruction to make the design physically buildable. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 and A2), recorded in the design decisions register (LKL-DEC-001, items 1 to 3). The record stays Draft.

## Context

On 2026-09-30 Amish asked for a build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of LKL-DDR-002 showed what LeakListen does, but several of its parts could not be made or fixed as drawn. Checking the model with build123d (overlaps, contacts, clearances and assembly order) found the nine problems below. An earlier note in `docs/REVIEW.md` (2026-09-26) had already flagged one of them: the hanger plate overlapped the antenna by about 10 mm.

The changes keep what LeakListen does: a magnet-on piezo sensor on the valve spindle cap, a sealed logger in the chamber neck, a flat antenna just under the cover, one C-size primary cell, placement from the surface with no chamber entry, and the same electronics, radio and data. Nothing here changes the pitch or the safety case; one change (P1) removes a hazard the concept had. Every change is in `cad/src/model.py`, which now runs 72 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least the stated clearance. All 72 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The hanger was a 1.5 mm stainless strap "hooked over the cover frame". The hook had nothing to hook over: the cover sits on the frame's seat, so a strap there lies under the cover, which then rocks under traffic. As modelled, the hook overlapped the frame and was held by nothing. | A telescopic neck bar: a 20 x 20 x 1.5 mm aluminium square tube with a 16 x 16 x 1.5 mm tube sliding inside it, a rubber-padded M10 levelling foot screwed into a tube insert at each end, and a 6 mm locking pin through both tubes. It is wedged across the chamber neck 85 mm below the street (below the frame) by winding one foot out by hand. The logger hangs from it on a 3 mm wire rope lanyard with a loop round the bar and a snap hook. | Leaves the cover and frame untouched and seated, needs no drilling of the utility's asset, and is still placed from the surface. Spreader bars of this kind are a common way of hanging instruments in manholes. Seven pin holes at 20 mm and about 30 mm of foot travel cover necks of about 570 to 710 mm. |
| P2 | The hanger plate overlapped the flat antenna by about 10 mm, and the antenna had no fixing. | A 40 x 3 mm aluminium bracket, 100 mm long, lies across the top of the outer tube on one M5 bolt; the antenna's centre stud passes through it with a nut underneath. The antenna centre is 45 mm off the bar line and its top is 20 mm under the cover (8 mm in the concept). | Nothing overlaps, and the antenna is held by the stud it is bought with. 12 mm further from the cover is small beside the 10 to 30 dB assumed for the cover itself (LKL-CAL-001, section D). |
| P3 | The logger's end plugs were drawn fused into the tube, with no way to retain them. | Two flanged end plugs turned from 65 mm acetal bar: a 63 mm flange 4 mm thick on the tube end and a 57 mm spigot 18 mm long inside, with two O-ring grooves. Each is held by three M4 screws through the tube wall into the spigot, 4 mm from the tube end, outboard of both O-rings. The PVC tube is cut to 232 mm so the logger stays 240 mm flange to flange. | A push-in plug with double O-rings is the usual way to seal a tube for 1 m submersion (R11); the screws stop it working out and never cross the seal. |
| P4 | One "antenna and lanyard gland" on the top plug. A lanyard cannot pass through a cable gland, and the antenna lead ends in a connector that a gland cannot seal round. | An M6 stainless eye bolt on the axis of the top plug, with a bonded sealing washer and nyloc nut, takes the lanyard; an IP67 SMA bulkhead with its O-ring, 14 mm off the axis, takes the antenna lead. New BOM line 13. | Each fitting does one job and seals on its own washer or O-ring. The lanyard load now goes into the plug, not into the antenna lead. |
| P5 | The board, capacitor, cell and desiccant floated inside the tube with no fixing. | A printed PETG chassis: a 48 x 3 x 158 mm spine with a top tab, hung from the top plug on two M3 x 20 standoffs. The board is on four short standoffs on one face; the cell and capacitor snap into clips and the desiccant sits in a pocket on the other face. New BOM line 12. | The electronics are fixed, lift out with the top plug as one unit, and clear the tube bore by 0.8 mm or more. |
| P6 | The M12 socket was drawn as a cylinder on the bottom of the tube with no way to mount it. | A front-mount M12 panel socket screwed into an M16 x 1.5 thread through the bottom plug, sealed by its own O-ring, with a short 4-pin lead to the board. | Uses the socket's standard panel mounting. |
| P7 | The puck had a 3 mm base, too thin to take the pot magnet's M6 stud, so the magnet had no fixing. | Base 8 mm thick, tapped M6 for 6 mm of full thread; the magnet's stud is cut to 6 mm and fitted with threadlocker. | The stud now holds the magnet to the puck and the base stays solid under the piezo disc. |
| P8 | The preamplifier board floated 6 mm above the seismic mass, and "potted" left open whether potting would fill round the mass. | The puck bore is stepped: 29 mm below, 32 mm above, the step 25 mm above the base. A round 31 mm preamplifier board sits on the step, 4.5 mm above the mass, and potting fills only the space above the board. | The mass must stand free: potting round it would add damping and stiffness and change the sensitivity of LKL-CAL-001 [F1]. The step locates the board without tools. |
| P9 | The sensor cable ran straight into the potted lid with no defined exit, and the logger hung from the old hanger at 90 mm below the street. | The cable leaves through the potting on the puck axis; the logger now hangs with its top 180 mm below the street, clear of the bar by 70 mm, and the M12 plug sits 480 mm below the street. | Follows from P1: the lanyard and snap hook need about 70 mm under the bar. The 2 m cable still reaches caps 2.18 m deep [K2]. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 1.35 kg in all with the neck bar and antenna (0.98 kg in the concept) [K1]. The logger, cable and sensor are 0.96 kg; the neck bar with its feet and lanyard is 0.32 kg. R12 (1.0 kg in all) is now not met; see A1. | The neck bar replaces a 0.05 kg strap; the flanged plugs, chassis and fittings add about 0.1 kg. |
| Cost | BOM lines 1, 6 and 9 repriced and lines 12 and 13 added. Value-engineering target: USD 130. Estimated cost of the constructable design: USD 141 (USD 11 over the target) [M1]. | Parts added for construction; the neck bar (USD 18) is the largest change. |
| Size | 63 mm diameter (68 mm over the radial screw heads), 240 mm flange to flange, 283 mm with the socket and eye bolt. R12's 70 x 300 mm still holds. | Flanges, socket and eye bolt. |
| Sensor | Puck and magnet 277 g (262 g); mounted resonance 676 to 1,352 Hz (695 to 1,389 Hz). R3 stays at risk, slightly worse. | Thicker base (P7). |
| Flooding | The logger body is 551 g against 748 g of water displaced; it still floats on its lanyard when the chamber floods, now with 1.9 N of lift [J2]. | Heavier plugs and chassis. |
| Install time | 11 min task estimate (10 min), with the bar, logger and antenna assembled before going to site [K3]. R10 stays not verifiable at TRL 3. | Setting the bar takes about a minute longer than hooking a strap. |
| Drawing | LKL-DWG-001 Rev P4; making sketches LKL-DWG-101 to 109 added. | Follows the model. |
| Calculations | LKL-CAL-001 v0.3: mass, cost, resonance, flooding, cable reach and install time re-run; every other section is unchanged. | Follows the model. |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | R12 limits total mass to 1.0 kg; with the neck bar the set is 1.35 kg. | (a) restate R12 as 1.0 kg for the logger, cable and sensor (0.96 kg) and count the neck bar as site hardware; (b) relax R12 to 1.5 kg in all; (c) look for a lighter hanger (1 mm wall tube saves about 55 g; still not met). | (a): R12 was set for handling the logger, and the bar stays in the neck between visits. Accepted 2026-10-02; the logger set is weighed at TRL 4, since the margin is 0.04 kg. |
| A2 | The neck bar needs a neck of about 570 to 710 mm with two sound opposite walls. | (a) neck bar as modelled, with a longer inner tube for wider necks; (b) a bracket on two concrete screws in the neck wall, which needs the utility's consent to drill. | (a) for the prototype; confirm the neck sizes of the pilot district before any deployment. Accepted 2026-10-02; a longer inner tube is designed only if the pilot utility's neck sizes go past 710 mm, and the drilled bracket stays the fallback. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan LKL-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- With A1 accepted, R12 is met on paper (0.96 kg for the logger, cable and sensor against 1.0 kg; LKL-REQ-001 v0.6, LKL-CAL-001 v0.4). Before it, the requirement status (LKL-CAL-001 v0.3) was: 1 not met (R12, mass, see A1), 4 at risk (R1, R3, R4, R7), 1 open (R2), 2 not verifiable at TRL 3 (R10, R13), 3 met on paper (R5, R6, R9), 3 met by design (R8, R11, R14), and R15 reported against the value-engineering target: USD 11 over it.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept strap hanger, the fused plugs and the single top gland; they need updating on Amish's Mac, where Blender is. `cad/src/model.py` keeps the concept strap parameters only so `product_model.py` still runs.
- The pot magnet's stud length, the antenna's stud size, the SMA bulkhead's hole size and the M12 socket's thread are confirmed when parts are bought (LKL-DEC-001).
