---
doc_id: LKL-PRC-001
title: LeakListen design precis
project: LeakListen
doc_type: Design precis
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
  change: TRL 2 concept, components, first-order numbers, safety and open questions
---

# LeakListen design precis

## Summary

LeakListen is a battery-powered acoustic leak logger that hangs under a valve chamber cover, sticks a magnetic vibration sensor onto the valve spindle cap, listens to the pipe for a few minutes each night, and sends one small LoRaWAN summary a day. A leak on a pressurized main makes a steady hiss that travels along the pipe wall; when a logger's quietest night-time level rises and stays up for several nights, the server flags that street for a follow-up survey. First-order estimates: about 1 mAh a day, about 10 years on one C-size lithium cell, and about $108 in parts. The concept is at TRL 2; detection distance, sensor noise and the radio link from under a cast-iron cover are not yet verified.

Figure 1. Concept in a valve chamber, street and chamber shown in section ([media/hero.png](../media/hero.png)). Figure 2. Exploded view with BOM numbers ([media/exploded.png](../media/exploded.png)). Figure 3. Cutaway of the logger and sensor ([media/cutaway.png](../media/cutaway.png)). Figure 4. Nightly data flow ([media/flow.png](../media/flow.png)).

## How it works

1. **Place from the surface.** A technician lifts the cover, lowers the sensor puck on its cable with a pole until the magnet snaps onto the valve spindle cap, and hooks the hanger over the cover frame so the logger hangs in the opening and the flat antenna sits just under the cover. Nobody enters the chamber.
2. **Listen at night.** A real-time clock wakes the logger between 02:00 and 04:00, when demand and traffic noise are lowest. It records 12 windows of 20 s at 8 kS/s from the piezo sensor through a charge preamplifier and a 24-bit ADC.
3. **Process on the device.** For each window the microcontroller computes the RMS level and a 64-band spectrum from 5 Hz to 2 kHz. It keeps the minimum and the 10th percentile level across the night (leaks are steady; traffic and water use are not) and a band spectrum. Raw samples are then deleted.
4. **Send one summary.** About 50 bytes (levels, spectral shape, battery voltage, temperature) go by LoRaWAN to any network server, such as the lab's TwinKit gateway.
5. **Flag on the server.** After a 14-night baseline, a logger whose night-time minimum rises by a set margin and stays up for 3 or more nights, with a steady narrow-band spectrum, is flagged. A crew then pinpoints with a ground microphone or a correlator.

## Main components

Numbers match the exploded view and [bom/bom.csv](../bom/bom.csv).

Table 1. Main components.

| No. | Component | Key figures | Role |
| --- | --- | --- | --- |
| 1 | Sensor puck body | Aluminium, 40 mm diameter x 34 mm, potted | Stiff, sealed carrier for the sensor and preamplifier |
| 2 | Pot magnet | 32 mm, about 290 N nominal pull on thick flat steel | Attaches to the spindle cap with no tools |
| 3 | Piezo disc and seismic mass | 27 mm brass-backed piezo disc with a small brass mass | Turns pipe vibration into charge |
| 4 | Charge preamplifier | Low-noise JFET-input stage, high-pass near 3 Hz, gain about 40 dB | Low-noise, low-frequency front end (R3, R4) |
| 5 | Sensor cable | 2 m shielded PUR, M12 IP68 plug | Lets the puck sit on the valve while the logger stays near the cover |
| 6 | Logger housing | 63 mm PVC tube, 240 mm, two O-ring end caps, M12 socket | IP68 enclosure (R11) |
| 7 | Main board | STM32WL LoRaWAN module (FieldNode core), 24-bit audio ADC, RTC, hybrid layer capacitor | Scheduling, spectrum, radio |
| 8 | Primary cell | Li-SOCl2, C size, 3.6 V, about 7.7 Ah | Years of life without charging (R6) |
| 9 | Hanger strap and hook | Stainless strap hooked over the cover frame | Surface installation (R10) |
| 10 | Flat LoRa antenna | About 70 mm disc on the hanger, 1 m lead | Radio as close to the cover as possible (R7) |

## Key design choices

