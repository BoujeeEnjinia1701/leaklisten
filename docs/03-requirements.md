---
doc_id: LKL-REQ-001
title: LeakListen requirements
project: LeakListen
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
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
---

# LeakListen requirements

These are first-pass requirements for one logger. Targets are proposals for review; they come from desk research, not yet from a partner utility, and must be revised after co-design (see the problem statement, LKL-PRB-001). Status is judged against the design in LKL-PRC-001 v0.3 by the calculations in LKL-CAL-001, which print every figure quoted here. The TRL 2 review items adopted for TRL 3 are recorded in LKL-DDR-001; no target is relaxed or redefined by them.

Table 1. Requirements and status at TRL 3 (LKL-CAL-001).

| ID | Requirement | Target | Verification | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Hear a leak on metallic mains | Flag a 5 L/min (1.3 US gal/min) leak at 3 bar within 100 m of the logger on cast or ductile iron DN100 to DN200 | Attenuation and detection estimate (LKL-CAL-001 section G); later a partner site with a controlled leak | **At risk:** about 185 m on ductile iron at the central estimate, 93 to 370 m over plausible pipe losses |
| R2 | Hear a leak on plastic mains | Same leak within 30 m on PVC or PE DN100 to DN200 | As R1 | **Not met:** about 4 m on PVC and 2 m on PE with a contact sensor on a valve |
| R3 | Sensor bandwidth | 5 Hz to 2 kHz, within ±3 dB after correction | Resonance estimate (LKL-CAL-001 section F); later a shaker comparison | **At risk:** the magnet mount resonates at about 780 to 1,550 Hz, flat only to 420 to 840 Hz |
| R4 | Sensor self-noise | Equivalent input noise 1 µg/√Hz or less from 100 Hz to 1 kHz | Noise calculation (LKL-CAL-001 section F) | **At risk:** 1.03 µg/√Hz worst case with the 53 g seismic mass |
| R5 | Night listening | 12 windows of 20 s between 02:00 and 04:00 local time, clock drift under 1 min per month | Clock drift estimate (LKL-CAL-001 section H) | Met on paper with a weekly network time correction (20 s worst); 87 s a month free running |
| R6 | Battery life | 5 years or more on one primary cell at the R5 schedule and one uplink a night | Power budget (LKL-CAL-001 section C) | Met on paper: 10.3 years or more on energy; taken as 10 years |
| R7 | Radio link | 90 % or more of nightly summaries delivered to a gateway within 1 km from a chamber with a cast-iron cover | Link budget (LKL-CAL-001 section D); later a field check | **Not met:** about 0.53 km under an iron cover at an assumed 20 dB cover loss (EU868 SF12) |
| R8 | Data and privacy | Only band levels and spectra leave the logger; raw vibration samples are deleted on the device after processing. Fixed requirement (LKL-DDR-001 D6) | Design review | Met by design |
| R9 | Attachment | Magnet holds 100 N or more on a steel or iron spindle cap, with no tools or pipe work | Hold estimate (LKL-CAL-001 section I); a pull test later | **At risk:** 149 N bare, 90 N on a 0.3 mm coating; not met for non-ferrous fittings |
| R10 | Install from the surface | Placed and recovered in 10 min or less without entering the chamber, for chambers up to 1.5 m deep | Task estimate (LKL-CAL-001 section K); a walk-through with the partner utility | Not verifiable at TRL 3: 10 min estimate; cable reaches caps 2.09 m down |
| R11 | Survive the chamber | IP68: 1 m submersion for 7 days; operate from -20 to +50 °C | Design review (LKL-CAL-001 section J) | Met by design; the logger floats on its lanyard when flooded |
| R12 | Size and mass | Logger 70 mm diameter or less and 300 mm long or less; total mass 1.0 kg or less | Parametric model (LKL-CAL-001 section K) | Met on paper: 63 x 267 mm overall, 0.93 kg |
| R13 | Leak flag quality | 1 false alarm or fewer per 20 loggers per month after a 14-night baseline | Field data from a partner network | Not verifiable at TRL 3 |
| R14 | Open and interoperable | Standard LoRaWAN 1.0.x uplink (1.0.3 for the time request), documented 24-byte payload, works with any network server and TwinKit | Design review (LKL-CAL-001 sections A and B) | Met by design |
| R15 | Cost | Parts cost $130 or less per logger | Priced BOM (LKL-CAL-001 section M) | Met on paper: $109.00 |

## Requirements not met or at risk

Summary (LKL-CAL-001, Table 6): 2 not met, 4 at risk, 2 not verifiable at TRL 3, 4 met on paper and 3 met by design.

- **R2 not met.** Leak noise attenuates quickly on plastic pipes (0.42 dB/m at 100 Hz on PVC against 0.011 dB/m on ductile iron), and a contact sensor on a valve hears the reference leak only a few metres along PVC or PE. The hydrophone variant kept open in LKL-DDR-001 D3 is the likely answer; the scope for plastic networks is proposed in `docs/REVIEW.md`, awaiting Amish.
- **R7 not met.** At an assumed 20 dB cover loss the link closes to about 0.53 km, not 1 km. Options (proposed, awaiting Amish): a through-cover antenna, a composite cover, or a gateway within about 0.5 km of each district.
- **R1 at risk.** The central estimate of 185 m on iron clears 100 m, but pipe loss and leak source strength are both uncertain by large factors.
- **R3 at risk.** The magnet mount's resonance falls inside the band and varies by site.
- **R4 at risk.** 1.03 µg/√Hz against 1 µg/√Hz, on assumed ceramic and op-amp data.
- **R9 at risk** on coated ferrous caps, and not met on brass, bronze or plastic fittings, which need an adapter. A 42 mm magnet is proposed in `docs/REVIEW.md`.
- **R10 and R13 not verifiable at TRL 3.** They need a walk-through and field data with a partner utility.

## Assumptions

- Network pressure at night 2 to 6 bar; leaks at lower pressure are quieter.
- Valve spindle caps and hydrant bodies are cast iron or steel on most networks the lab would target first.
- A LoRaWAN gateway (TwinKit, a partner's or a public network) is within about 1 km in an urban area. LKL-CAL-001 shows that under an iron cover it must be closer, about 0.5 km, unless the cover loss is lower than assumed.
- Transmit power follows the regional limit: +14 dBm in EU868, up to +20 dBm in US915.
- Primary cell: lithium thionyl chloride C size, 3.6 V, about 7.7 Ah nominal, derated to 70 % usable for cold and pulse loads.

## Safety requirements

> **Safety:** S1: no confined space entry is needed to place, service or recover a logger. S2: the cell is a primary lithium cell with a fuse or PTC and reverse protection; no charging circuit is fitted. S3: the logger carries a label with the owner, a contact and a lithium cell warning. S4: nothing touches drinking water, and nothing is fixed to the pipe other than the magnet.
