---
doc_id: LKL-PRS-001
title: LeakListen product requirements and specifications
project: LeakListen
doc_type: Product requirements and specifications
version: "0.8"
status: Draft
date: '2026-11-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: "TRL 3, status from LKL-CAL-001 for every requirement; R8 fixed (LKL-DDR-001 D6); R5 and R14 note the weekly time correction and the 24-byte summary"
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002): R1 and R2 restated (contact sensor for metallic mains, hydrophone variant for plastic); R7 restated against a district gateway within 0.5 km under iron covers; R9 met with the 42 mm magnet; status from LKL-CAL-001 v0.2"
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Constructable design (LKL-DDR-003): status from LKL-CAL-001 v0.3; R12 not met on mass with the neck bar; R15 reported against the value-engineering target; R3 and R10 figures updated"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R12 restated by Amish on 2026-10-02 (LKL-DDR-003 A1): 1.0 kg for the logger, cable and sensor, neck bar counted as site hardware; met on paper"
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'R6 figure and R15 cost updated for the status light pipe (LKL-DDR-003 follow-up); no status changed'
- version: "0.8"
  date: '2026-11-01'
  author: Amish Chadha
  change: 'Converted to the kit 1.9.1 product requirements and specifications format (LKL-REQ-001 becomes LKL-PRS-001): R1 to R15 become PR-001 to PR-015 and S1 to S4 become PR-016 to PR-019, each traced to a user requirement in LKL-URS-001 and listing its old number; PR-020 (legal transmit power) added from LKL-CAL-001 D4; the status of each requirement is unchanged; mass re-run on the D3 model (1.34 kg with the neck bar)'

---

# LeakListen product requirements and specifications

These are the product requirements for one logger, each traced to a user need in LKL-URS-001 (links in LKL-RTM-001); they replace LKL-REQ-001, whose numbers R1 to R15 and S1 to S4 are kept in the "Was" column. The requirements describe option A, the current design, which has not been through a concept choice yet (LKL-OPT-001 recommends it; "Proposed, awaiting Amish"). Targets are proposals for review; they come from desk research, not yet from a partner utility, and must be revised after co-design (see the problem statement, LKL-PRB-001). Status is judged against the design in LKL-PRC-001 v0.5 by the calculations in LKL-CAL-001 v0.2, which print every figure quoted here. The TRL 2 review decisions are recorded in LKL-DDR-001. The TRL 3 review decisions, accepted by Amish on 2026-09-25, are recorded in LKL-DDR-002: they restate R2 (plastic mains are served by the hydrophone variant) and R7 (a gateway within 0.5 km of each district with iron covers); no numeric target is lowered.

