---
doc_id: LKL-PRC-001
title: LeakListen design precis
project: LeakListen
doc_type: Design precis
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
  change: TRL 2 concept, components, first-order numbers, safety and open questions
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 design choices adopted for TRL 3 (LKL-DDR-001); numbers replaced by LKL-CAL-001; 53 g seismic mass, 24-byte summary, regional transmit power, weekly time correction; links to the model and LKL-DWG-001
---

# LeakListen design precis

## Summary

LeakListen is a battery-powered acoustic leak logger that hangs under a valve chamber cover, sticks a magnetic vibration sensor onto the valve spindle cap, listens to the pipe for a few minutes each night, and sends one small LoRaWAN summary a day. A leak on a pressurized main makes a steady hiss that travels along the pipe wall; when a logger's quietest night-time level rises and stays up for several nights, the server flags that street for a follow-up survey. The TRL 3 calculations (LKL-CAL-001) give about 1.2 mAh a day, 10 years or more on one C-size lithium cell, 0.93 kg and $109.00 in parts. They also show the two weak points: the reference leak is heard about 185 m along an iron main but only a few metres along a plastic one (R2 not met), and the radio reaches about 0.5 km, not 1 km, from under a cast-iron cover (R7 not met).

Figure 1. Concept in a valve chamber, street and chamber shown in section ([media/hero.png](../media/hero.png)). Figure 2. Exploded view with BOM numbers ([media/exploded.png](../media/exploded.png)). Figure 3. Cutaway of the logger and sensor ([media/cutaway.png](../media/cutaway.png)). Figure 4. Nightly data flow ([media/flow.png](../media/flow.png)). Figure 5. General arrangement, drawing LKL-DWG-001 Rev P1 ([cad/drawings/LKL-DWG-001.pdf](../cad/drawings/LKL-DWG-001.pdf)), from the parametric model [cad/src/model.py](../cad/src/model.py).

## How it works

1. **Place from the surface.** A technician lifts the cover, lowers the sensor puck on its cable with a pole until the magnet snaps onto the valve spindle cap, and hooks the hanger over the cover frame so the logger hangs in the opening and the flat antenna sits just under the cover. Nobody enters the chamber.
2. **Listen at night.** A real-time clock wakes the logger between 02:00 and 04:00, when demand and traffic noise are lowest. It records 12 windows of 20 s at 8 kS/s from the piezo sensor through a charge preamplifier and a 24-bit ADC. Once a week it asks the network for the time (LoRaWAN 1.0.3 DeviceTimeReq) so the clock stays within 20 s.
3. **Process on the device.** For each window the microcontroller computes the RMS level and a 64-band spectrum from 5 Hz to 2 kHz, in fixed point, with three FFT stages at 8,000, 1,000 and 250 S/s so that even the 0.49 Hz wide bottom band is resolved. It keeps the minimum and the 10th percentile level across the night (leaks are steady; traffic and water use are not) and a band spectrum. Raw samples are then deleted.
4. **Send one summary.** 24 bytes (two night levels, 16 band levels, peak band, steadiness, battery voltage, temperature, flags) go by LoRaWAN to any network server, such as the lab's TwinKit gateway, at +14 dBm in EU868 or up to +20 dBm in US915. The frame fits every EU868 rate and US915 at SF9 or faster.
5. **Flag on the server.** After a 14-night baseline, a logger whose night-time minimum rises by a set margin and stays up for 3 or more nights, with a steady narrow-band spectrum, is flagged. A crew then pinpoints with a ground microphone or a correlator.

## Main components

Numbers match the exploded view and [bom/bom.csv](../bom/bom.csv).

Table 1. Main components.

| No. | Component | Key figures | Role |
| --- | --- | --- | --- |
| 1 | Sensor puck body | Aluminium, 40 mm diameter x 42 mm, potted | Stiff, sealed carrier for the sensor and preamplifier |
| 2 | Pot magnet | 32 mm, about 290 N nominal pull on thick flat steel | Attaches to the spindle cap with no tools |
| 3 | Piezo disc and seismic mass | 27 mm brass-backed piezo disc in compression under a 20 x 20 mm brass mass, about 53 g; about 157 pC/g | Turns pipe vibration into charge |
| 4 | Charge preamplifier | Low-noise JFET-input stage, 1 nF and 53 MΩ feedback (3 Hz high-pass), then 40 dB; about 1.0 µg/√Hz | Low-noise, low-frequency front end (R3, R4) |
| 5 | Sensor cable | 2 m shielded PUR, M12 IP68 plug | Lets the puck sit on the valve while the logger stays near the cover |
| 6 | Logger housing | 63 mm PVC tube, 240 mm, two O-ring end caps, M12 socket | IP68 enclosure (R11) |
| 7 | Main board | STM32WL LoRaWAN module (FieldNode core), 24-bit audio ADC, RTC, hybrid layer capacitor of 0.1 F or more | Scheduling, spectrum, radio |
| 8 | Primary cell | Li-SOCl2, C size, 3.6 V, about 7.7 Ah | Years of life without charging (R6) |
| 9 | Hanger strap and hook | Stainless strap hooked over the cover frame | Surface installation (R10) |
| 10 | Flat LoRa antenna | About 70 mm disc on the hanger, 1 m lead | Radio as close to the cover as possible (R7) |

## Key design choices

These choices were proposed at TRL 2 and are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (LKL-DDR-001).

