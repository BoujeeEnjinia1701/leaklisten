---
doc_id: LKL-CAL-001
title: LeakListen sizing calculations
project: LeakListen
doc_type: Calculation
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (data and processing, airtime, energy and battery life, link budget through the cover, leak noise attenuation, sensor noise and resonances, detection distance, clock, magnet hold, chamber survival, size and mass, installation, false alarms, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002): 42 mm magnet fitted; R2 restated for the hydrophone variant; R7 against a gateway within 0.5 km under iron covers; results re-run"
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Constructable design (LKL-DDR-003): mass, cost, resonance, flooding, cable reach and install time re-run; R12 not met on mass; cost reported against the value-engineering target"
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R12 status from Amish's 2026-10-02 restatement (LKL-DDR-003 A1): met on paper. Figures not rerun; sizing.py still prints the 1.0 kg total-mass target"
---

# LeakListen sizing calculations

On paper, LeakListen meets seven of its fifteen requirements (four on paper, three by design), has four at risk, misses none (R12, mass, was missed once the constructable design added a neck bar hanger, LKL-DDR-003, until Amish restated it for the logger, cable and sensor on 2026-10-02), is USD 11 over its value-engineering target on cost (R15), leaves two that cannot be checked until there is field data and leaves one (R2) open until the hydrophone variant is sized. Version 0.1 of this note found two misses. R7 (radio link) was not met at 1 km: with a flat antenna under a cast-iron cover, and an assumed 20 dB cover loss, the link closes to about 0.53 km. Under LKL-DDR-002 a gateway is now planned within 0.5 km of each district with iron covers, and R7 is at risk rather than not met, because the margin at 0.5 km is only +0.9 dB and the cover loss is unmeasured. R2 (plastic mains) was not met: a contact sensor on a valve hears the reference leak only a few metres along PVC or PE pipe. R2 now applies to the hydrophone variant, and the contact sensor's scope is metallic mains. The 42 mm magnet fitted under LKL-DDR-002 moves R9 to met on paper. On iron mains the central estimate is about 185 m against the 100 m target, but the range spans about 93 to 370 m for plausible pipe losses, so R1 is at risk rather than met. The calculations changed four things in the TRL 2 concept: the seismic mass grows from about 11 g to about 53 g so that the sensor meets its noise target, the nightly summary shrinks from about 50 to 24 bytes so that it fits every LoRaWAN region, transmit power follows the regional limit (+14 dBm in EU868, not +20 dBm), and the clock is corrected weekly by the network. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C1], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace confined space procedures, a lithium cell safety review or the utility's permission. Valve chambers can hold low-oxygen or toxic air; nothing in this note needs anyone to enter one. See LKL-PRC-001, Safety.

## Scope and method