- **Contact sensor on the valve, not a hydrophone.** A magnet-on sensor needs no pipe tapping and no contact with drinking water. Hydrophones hear further on plastic pipes but need a hydrant or tapping point; this is recorded as an option.
- **Noise-level screening, not correlation.** Correlation needs time-synchronized raw audio from pairs of loggers and much more data over the radio. Nightly level and spectrum screening fits LoRaWAN and a primary cell; correlation is left as an open question.
- **Primary cell, not solar.** A chamber has no sun, and a lithium thionyl chloride cell has very low self-discharge. A hybrid layer capacitor supplies the radio pulses the cell cannot deliver alone.
- **Reuse the FieldNode radio core.** The STM32WL module, payload conventions and network settings are shared with FieldNode so fixes carry across; FieldNode's solar charger and enclosure are not used.
- **Privacy by design.** Raw samples never leave the logger (R8). A contact sensor on a valve is a poor microphone, but the rule keeps the design acceptable for street deployment.

## First-order numbers

All values are estimates to be checked at TRL 3.

**Data per night.** 12 windows x 20 s x 8,000 samples/s x 2 bytes = 3.84 MB sampled; 12 spectra x 64 bands x 2 bytes = about 1.5 kB kept in RAM; about 50 bytes sent (Figure 4).

**Energy per day.** Assumptions: sleep current 4 µA; 12 mA while sampling and processing; 3 uplinks a day (one plus up to two retries) of 0.4 s at 120 mA (20 dBm, needed for cover loss).

Table 2. Daily energy budget (estimate).

| Item | Calculation | mAh per day |
| --- | --- | --- |
| Sleep | 0.004 mA x 24 h | 0.10 |
| Listening and processing | 12 mA x 240 s / 3,600 | 0.80 |
| Radio | 3 x 0.4 s x 120 mA / 3,600 | 0.04 |
| Cell self-discharge | about 1 % a year of 7.7 Ah | 0.21 |
| **Total** | | **about 1.15** |

**Battery life.** 7.7 Ah x 70 % usable = 5.4 Ah; 5,400 / 1.15 = about 4,700 days, or about 12.8 years. Life is taken as about 10 years, limited by cell and seal aging rather than energy (R6: 5 years).

**Magnet hold.** A 32 mm pot magnet is rated about 290 N on thick flat steel. On a small square spindle cap with paint and rust, a third of that (about 95 N) is a plausible hold; R9 asks for 100 N, so this is marginal and needs a pull check.

**Cost.** About $108 in parts (see [bom/bom.csv](../bom/bom.csv)), under the $130 budget.

## Safety

> **Safety:** Valve chambers can be confined spaces with low oxygen or toxic gas. LeakListen is designed to be placed from the surface; nobody should enter a chamber without the utility's confined space permit, gas testing and a trained standby person. Covers can weigh 30 kg or more: use a lifting key, lift with the legs and keep feet clear. Street work needs traffic management and high-visibility clothing under local rules.
>
> The lithium thionyl chloride primary cell can vent, burn or explode if shorted, crushed, heated above its rating or charged. Fit a fuse or PTC and reverse protection, never fit a charging circuit, and store and ship cells under the dangerous goods rules for lithium metal cells.
>
> The pot magnet can pinch fingers and affect pacemakers and implanted devices. Carry it with its keeper plate fitted.
>
> Placing anything on a public water network needs the utility's written permission. Nothing in LeakListen touches drinking water.

## Open questions

- [ ] Detection distance on iron and on plastic pipes with a low-cost piezo sensor (R1, R2); needs an attenuation estimate at TRL 3.
- [ ] Radio loss through cast-iron, ductile iron and composite covers (R7); through-cover antenna or composite cover?
- [ ] Sensor self-noise of a piezo disc with a charge amplifier against a commercial accelerometer (R4).
- [ ] Threshold rules for the leak flag, and how to handle pumps, pressure reducing valves and night-time customer use (R13).
- [ ] Adapter for brass, bronze and plastic fittings (R9).
- [ ] Whether time synchronization for correlation between neighboring loggers is worth adding later.
- [ ] Whether a logger calibration check (a small shaker bench) belongs in this repo or in CalRig, which today covers temperature, humidity and particles only.
