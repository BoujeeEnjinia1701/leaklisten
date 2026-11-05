---
doc_id: LKL-RSK-001
title: LeakListen risk register and hazard analysis
project: LeakListen
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis and first-pass design FMEA for option A (stage P3), with the extra hazards of options B and C
---

# LeakListen risk register and hazard analysis

The top project risk is that no utility partner is found, so the cover loss, the pipe materials and the site noise all stay assumptions; the top hazard is work at a street chamber (confined space, traffic and a heavy cover), which the design avoids by placing the logger from the surface; the highest design FMEA scores are the lithium cell failing its first radio pulse after a long rest (RPN 48) and the radio not escaping an iron cover (RPN 36). All scores are the author's judgement, not data. Method: STANDARDS section 23 and ISO 12100. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be caught) to 5 (unlikely to be caught).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No utility partner | None approached; the first candidate region is the UK (LKL-DEC-001, 2026-10-02) | Reach, cover loss and false alarm rate stay desk estimates; no TRL 4 | 3 | 5 | Amish | Approach a UK water company with district metered areas before TRL 4 |
| P2 | Cover loss too high | Cast-iron or flooded covers block LoRa (20 dB assumed, 30 dB tight) | Nightly summary does not arrive (PR-007) | 4 | 4 | Design lead | Gateway within 0.5 km, through-cover antenna where agreed; measure first (LKL-DDR-002 D7) |
| P3 | Sensor data assumed | Ceramic d33, op-amp noise and contact stiffness taken from typical values | Self-noise and bandwidth miss PR-003, PR-004 | 3 | 3 | Design lead | Check against chosen parts; shaker comparison in CalRig (decided 2026-10-02) |
| P4 | Cost over target | USD 142 against USD 130; main board is a prototype price | Value-engineering target missed (PR-015) | 3 | 2 | Amish | Savings in LKL-DEC-001 (fixed-length bar, batch plugs) |
| P5 | Lithium cell supply and shipping | Dangerous goods rules for lithium metal cells | Delays and cost for sample cells | 3 | 2 | Design lead | Use a distributor that ships UN3090 cells; LKL-REG-001 G3 |
| P6 | Hydrophone variant undefined | Option B is not sized in LKL-CAL-001; hydrant outlets vary | PR-002 (plastic mains) stays open | 4 | 3 | Design lead | Size B after Amish chooses (LKL-DDR-004); hydrant survey with the partner |
| P7 | TRL 4 on hold | Portfolio stage cap P3 | No hardware evidence | 5 | 3 | Amish | Wait for the cap to lift; keep a plan (LKL-PLN-001) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Confined space entry | Someone enters the chamber to place or fetch a logger | Asphyxia, poisoning | 5 | 2 | Placed from the surface by pole; lanyard to recover the logger; no entry without the utility's permit, gas test and standby (LKL-PRC-001 Safety) | 2 |
| H2 | Heavy cover | Lifting a 30 kg or heavier cover | Back injury, crushed foot | 4 | 3 | Lifting key, two people, feet clear | 2 |
| H3 | Traffic at the chamber | Work in a live street | Death or injury from a vehicle | 5 | 2 | Traffic management under local rules (LKL-REG-001 G6) | 2 |
| H4 | Lithium cell fire or venting | Short, crush, heat or charge of the Li-SOCl2 cell | Burns, toxic gas | 5 | 1 | Fuse or PTC, reverse protection, no charging circuit, label (PR-017, PR-018) | 2 |
| H5 | Magnet pinch and implant interference | The 42 mm pot magnet, about 600 N rated, snaps to steel | Crushed fingers; effect on pacemakers | 3 | 3 | Keeper plate on in transport; removed only at the cap; warning in the build plan | 2 |
| H6 | Dropped neck bar or logger | The bar slips off the neck and falls onto the valve | Damage; falling object | 2 | 3 | Lanyard from the bar to the logger; rubber feet wedge the bar; pole placement | 1 |
| H7 | Pressurised hydrant (option B) | Cap removed or hydrant opened under pressure | A 3.2 kN force on the cap at 10 bar; water hammer; jet | 4 | 2 | Not applicable to option A; for B: open and close hydrants slowly, partner's procedure, depressurise before bolting | 3 |
| H8 | Buried services strike (option C) | Digging a hole and driving a spike near services | Electric shock, gas or water main damage | 5 | 2 | Not applicable to option A; for C: services search, hand dig, trained crew | 3 |