The note checks every requirement in LKL-REQ-001 v0.5 against the design in LKL-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and part solids, so the puck, seismic mass, logger tube, cable run and part volumes used here are the ones in the STEP files and in drawing LKL-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes the status table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is a DN150 gate valve in a concrete chamber under a cast-iron cover, with the spindle cap 0.48 m below the street, a network pressure of 3 bar (44 psi) at night, and a LoRaWAN gateway 30 m up in an urban area, 0.5 km away in districts with iron covers (LKL-DDR-002) and 1 km away elsewhere.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Electronics | Sleep 4 µA; 12 mA while sampling and processing; 1 s of preamplifier settling per window; two 0.2 s receive windows at 5 mA per uplink | STM32WL-class figures; to confirm from the chosen module's datasheet |
| Radio | +14 dBm at 45 mA (EU868, as FieldNode); +20 dBm at 120 mA (US915); up to 3 transmissions a night | FieldNode FND-CAL-001 for EU868; the TRL 2 figure for US915 |
| Cell | Li-SOCl2 C, 7.7 Ah, 70 % usable, 1 % a year self-discharge; carries up to 30 mA, the capacitor the rest | Typical bobbin cell; check against the chosen cell |
| Link | 6 dB receiver noise figure; LoRa SNR limits -7.5 dB (SF7) to -20 dB (SF12); node antenna -3 dBi near the cover, 0.5 dB lead; gateway 2 dBi, 2 dB feeder; 10 dB fade margin; Okumura-Hata urban model at a 1 m mobile height | As FieldNode, with an urban rather than suburban path |
| Cover loss | 10 dB composite cover; 20 dB cast-iron cover (central); 30 dB tight cover over a flooded chamber | Assumed, no verified source; the largest single uncertainty in R7 |
| Pipe waves | Fluid-dominated axial wave below the ring frequency, wavenumber k = k_f √(1 + 2Ba/(Eh(1 + iη))), model form after Gao et al. (2004); water B 2.2 GPa, 1,480 m/s | [Gao, Brennan, Joseph, Muggleton and Hunaidi, *J. Sound Vib.* 277 (2004) 133 to 148](https://www.sciencedirect.com/science/article/pii/S0022460X03011647) |
| Pipes | Ductile iron 170 GPa, 6 mm wall; cast iron 100 GPa, 10 mm; PVC 3.3 GPa, 7.7 mm; PE100 1.2 GPa, 14.6 mm; loss factor including soil coupling 0.02 (iron), 0.065 (PVC), 0.10 (PE) | Handbook moduli; loss factors assumed |
| Leak source | 5 L/min at 3 bar through a sharp orifice (Cd 0.6); acoustic efficiency 1e-6 to 1e-4 of the jet's mechanical power (central 1e-5), half into each direction, flat spectrum from 5 Hz to 2 kHz | Flat spectrum as in Gao et al. (2004); efficiency assumed |
| Sensing | Sensor acceleration = -10 dB coupling times the hoop acceleration of a ductile iron valve body (80 mm radius, 10 mm wall) | Assumed; the valve, not the pipe, is what the magnet touches |
| Background | Night vibration on the spindle cap 0.5 µg/√Hz above 100 Hz, rising as 1/f below | Assumed; site data will replace it |
| Sensor | Soft PZT, d33 300 pC/N; 20 mm ceramic, 0.23 mm, εr 1,800, tan δ 0.02; JFET op-amp 5 nV/√Hz with a 10 Hz 1/f corner; 1 nF feedback, 3 Hz high-pass | Typical buzzer ceramic and op-amp figures |
| Magnet | Rated pull 600 N (42 mm, fitted) or 290 N (32 mm, v0.1) on thick mild steel; 0.7 on cast or ductile iron; pull falls as 1/(1 + g/0.6 mm)² with a coating gap g | Assumed gap law; to check against a supplier's curve |
| Clock | 32.768 kHz crystal, ±20 ppm at 25 °C, -0.034 ppm/°C² | Typical tuning-fork crystal |

## A. Nightly data, processing and payload (R5, R8, R14)

- **Data.** Twelve 20 s windows at 8 kS/s and 16 bits are 3.84 MB a night; 12 spectra of 64 bands, 1.54 kB, stay in RAM [A1]. Raw samples are processed as they arrive and never stored.
- **Resolution.** The 64 bands spaced evenly on a log scale from 5 Hz to 2 kHz are only 0.49 Hz wide at the bottom. A three-stage multirate scheme resolves every band: a 1,024-point FFT at the full rate for 80 Hz to 2 kHz, the same after decimating by 8 for 10 to 80 Hz, and a 512-point FFT after decimating by 32 for 5 to 10 Hz [A2].
- **Memory.** The signal path needs about 22 kB, and with a 32 kB allowance for the LoRaWAN stack the total is 54 kB of the STM32WLE5's 64 kB. The STM32WL has no floating-point unit, so processing is fixed point (q15) [A3].
- **Payload.** The TRL 2 summary of about 50 bytes does not fit US915's slowest rate (11 bytes at SF10) and takes 2.8 s at SF12. The summary is now 24 bytes: night minimum and 10th percentile levels, 16 band levels in 1 dB steps (the 64 bands merged four to one), the peak band, a steadiness index, battery, temperature, flags and a sequence number [A4]. The full 64-band spectrum stays on the device and can be requested later.

## B. LoRaWAN airtime (R7, R14)

- **Time on air.** With 13 bytes of LoRaWAN overhead the 37-byte frame takes 82 ms at SF7, 267 ms at SF9, 494 ms at SF10 and 1.97 s at SF12 [B1].
- **Regional limits.** 24 bytes fits EU868 at every rate and US915 at SF9 or faster, within its 400 ms dwell limit (267 ms) [B2].
- **Fair use.** Three transmissions at SF12 use 5.9 s a day, 20 % of The Things Network's 30 s fair-use allowance, and each needs 197 s of silence under the 1 % duty cycle [B3]. R14 is met by design.

## C. Energy and battery life (R6)

*Table 2. Daily charge and battery life [C1].*

| Case | Sleep | Listening | Radio | Self-discharge | Total | Life on energy |
| --- | --- | --- | --- | --- | --- | --- |
| EU868 SF7 +14 dBm | 0.096 | 0.840 | 0.005 | 0.211 | 1.15 mAh | 12.8 years |
| EU868 SF12 +14 dBm | 0.096 | 0.840 | 0.076 | 0.211 | 1.22 mAh | 12.1 years |
| US915 SF9 +20 dBm | 0.096 | 0.840 | 0.028 | 0.211 | 1.18 mAh | 12.6 years |
| TRL 2 case, 50 bytes at SF12, +20 dBm | 0.096 | 0.840 | 0.281 | 0.211 | 1.43 mAh | 10.3 years |

- **R6 is met on paper.** Every case gives 10.3 years or more on 5.39 Ah usable; life is still taken as 10 years, limited by cell and seal ageing. Listening, not radio, dominates: 59 % of the worst day [C2]. The TRL 2 figure of about 1.15 mAh a day stands for the EU868 case.
- **Pulse capacitor.** A bobbin cell carrying 30 mA leaves 0.06 F of capacitance to cover an EU868 SF12 burst and 0.05 F for US915 SF9, over a 0.5 V droop; a +20 dBm burst as long as SF12 would need 0.36 F [C3]. The main board specifies a hybrid layer capacitor of 0.1 F or more.

## D. Radio link from under the cover (R7)

*Table 3. Link margin at 1 km after the 10 dB fade margin, and the range at zero margin [D1], [D2].*

| Radio | Link budget | Composite cover (10 dB) | Iron cover (20 dB) | Tight iron cover, flooded (30 dB) |
| --- | --- | --- | --- | --- |
| EU868 SF12, +14 dBm | 147.5 dB | +0.3 dB; 1.02 km | **-9.7 dB; 0.53 km** | **-19.7 dB; 0.28 km** |
| US915 SF9, +20 dBm | 146.0 dB | **-1.8 dB; 0.89 km** | **-11.8 dB; 0.46 km** | **-21.8 dB; 0.24 km** |
| EU868 SF7, +14 dBm | 135.0 dB | **-12.2 dB; 0.45 km** | **-22.2 dB; 0.23 km** | **-32.2 dB; 0.12 km** |

Bold values miss 1 km. The urban Hata path loss at 1 km is 127.3 dB at 868 MHz and 127.9 dB at 915 MHz.

*Table 3a. Link margin at 0.5 km, the planned gateway distance under iron covers (LKL-DDR-002), after the 10 dB fade margin [D5].*

| Radio | Iron cover (20 dB) | Tight iron cover, flooded (30 dB) |
| --- | --- | --- |
| EU868 SF12, +14 dBm | +0.9 dB | **-9.1 dB** |
| US915 SF9, +20 dBm | **-1.2 dB** | **-11.2 dB** |
| EU868 SF7, +14 dBm | **-11.6 dB** | **-21.6 dB** |

- **R7 is at risk.** Under the central iron cover the link reaches about 0.53 km at the slowest EU868 rate and 0.46 km at US915 SF9. R7 is restated under LKL-DDR-002 against a gateway within 0.5 km of each district with iron covers; the EU868 link closes there with +0.9 dB to spare, the US915 link misses by 1.2 dB, and a tight cover over a flooded chamber misses by about 9 dB [D5]. To close 1 km the cover may cost no more than 10.3 dB (EU868 SF12) or 8.2 dB (US915 SF9) [D3], which only a composite cover or a through-cover antenna is likely to give; that remains the option where a utility agrees.
- **Transmit power.** EU868 limits the uplink to 14 dBm ERP (16.15 dBm EIRP), so the TRL 2 assumption of +20 dBm is not permitted there [D4]; the design now uses +14 dBm in EU868, as FieldNode does, and up to +20 dBm in US915.
- **Decision.** Decided by Amish, 2026-09-25 (LKL-DDR-002): measure the cover loss first, then plan a gateway within about 0.5 km of each district as the default, with a through-cover antenna or composite cover where a utility agrees. The cover loss measurement is TRL 4 work and on hold; until then the 20 dB figure is an assumption.

## E. Leak noise attenuation along the pipe (R1, R2)

- **Wave speed.** The fluid-dominated wave travels at about 1,270 m/s in the iron mains and 394 m/s (PVC) and 338 m/s (PE) in the plastic ones, because a compliant wall slows it [E1].
- **Attenuation.** On ductile iron it is 0.011 dB/m at 100 Hz and 0.11 dB/m at 1 kHz; on PVC 0.42 dB/m at 100 Hz and 4.2 dB/m at 1 kHz; on PE nearly twice the PVC figure [E1]. Over 100 m of iron, a 200 Hz tone loses 2.2 dB; over 30 m of PVC it loses 25.1 dB and a 50 Hz tone 6.3 dB [E2]. This agrees in kind with the low-frequency, narrow-band leak signals on plastic pipes that Gao et al. (2004) and Hunaidi and Chu (1999, cited in LKL-PRB-001) describe.

## F. Sensor: sensitivity, self-noise and resonances (R3, R4)

- **Sensitivity.** In compression, a piezo disc's charge output is d33 times the seismic mass. The TRL 2 mass of about 11 g gives 32 pC/g; the TRL 3 mass, a brass cylinder 20 mm x 20 mm of about 53 g, gives 157 pC/g. The disc has 21.8 nF; the charge amplifier uses 1 nF and 53 MΩ [F1].
- **Self-noise.** Op-amp voltage noise across the disc capacitance, the feedback resistor's current noise and the disc's dielectric loss give 1.03 µg/√Hz at 100 Hz, 0.83 at 300 Hz and 0.76 at 1 kHz, and 2.95 µg/√Hz at 10 Hz. With the TRL 2 mass the figures were five times higher [F2]. The worst value from 100 Hz to 1 kHz is 1.03 µg/√Hz against the 1 µg/√Hz target [F3], so **R4 is at risk**, 3 % over the target on assumed ceramic and op-amp data. The ADC's contribution is negligible after the 40 dB stage [F4].
- **Seismic resonance.** In compression the disc and mass resonate far above the band, near 200 kHz [F5]. A disc used as a bender, the other way to raise sensitivity, would resonate inside the band.
- **Mounted resonance.** With the 42 mm magnet and the 8 mm puck base of LKL-DDR-003 the puck and magnet weigh about 277 g (262 g in v0.2, 210 g with the 32 mm magnet of v0.1). On a contact stiffness of 5 to 20 MN/m, typical of a magnet on a painted cap but assumed, they resonate at 676 to 1,352 Hz and stay within 3 dB only up to 366 to 732 Hz [F6]; the heavier magnet and base lower both by about 13 %. A fixed correction cannot remove a resonance that changes from site to site, so **R3 is at risk** above about 370 Hz. This matters for R1: the band that sets the detection distance on iron is the 800 Hz third octave (section G), at the edge of the flat range. Near the resonance the mount amplifies the leak and the background alike, so the level is site-dependent rather than lost; the nightly trend compares a logger with itself, which tolerates this better than an absolute threshold would.

## G. Detection distance (R1, R2)

The reference leak (5 L/min at 3 bar) is a 24.5 m/s jet through a 2.7 mm orifice, 25 W of mechanical power at a Mach number of 0.017 [G1]. The script spreads a fraction of that power over the pipe as a flat spectrum, turns the in-pipe pressure into valve acceleration and, in each third-octave band, finds the distance at which the attenuated leak level falls to the combined background and sensor noise. At that distance the band level rises by 3 dB, enough for the nightly minimum to show it.

*Table 4. Detection distance for the reference leak [G2].*

| Pipe | Efficiency 1e-6 | Efficiency 1e-5 (central) | Efficiency 1e-4 | Target |
| --- | --- | --- | --- | --- |
| Ductile iron DN150 | 105 m | 185 m | 325 m | 100 m (R1) |
| Cast iron DN150 | 99 m | 175 m | 308 m | 100 m (R1) |
| PVC DN150 | 2 m | 4 m | 7 m | 30 m (R2) |
| PE100 DN150 SDR11 | 1 m | 2 m | 4 m | 30 m (R2) |

- **Limiting band.** The detection distance is set by the 800 Hz third octave on iron and the 1 kHz band on plastic [G2]. Leak pressure turns into valve acceleration in proportion to the square of frequency, so the higher bands win until pipe attenuation takes over.
- **R1 is at risk.** The central estimate on ductile iron is 185 m, but halving or doubling the pipe loss factor moves it to 370 m or 93 m [G3], and the source efficiency spans a factor of 100. Only field recordings of known leaks can pin these down.
- **R2 is not met.** A contact sensor on a valve hears only a few metres along a plastic main in this model; halving the pipe loss factor gives 8 m [G3]. The model is pessimistic at low frequency, because a stiff metal valve body converts pressure into very little acceleration there, and practice with hydrophones on plastic mains reaches further. That is the case for the hydrophone variant kept open in decision D3. Under LKL-DDR-002 the contact sensor's scope is metallic mains and R2 applies to the hydrophone variant, which is not sized in this note; the contact sensor figures above are kept for the record.

## H. Clock (R5)

- **Free running.** A ±20 ppm crystal in a chamber at 5 to 20 °C drifts by 54 to 87 s in 30 days [H1], which misses the 1 min a month in R5.
- **Corrected.** A weekly network time request (LoRaWAN 1.0.3 DeviceTimeReq, answered by any compliant network server) holds the error to 20 s at worst [H2]. **R5 is met on paper** with that correction, which is now part of the design.

## I. Magnet hold (R9)

*Table 5. Pull on a cast or ductile iron spindle cap [I1].*

| Magnet | 0.1 mm gap (bare) | 0.3 mm (paint) | 0.5 mm (paint and rust) | 1.0 mm (heavy coating) |
| --- | --- | --- | --- | --- |
| 32 mm pot, 290 N rated (v0.1, replaced) | 149 N | **90 N** | **60 N** | **29 N** |
| 42 mm pot, about 600 N rated (fitted) | 309 N | 187 N | 125 N | **59 N** |

- **R9 is met on paper.** The 32 mm magnet of v0.1 met 100 N only on a bare or lightly coated cap. The 42 mm magnet fitted under LKL-DDR-002 (it fits the 50 mm cap) meets it up to a 0.5 mm coating, and only a heavy 1 mm coating defeats it. The magnet itself carries only about 3.0 N of static load, since the puck sits on top of the cap [I2]; the 100 N target covers a snagged cable or a knock. Non-ferrous caps, outside R9's target, still need an adapter. The larger magnet roughly doubles the pinch hazard; it ships with its keeper plate fitted.

## J. Chamber survival (R11)

- **Submersion.** 1 m of water puts 9.8 kPa on the O-rings and the M12 socket [J1], well within the rating of static O-ring seals and IP68 connectors.
- **Flooding.** The logger body (tube, flanged plugs, fittings, chassis and electronics) weighs about 551 g and displaces 748 g of water, so in a flooded chamber it floats up against the lanyard with 1.9 N [J2]. The lanyard, eye bolt and neck bar carry that by a wide margin.
- **Condensation.** The free air in the tube holds about 5 mg of water at saturation; a 10 g silica gel pack holds about 2,000 mg [J3]. Long-term vapour ingress through the seals cannot be estimated on paper. **R11 is met by design**; a submersion test is TRL 4 work and on hold.

## K. Size, mass and installation (R10, R12)

- **Size and mass.** The logger is 63 mm in diameter (68 mm over the radial screw heads) and 240 mm long flange to flange, 283 mm with its socket and eye bolt, within R12's 70 x 300 mm. Made parts are weighed from their model volume and material, bought parts from catalogue figures. The whole set weighs 1.35 kg [K1]: the housing with its acetal plugs 365 g, the neck bar with feet and lanyard 322 g, the cable 140 g, the magnet 126 g, the cell 90 g, the puck body 78 g and the antenna 70 g. The logger, cable and sensor alone weigh 0.96 kg. The neck bar that replaced the concept's 51 g strap (LKL-DDR-003, P1) puts the whole set 0.35 kg over 1.0 kg. On 2026-10-02 Amish restated R12 as 1.0 kg for the logger, cable and sensor, with the bar counted as site hardware (LKL-DDR-003, A1), so **R12 is met on paper** at 0.96 kg, a margin of 0.04 kg on estimated masses; the logger set is weighed at TRL 4.
- **Reach.** The cable plug sits 0.48 m below the street, so the 2 m cable with 0.3 m of slack reaches a spindle cap 2.18 m down, covering chambers up to the 1.5 m of R10 [K2].
- **Time.** The task estimate is 11 min: 3 min for cones and cover, 2 min to lower the puck on a pole, 2 min to set the neck bar with the logger and antenna already fitted and plug in the cable, 2 min to check the network join and 2 min to close up [K3]. It is 1 min over the R10 target and has not been shown with a crew, so **R10 is not verifiable at TRL 3**.

## L. False alarms (R13)

Random night-to-night scatter in the minimum level does not cause false alarms: with a 2 dB scatter and a flag at +6 dB for three nights, the rate is about 1e-6 per 20 loggers a month, and 7e-3 even at 3 dB scatter [L1]. Real false alarms come from persistent changes: a pump schedule, a pressure reducing valve that starts to hunt, a customer's night irrigation. Their rate is a property of the network, so **R13 is not verifiable at TRL 3**.

## M. Cost (R15)

Thirteen BOM lines, every one priced [M1]. Value-engineering target: USD 130 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 141 (USD 11 over the target). The constructable design added USD 28 to the USD 113 of v0.2: the neck bar (USD 12 more than the strap), the turned plugs, O-rings and screws (USD 4), the chassis (USD 4), the eye bolt and SMA bulkhead (USD 7) and the thicker puck (USD 1). **R15 is USD 11 over the value-engineering target.**

## N. Requirement status

*Table 6. Requirement status from this note [N]. Not met first, then at risk, then open.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R12 | Size and mass | 68 x 283 mm; logger, cable and sensor 0.96 kg (1.35 kg with the neck bar) | 70 x 300 mm; 1.0 kg for the logger, cable and sensor (restated 2026-10-02) | Met on paper (0.04 kg margin) |
| R1 | Hear a leak on metallic mains | 185 m on ductile iron at central efficiency (105 to 325 m over source efficiency, 93 to 370 m over pipe loss) | 100 m | **At risk** |
| R3 | Sensor bandwidth | Mounted resonance 676 to 1,352 Hz; flat to 366 to 732 Hz | 5 Hz to 2 kHz, ±3 dB after correction | **At risk** |
| R4 | Sensor self-noise | 1.03 µg/√Hz worst from 100 Hz to 1 kHz | 1 µg/√Hz | **At risk** |
| R7 | Radio link | Range 0.53 km under an iron cover at 20 dB (EU868 SF12), 0.46 km (US915 SF9); cover loss unmeasured | 90 % delivery to a gateway within 0.5 km under iron covers | **At risk** |
| R2 | Hear a leak on plastic mains | Hydrophone variant not sized; the contact sensor (out of scope for plastic) hears 4 m on PVC | 30 m, hydrophone variant | Open, variant not sized at TRL 3 |
| R10 | Install from the surface | 11 min task estimate; reach to 2.18 m | 10 min, 1.5 m, no entry | Not verifiable at TRL 3 |
| R13 | Leak flag quality | Random scatter negligible; site events unknown | 1 per 20 loggers per month | Not verifiable at TRL 3 |
| R5 | Night listening | 20 s worst with weekly time correction | 12 windows, under 1 min a month | Met on paper |
| R6 | Battery life | 10.3 years or more on energy | 5 years | Met on paper |
| R9 | Attachment | 125 N at a 0.5 mm coating (187 N at 0.3 mm, 309 N bare) | 100 N | Met on paper |
| R15 | Cost | $141.00 | $130 value-engineering target | USD 11 over the value-engineering target |
| R8 | Data and privacy | Processed as sampled, deleted on device | Only levels and spectra leave | Met by design |
| R11 | Survive the chamber | IP68 parts; floats on its lanyard when flooded | IP68, -20 to +50 °C | Met by design |
| R14 | Open and interoperable | 24-byte LoRaWAN 1.0.3 uplink, documented | Standard LoRaWAN | Met by design |

## O. TRL 2 figures checked

*Table 7. TRL 2 figures against this note.*

| TRL 2 figure | This note | Outcome |
| --- | --- | --- |
| 3.84 MB sampled a night | 3.84 MB [A1] | Stands |
| About 50 bytes sent a night | 24 bytes [A4] | Changed; the precis is updated |
| About 1.15 mAh a day | 1.15 to 1.22 mAh [C1] | Stands |
| About 12.8 years on energy, about 10 years life | 10.3 to 12.8 years [C1] | Stands |
| Radio at 20 dBm, 120 mA | +14 dBm in EU868 [D4] | Changed |
| Magnet hold about 95 N, marginal | 90 N at 0.3 mm, 60 N at 0.5 mm [I1] | Stood; 42 mm magnet fitted (LKL-DDR-002) |
| 63 x 240 mm, about 0.7 kg | 63 x 240 mm (283 mm overall), 1.35 kg with the neck bar [K1] | Mass changed (v0.2: 0.98 kg); the precis is updated |
| About $108 in parts | $141.00 [M1] | Changed: $113.00 in v0.2 (mass $1, magnet $4); constructable design $28 more |
