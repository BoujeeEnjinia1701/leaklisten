---
doc_id: LKL-REQ-001
title: LeakListen requirements
project: LeakListen
doc_type: Requirements
version: "0.2"
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
---

# LeakListen requirements

These are first-pass requirements for one logger. Targets are proposals for review; they come from desk research, not yet from a partner utility, and must be revised after co-design (see the problem statement, LKL-PRB-001). Status is judged against the concept in LKL-PRC-001 and is an estimate until checked at TRL 3 or later.

Table 1. Requirements and status at TRL 2.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Hear a leak on metallic mains | Flag a 5 L/min (1.3 US gal/min) leak at 3 bar within 100 m of the logger on cast or ductile iron DN100 to DN200 | Literature attenuation estimate at TRL 3; later a test rig or partner site with a controlled leak | Unverified |
| R2 | Hear a leak on plastic mains | Same leak within 30 m on PVC or PE DN100 to DN200 | As R1 | At risk: plastic pipes attenuate leak noise strongly |
| R3 | Sensor bandwidth | 5 Hz to 2 kHz, within ±3 dB after correction | Preamplifier calculation; later a shaker comparison with a reference accelerometer | Met on paper (design choice) |
| R4 | Sensor self-noise | Equivalent input noise 1 µg/√Hz or less from 100 Hz to 1 kHz | Noise calculation of the piezo and charge amplifier at TRL 3 | Unverified |
| R5 | Night listening | 12 windows of 20 s between 02:00 and 04:00 local time, clock drift under 1 min per month | Firmware sketch and RTC datasheet | Met on paper |
| R6 | Battery life | 5 years or more on one primary cell at the R5 schedule and one uplink a night | Power budget calculation | Met on paper: about 10 years (estimate) |
| R7 | Radio link | 90 % or more of nightly summaries delivered to a gateway within 1 km from a chamber with a cast-iron cover | Link budget at TRL 3; later a field check | **At risk:** cover loss is unknown and may block the link |
| R8 | Data and privacy | Only band levels and spectra leave the logger; raw vibration samples are deleted on the device after processing | Design review of the firmware sketch | Met by design |
| R9 | Attachment | Magnet holds 100 N or more on a steel or iron spindle cap, with no tools or pipe work | Magnet datasheet and a pull test later | Met for ferrous fittings; **not met** for brass, bronze or plastic fittings |
| R10 | Install from the surface | Placed and recovered in 10 min or less without entering the chamber, for chambers up to 1.5 m deep | Walk-through with the partner utility | Met on paper; not yet shown in the field |
| R11 | Survive the chamber | IP68: 1 m submersion for 7 days; operate from -20 to +50 °C | Design review; later a submersion test | Met on paper (sealed tube, IP68 connector) |
| R12 | Size and mass | Logger 70 mm diameter or less and 300 mm long or less; total mass 1.0 kg or less | Massing model | Met: 63 x 240 mm, about 0.7 kg (estimate) |
| R13 | Leak flag quality | 1 false alarm or fewer per 20 loggers per month after a 14-night baseline | Needs field data from a partner network | Unverified |
| R14 | Open and interoperable | Standard LoRaWAN 1.0.x uplink, documented payload, works with any network server and TwinKit | Design review | Met by design |
| R15 | Cost | Parts cost $130 or less per logger | Priced BOM | Met: about $108 (indicative) |

## Requirements not met or at risk

- **R2 at risk.** Leak noise attenuates quickly on plastic pipes ([Hunaidi and Chu, 1999](https://www.sciencedirect.com/science/article/pii/S0003682X99000134)), so 30 m may not be reachable with a low-cost sensor.
- **R7 at risk.** A cast-iron cover may block the LoRa link. Options (proposed, awaiting Amish): a composite cover, a through-cover antenna, or a lower spreading factor gateway placed nearby.
- **R9 not met** for non-ferrous fittings. A strap-on adapter would be needed.
- **R1, R4 and R13 unverified.** They depend on sensor noise, pipe attenuation and site background noise, which need calculation at TRL 3 and field data later.

## Assumptions

- Network pressure at night 2 to 6 bar; leaks at lower pressure are quieter.
- Valve spindle caps and hydrant bodies are cast iron or steel on most networks the lab would target first.
- A LoRaWAN gateway (TwinKit, a partner's or a public network) is within about 1 km in an urban area.
- Primary cell: lithium thionyl chloride C size, 3.6 V, about 7.7 Ah nominal, derated to 70 % usable for cold and pulse loads.

## Safety requirements

> **Safety:** S1: no confined space entry is needed to place, service or recover a logger. S2: the cell is a primary lithium cell with a fuse or PTC and reverse protection; no charging circuit is fitted. S3: the logger carries a label with the owner, a contact and a lithium cell warning. S4: nothing touches drinking water, and nothing is fixed to the pipe other than the magnet.