## Design FMEA (first pass, P3)

Table 3. Failure modes of option A. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Lithium cell and capacitor | Supply the radio pulse | First pulse browns out after a long rest | Reset; no uplink the first nights | Passivation of the Li-SOCl2 cell | 4 | 3 | 4 | 48 | Hybrid layer capacitor (0.059 F needed against 0.1 F fitted, LKL-CAL-001 C3); pulse test at TRL 4 (LKL-STM-001 S9) |
| F2 | Flat antenna | Radio out of the chamber | Cover blocks the signal | No summary received | Cast-iron or flooded cover, 20 to 30 dB | 3 | 4 | 3 | 36 | Gateway within 0.5 km; measure cover loss first; through-cover antenna where agreed |
| F3 | M12 plug and socket | Sensor link | Corrosion or water in the connector | Noisy or lost signal | Chamber damp; mated for years | 3 | 3 | 4 | 36 | IP68 A-coded connector; potted overmould; inspect at each visit |
| F4 | Desiccant and seals | Keep the board dry | Condensation in the tube | Corrosion of the board | Humid chamber; pack used up | 3 | 3 | 4 | 36 | 10 g silica gel holds about 2,000 mg against 5 mg of vapour (LKL-CAL-001 J3); O-ring grooves; potting |
| F5 | O-rings and radial screws | Seal the housing | Leak | Water in the logger | Damaged O-ring; screw not seated | 4 | 2 | 4 | 32 | Compressed O-rings in grooves; the logger floats on its lanyard so it is not submerged for long |
| F6 | Sensor mount | Pass the pipe vibration | Resonance in the band | Wrong spectrum shape | Contact stiffness of a coated cap | 2 | 4 | 4 | 32 | Calibrate on the shaker (CalRig bay); equaliser (LKL-STM-001 S6) |
| F7 | Pot magnet | Hold the puck | Puck slips off | No signal; puck dangles on its cable | Coating gap over 0.5 mm; non-ferrous cap | 3 | 3 | 3 | 27 | 125 N at 0.5 mm against 100 N; adapter for non-ferrous fittings |
| F8 | Piezo disc and mass | Sense | Bond fails or depolarises | Sensitivity lost | Heat, shock, epoxy ageing | 3 | 2 | 4 | 24 | Compression mode with a bonded brass mass; ceramic temperature rating to check |
| F9 | Light pipe seal | Show status | Water enters round the rod | Water in the top plug | Epoxy bond cracks | 3 | 2 | 4 | 24 | Epoxied into a 3 mm hole; blink only at power-up and magnet swipes |
| F10 | Neck bar feet | Hold the bar across the neck | Bar slips | Logger and antenna hang on the lanyard | Neck out of the 570 to 710 mm range; smooth wall | 2 | 3 | 3 | 18 | Rubber pads; locking pin; neck range asked of the partner (LKL-DEC-001) |
| F11 | Real-time clock | Wake in the night window | Drift beyond the window | Listens at the wrong hour | Temperature; missed time sync | 2 | 2 | 3 | 12 | Weekly time request; 20 s worst (LKL-CAL-001 H2) |

## Sources

- TFL-RSK-001 of the sister repo TideFlap (format only).
- LKL-CAL-001 for the loads, charges and margins quoted; LKL-STM-001 for the plausible rows.
- Hazards H5 to H8 follow the design notes in LKL-PRC-001 and the option descriptions in LKL-OPT-001; no incident data was consulted.
