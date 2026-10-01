---
doc_id: LKL-REQ-001
title: LeakListen requirements
project: LeakListen
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-01'
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
---

# LeakListen requirements

These are first-pass requirements for one logger. Targets are proposals for review; they come from desk research, not yet from a partner utility, and must be revised after co-design (see the problem statement, LKL-PRB-001). Status is judged against the design in LKL-PRC-001 v0.5 by the calculations in LKL-CAL-001 v0.2, which print every figure quoted here. The TRL 2 review decisions are recorded in LKL-DDR-001. The TRL 3 review decisions, accepted by Amish on 2026-09-25, are recorded in LKL-DDR-002: they restate R2 (plastic mains are served by the hydrophone variant) and R7 (a gateway within 0.5 km of each district with iron covers); no numeric target is lowered.

Table 1. Requirements and status at TRL 3 (LKL-CAL-001).

| ID | Requirement | Target | Verification | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Hear a leak on metallic mains (contact sensor) | Flag a 5 L/min (1.3 US gal/min) leak at 3 bar within 100 m of the logger on cast or ductile iron DN100 to DN200. The magnet-on contact sensor's scope is metallic mains (LKL-DDR-002) | Attenuation and detection estimate (LKL-CAL-001 section G); later a partner site with a controlled leak | **At risk:** about 185 m on ductile iron at the central estimate, 93 to 370 m over plausible pipe losses |
| R2 | Hear a leak on plastic mains (hydrophone variant) | Same leak within 30 m on PVC or PE DN100 to DN200, with the hydrophone variant on a hydrant or tapping point (LKL-DDR-002, D3) | As R1, for the hydrophone variant | Open: the hydrophone variant is not sized at TRL 3. For the record, the contact sensor, now out of scope for plastic, hears about 4 m on PVC and 2 m on PE |
| R3 | Sensor bandwidth | 5 Hz to 2 kHz, within ±3 dB after correction | Resonance estimate (LKL-CAL-001 section F); later a shaker comparison | **At risk:** with the 42 mm magnet and the 8 mm puck base the mount resonates at about 676 to 1,350 Hz, flat only to 370 to 730 Hz |
| R4 | Sensor self-noise | Equivalent input noise 1 µg/√Hz or less from 100 Hz to 1 kHz | Noise calculation (LKL-CAL-001 section F) | **At risk:** 1.03 µg/√Hz worst case with the 53 g seismic mass |
| R5 | Night listening | 12 windows of 20 s between 02:00 and 04:00 local time, clock drift under 1 min per month | Clock drift estimate (LKL-CAL-001 section H) | Met on paper with a weekly network time correction (20 s worst); 87 s a month free running |
| R6 | Battery life | 5 years or more on one primary cell at the R5 schedule and one uplink a night | Power budget (LKL-CAL-001 section C) | Met on paper: 10.3 years or more on energy; taken as 10 years |
| R7 | Radio link | 90 % or more of nightly summaries delivered from a chamber with a cast-iron cover to a gateway planned within 0.5 km of each such district; 1 km where the utility agrees to a composite cover or a through-cover antenna (LKL-DDR-002) | Link budget (LKL-CAL-001 section D); cover loss measurement and field check later (TRL 4, on hold) | **At risk:** +0.9 dB at 0.5 km under a 20 dB iron cover (EU868 SF12), -1.2 dB for US915 SF9, -9.1 dB for a tight 30 dB cover; cover loss unmeasured |
| R8 | Data and privacy | Only band levels and spectra leave the logger; raw vibration samples are deleted on the device after processing. Fixed requirement (LKL-DDR-001 D6) | Design review | Met by design |
| R9 | Attachment | Magnet holds 100 N or more on a steel or iron spindle cap, with no tools or pipe work | Hold estimate (LKL-CAL-001 section I); a pull test later | Met on paper with the 42 mm magnet (LKL-DDR-002): 125 N on a 0.5 mm coating, 187 N on 0.3 mm. Non-ferrous fittings, outside this target, need an adapter |
| R10 | Install from the surface | Placed and recovered in 10 min or less without entering the chamber, for chambers up to 1.5 m deep | Task estimate (LKL-CAL-001 section K); a walk-through with the partner utility | Not verifiable at TRL 3: 11 min estimate with the neck bar assembled beforehand; cable reaches caps 2.18 m down |
| R11 | Survive the chamber | IP68: 1 m submersion for 7 days; operate from -20 to +50 °C | Design review (LKL-CAL-001 section J) | Met by design; the logger floats on its lanyard when flooded |
| R12 | Size and mass | Logger 70 mm diameter or less and 300 mm long or less; total mass 1.0 kg or less | Parametric model (LKL-CAL-001 section K) | **Not met (mass):** 68 x 283 mm overall meets the size limits; 1.35 kg with the neck bar hanger (LKL-DDR-003), of which the logger, cable and sensor are 0.96 kg. Restating the mass limit is proposed (LKL-DDR-003, A1) |
| R13 | Leak flag quality | 1 false alarm or fewer per 20 loggers per month after a 14-night baseline | Field data from a partner network | Not verifiable at TRL 3 |
| R14 | Open and interoperable | Standard LoRaWAN 1.0.x uplink (1.0.3 for the time request), documented 24-byte payload, works with any network server and TwinKit | Design review (LKL-CAL-001 sections A and B) | Met by design |
| R15 | Cost | Parts cost per logger against a value-engineering target of USD 130 (`budget_usd`, a hypothetical control target) | Priced BOM (LKL-CAL-001 section M) | USD 141, USD 11 over the value-engineering target |

## Requirements at risk or open

Summary (LKL-CAL-001 v0.3, Table 6): 1 not met (R12, mass), 4 at risk, 1 open (R2, variant not sized), 2 not verifiable at TRL 3, 3 met on paper, 3 met by design, and R15 USD 11 over its value-engineering target. Before LKL-DDR-003 R12 and R15 were met on paper; before LKL-DDR-002 there were 2 not met (R2, R7) and 4 at risk (R1, R3, R4, R9).

- **R12 not met on mass.** The concept's strap hanger could not be built (it had nothing to hook over except the seat under the cover), and the neck bar that replaces it (LKL-DDR-003) weighs 0.32 kg. The set is 1.35 kg; the logger, cable and sensor are 0.96 kg. Proposed, awaiting Amish: restate the limit for the logger, cable and sensor and count the bar as site hardware (LKL-DDR-003, A1).

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

> **Safety:** S1: no confined space entry is needed to place, service or recover a logger. S2: the cell is a primary lithium cell with a fuse or PTC and reverse protection; no charging circuit is fitted. S3: the logger carries a label with the owner, a contact and a lithium cell warning. S4: nothing touches drinking water, and nothing is fixed to the pipe other than the magnet.