- **Contact sensor on the valve, not a hydrophone.** A magnet-on sensor needs no pipe tapping and no contact with drinking water. Hydrophones hear further on plastic pipes but need a hydrant or tapping point; this is kept as an option for plastic networks (D3), and LKL-CAL-001 shows it is needed to hear any distance on PVC or PE.
- **Noise-level screening, not correlation.** Correlation needs time-synchronized raw audio from pairs of loggers and much more data over the radio. Nightly level and spectrum screening fits LoRaWAN and a primary cell (D1); correlation is recorded as a later variant.
- **Primary cell, not solar.** A chamber has no sun, and a lithium thionyl chloride cell has very low self-discharge. A hybrid layer capacitor supplies the radio pulses the cell cannot deliver alone. A C-size cell (D5) gives 10 years or more.
- **Reuse the FieldNode radio core.** The STM32WL module, payload conventions and network settings are shared with FieldNode so fixes carry across; FieldNode's solar charger and enclosure are not used (D4). Transmit power and the link budget method follow FieldNode's FND-CAL-001.
- **Compression-mode sensor with a heavy mass.** A 53 g brass mass on the disc in compression gives five times the TRL 2 sensitivity while keeping the sensor's own resonance near 200 kHz, far above the band. A disc used as a bender would be as sensitive but would resonate inside the band.
- **Privacy by design.** Raw samples never leave the logger (R8, a fixed requirement under D6). A contact sensor on a valve is a poor microphone, but the rule keeps the design acceptable for street deployment.

## Key numbers (LKL-CAL-001)

All values come from LKL-CAL-001 and `docs/04-calcs/sizing.py`; they are first-principles estimates on assumed data.

Table 2. Key numbers.

| Quantity | Value | Requirement |
| --- | --- | --- |
| Data sampled and sent per night | 3.84 MB sampled and deleted; 24 bytes sent | R8, R14 |
| Daily charge | 1.15 mAh (EU868 SF7) to 1.22 mAh (EU868 SF12) | R6 |
| Battery life on energy | 10.3 to 12.8 years; taken as 10 years | R6 (5 years) |
| Airtime | 1.97 s per uplink at SF12; 5.9 s a day worst case | R14 |
| Link under an iron cover (20 dB assumed) | -9.7 dB at 1 km; about 0.53 km range (EU868 SF12) | **R7 not met** |
| Detection distance, reference leak | About 185 m on ductile iron (93 to 370 m); about 4 m on PVC | R1 at risk, **R2 not met** |
| Sensor self-noise | 1.03 µg/√Hz worst from 100 Hz to 1 kHz | R4 at risk |
| Mounted resonance | About 780 to 1,550 Hz | R3 at risk |
| Magnet hold on iron | 149 N bare, 90 N at a 0.3 mm coating | R9 at risk |
| Clock | 20 s worst with a weekly time correction | R5 |
| Size and mass | 63 x 240 mm tube, 267 mm overall; 0.93 kg | R12 |
| Parts cost | $109.00 against $130 | R15 |

**Energy.** Listening, 12 mA for about 252 s a night, is 59 % of the worst day; sleep at 4 µA and the cell's own self-discharge make up most of the rest. The radio adds only 0.005 to 0.08 mAh a day at +14 dBm.

**Radio.** The flat antenna under the cover is the weak link. To close 1 km, the cover may cost no more than about 10 dB, which suggests a through-cover antenna, a composite cover or a closer gateway; the choice is proposed in `docs/REVIEW.md`, awaiting Amish.

**Cost.** $109.00 in parts (see [bom/bom.csv](../bom/bom.csv)), under the $130 budget.

## Safety

> **Safety:** Valve chambers can be confined spaces with low oxygen or toxic gas. LeakListen is designed to be placed from the surface; nobody should enter a chamber without the utility's confined space permit, gas testing and a trained standby person. Covers can weigh 30 kg or more: use a lifting key, lift with the legs and keep feet clear. Street work needs traffic management and high-visibility clothing under local rules.
>
> The lithium thionyl chloride primary cell can vent, burn or explode if shorted, crushed, heated above its rating or charged. Fit a fuse or PTC and reverse protection, never fit a charging circuit, and store and ship cells under the dangerous goods rules for lithium metal cells.
>
> The pot magnet can pinch fingers and affect pacemakers and implanted devices. Carry it with its keeper plate fitted.
>
> Placing anything on a public water network needs the utility's written permission. Nothing in LeakListen touches drinking water.

## Open questions

- [ ] Detection distance on iron and plastic pipes (R1, R2): estimated in LKL-CAL-001, but the leak source strength and pipe losses need field recordings of known leaks.
- [ ] Radio loss through cast-iron, ductile iron and composite covers (R7): assumed 10 to 30 dB in LKL-CAL-001, not measured. Through-cover antenna, composite cover or closer gateway: proposed, awaiting Amish.
- [ ] Sensor self-noise (R4): 1.03 µg/√Hz on assumed data; the ceramic's d33 and the op-amp noise need checking against chosen parts.
- [ ] Threshold rules for the leak flag, and how to handle pumps, pressure reducing valves and night-time customer use (R13).
- [ ] Adapter for brass, bronze and plastic fittings, and a 42 mm magnet for coated caps (R9; the magnet is proposed, awaiting Amish).
- [ ] Whether time synchronization for correlation between neighboring loggers is worth adding later.
- [ ] Whether a logger calibration check (a small shaker bench) belongs in this repo or in CalRig, which today covers temperature, humidity and particles only.