*Table 1. Product requirements and specifications. Status at TRL 3 from LKL-CAL-001 (python docs/04-calcs/sizing.py).*

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Hears a leak on metallic mains | Flag a 5 L/min (1.3 US gal/min) leak at 3 bar within 100 m of the logger on cast or ductile iron DN100 to DN200. The magnet-on contact sensor's scope is metallic mains (LKL-DDR-002) | 100 | max distance | m | Attenuation and detection estimate (LKL-CAL-001 section G); later a partner site with a controlled leak | **At risk:** about 185 m on ductile iron at the central estimate (signal equal to noise), about 140 m if the leak must lift the level by the 6 dB of the flag rule (independent review, LKL-STM-001 S2); 93 to 370 m over plausible pipe losses | R1 |
| PR-002 | UR-002 | Performance | Hears a leak on plastic mains (hydrophone variant) | Same leak within 30 m on PVC or PE DN100 to DN200, with the hydrophone variant on a hydrant or tapping point (LKL-DDR-002, D3; option B in LKL-OPT-001) | 30 | max distance | m | As PR-001, for the hydrophone variant | Open: the hydrophone variant is not sized in LKL-CAL-001. First-order screen only (LKL-STM-001 SB1): 54 m on PVC at an assumed 0.1 Pa/rtHz background, none at 1 Pa/rtHz. For the record the contact sensor hears about 4 m on PVC and 2 m on PE | R2 |
| PR-003 | UR-001 | Performance | Sensor bandwidth | 5 Hz to 2 kHz, within ±3 dB after correction | 5 to 2,000 | ±3 dB | Hz | Resonance estimate (LKL-CAL-001 section F); later a shaker comparison | **At risk:** with the 42 mm magnet and the 8 mm puck base the mount resonates at about 676 to 1,350 Hz, flat only to 370 to 730 Hz | R3 |
| PR-004 | UR-001 | Performance | Sensor self-noise | Equivalent input noise 1 µg/√Hz or less from 100 Hz to 1 kHz | 1 | max | µg/√Hz | Noise calculation (LKL-CAL-001 section F) | **At risk:** 1.03 µg/√Hz worst case with the 53 g seismic mass | R4 |
| PR-005 | UR-005 | Performance | Night listening | 12 windows of 20 s between 02:00 and 04:00 local time, clock drift under 1 min per month | 60 | max drift per month | s | Clock drift estimate (LKL-CAL-001 section H) | Met on paper with a weekly network time correction (20 s worst); 87 s a month free running | R5 |
| PR-006 | UR-007 | Electrical | Battery life | 5 years or more on one primary cell at the PR-005 schedule and one uplink a night | 5 | min | years | Power budget (LKL-CAL-001 section C) | Met on paper: 10.1 years or more on energy; taken as 10 years | R6 |
| PR-007 | UR-005 | Electrical | Radio link | 90 % or more of nightly summaries delivered from a chamber with a cast-iron cover to a gateway planned within 0.5 km of each such district; 1 km where the utility agrees to a composite cover or a through-cover antenna (LKL-DDR-002) | 90 at 0.5 | min | % at km | Link budget (LKL-CAL-001 section D); cover loss measurement and field check later (TRL 4, on hold) | **At risk:** +0.9 dB at 0.5 km under a 20 dB iron cover (EU868 SF12), -1.2 dB for US915 SF9, -9.1 dB for a tight 30 dB cover; cover loss unmeasured | R7 |
| PR-008 | UR-009 | Software | Data and privacy | Only band levels and spectra leave the logger; raw vibration samples are deleted on the device after processing. Fixed requirement (LKL-DDR-001 D6) | Pass or fail | Pass or fail | n/a | Design review | Met by design | R8 |
| PR-009 | UR-003, UR-012 | Physical architecture | Attachment | Magnet holds 100 N or more on a steel or iron spindle cap, with no tools or pipe work | 100 | min | N | Hold estimate (LKL-CAL-001 section I); a pull test later | Met on paper with the 42 mm magnet (LKL-DDR-002): 125 N on a 0.5 mm coating, 187 N on 0.3 mm. Non-ferrous fittings, outside this target, need an adapter | R9 |
| PR-010 | UR-003, UR-004 | Usability | Install from the surface | Placed and recovered in 10 min or less without entering the chamber, for chambers up to 1.5 m deep | 10 | max | min | Task estimate (LKL-CAL-001 section K); a walk-through with the partner utility | Not verifiable at TRL 3; the 11 min estimate (neck bar assembled beforehand) is 1 min over the target, so it is at risk on the estimate; cable reaches caps 2.18 m down | R10 |
| PR-011 | UR-006 | Physical architecture | Survive the chamber | IP68: 1 m submersion for 7 days; operate from -20 to +50 °C | IP68; -20 to +50 | Pass or fail | class; °C | Design review (LKL-CAL-001 section J) | Met by design; the logger floats on its lanyard when flooded | R11 |
| PR-012 | UR-014 | Packaging and transport | Size and mass | Logger 70 mm diameter or less and 300 mm long or less; logger, cable and sensor 1.0 kg or less. The neck bar is site hardware that stays in the chamber and is not counted (restated by Amish on 2026-10-02, LKL-DDR-003 A1) | 70 x 300; 1.0 | max | mm; kg | Parametric model (LKL-CAL-001 section K); weighing at TRL 4 | Met on paper: 68 x 283 mm overall; logger, cable and sensor 0.96 kg (0.04 kg margin); the neck bar is 0.31 kg. The 70 g antenna rides on the bar and is counted with it; with the antenna the carried set is 1.03 kg (independent review 2026-11-01): the exclusion is Proposed, awaiting Amish to confirm | R12 |
| PR-013 | UR-013 | Performance | Leak flag quality | 1 false alarm or fewer per 20 loggers per month after a 14-night baseline | 1 per 20 | max | per month | Field data from a partner network | Not verifiable at TRL 3 | R13 |
| PR-014 | UR-010, UR-015 | Software | Open and interoperable | Standard LoRaWAN 1.0.x uplink (1.0.3 for the time request), documented 24-byte payload, works with any network server and TwinKit | 24 | max payload | B | Design review (LKL-CAL-001 sections A and B) | Met by design | R14 |
| PR-015 | UR-008 | Cost | Cost | Parts cost per logger against a value-engineering target of USD 130 (`budget_usd`, a hypothetical control target) | 130 | max | USD | Priced BOM (LKL-CAL-001 section M) | USD 142, USD 12 over the value-engineering target | R15 |
| PR-016 | UR-003, UR-011 | Safety | No confined space entry | No confined space entry is needed to place, service or recover a logger | Pass or fail | Pass or fail | n/a | Design review; build plan steps (LKL-BLD-001) | Met by design (surface placement by pole, PR-010) | S1 |
| PR-017 | UR-011 | Safety | Safe cell | The cell is a primary lithium cell with a fuse or PTC and reverse protection; no charging circuit is fitted | Pass or fail | Pass or fail | n/a | Design review; main board design at TRL 4 | Met by design on paper; the board is not designed at TRL 3 | S2 |
| PR-018 | UR-011, UR-016 | Safety | Labelled | The logger carries a label with the owner, a contact and a lithium cell warning | Pass or fail | Pass or fail | n/a | Inspection of BOM line 11 and the build plan | Met by design (label in BOM line 11) | S3 |
| PR-019 | UR-012 | Safety | Nothing touches the water | Nothing touches drinking water, and nothing is fixed to the pipe other than the magnet | Pass or fail | Pass or fail | n/a | Design review of the model (no part passes through a pipe wall) | Met by design; applies to option A only (option B's hydrophone is in the water, LKL-REG-001 G4) | S4 |
| PR-020 | UR-016 | Regulatory | Legal transmit power | Transmit power within the regional limit: +14 dBm ERP in EU868 (16.15 dBm EIRP); up to +20 dBm in US915 where permitted | 14 | max | dBm | Design review (LKL-CAL-001 D4); regulatory check at TRL 4 (LKL-REG-001) | Met by design in EU868 at +14 dBm; the TRL 2 figure of +20 dBm conducted is not permitted there unless the antenna gain and lead loss bring it under 14 dBm ERP (independent review): the free-field antenna gain is to assess | (LKL-CAL-001 D4) |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software, cost, regulatory. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Requirements at risk or open

The notes below keep the old numbers R1 to R15; R-n is PR-0n (R1 is PR-001, R15 is PR-015).

Summary (LKL-CAL-001 v0.6, Table 6): none not met, 4 at risk, 1 open (R2, variant not sized), 2 not verifiable at TRL 3, 4 met on paper, 3 met by design, and R15 USD 12 over its value-engineering target. R12 was not met on mass after LKL-DDR-003 until Amish restated it on 2026-10-02 (A1); before LKL-DDR-003 R12 and R15 were met on paper; before LKL-DDR-002 there were 2 not met (R2, R7) and 4 at risk (R1, R3, R4, R9).

- **R12 thin margin on mass.** The concept's strap hanger could not be built (it had nothing to hook over except the seat under the cover), and the neck bar that replaces it (LKL-DDR-003) weighs 0.31 kg (0.32 kg before the D3 rebuild). The set is 1.34 kg; the logger, cable and sensor are 0.96 kg. Amish decided on 2026-10-02 (LKL-DDR-003, A1) to restate R12 as 1.0 kg for the logger, cable and sensor and count the bar as site hardware, so R12 is met on paper with a 0.04 kg margin; the logger set is weighed at TRL 4.

- **R7 at risk.** At an assumed 20 dB cover loss the link closes to about 0.53 km in EU868 and 0.46 km in US915. Under LKL-DDR-002 a gateway is planned within 0.5 km of each district with iron covers, which EU868 SF12 reaches with +0.9 dB to spare and US915 SF9 misses by 1.2 dB. The cover loss must be measured first; that is TRL 4 work and on hold.
- **R2 open.** Leak noise attenuates quickly on plastic pipes (0.42 dB/m at 100 Hz on PVC against 0.011 dB/m on ductile iron), and a contact sensor on a valve hears the reference leak only a few metres along PVC or PE. Under LKL-DDR-002 R2 applies to the hydrophone variant (LKL-DDR-001 D3), which is not yet sized.
- **R1 at risk.** The central estimate of 185 m on iron clears 100 m, but pipe loss and leak source strength are both uncertain by large factors.
- **R3 at risk.** The magnet mount's resonance falls inside the band and varies by site; the heavier 42 mm magnet and the 8 mm puck base lower it by about 13 %.
- **R4 at risk.** 1.03 µg/√Hz against 1 µg/√Hz, on assumed ceramic and op-amp data.
- **R9 met on paper** with the 42 mm magnet (LKL-DDR-002); it was at risk with the 32 mm magnet (90 N at a 0.3 mm coating). Brass, bronze or plastic fittings still need an adapter.
- **R10 and R13 not verifiable at TRL 3.** They need a walk-through and field data with a partner utility.

## Assumptions

- Network pressure at night 2 to 6 bar; leaks at lower pressure are quieter.
- Valve spindle caps and hydrant bodies are cast iron or steel on most networks the lab would target first.
- A LoRaWAN gateway (TwinKit, a partner's or a public network) is within about 1 km in an urban area, and within about 0.5 km of each district with cast-iron covers (LKL-DDR-002).
- Transmit power follows the regional limit: +14 dBm in EU868, up to +20 dBm in US915.
- Primary cell: lithium thionyl chloride C size, 3.6 V, about 7.7 Ah nominal, derated to 70 % usable for cold and pulse loads.

## Safety requirements

> **Safety:** PR-016 (was S1): no confined space entry is needed to place, service or recover a logger. PR-017 (was S2): the cell is a primary lithium cell with a fuse or PTC and reverse protection; no charging circuit is fitted. PR-018 (was S3): the logger carries a label with the owner, a contact and a lithium cell warning. PR-019 (was S4): nothing touches drinking water, and nothing is fixed to the pipe other than the magnet.
