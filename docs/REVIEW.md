# Review note: LeakListen

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to fix the weaker sources. README change only; no controlled document changed. All other README sources (World Bank, Kingdom et al. 2006, ASCE 2025, Discover Water, Tokyo Bureau of Waterworks) were re-checked and support their claims.

| Where | Old source | New source |
| --- | --- | --- |
| Country row: Sub-Saharan Africa | None | Replaced by South Africa, citing [Loubser, Chimbanga and Jacobs, 2021, *Water SA*](https://scielo.org.za/scielo.php?pid=S1816-79502021000100001&script=sci_arttext) (22 million people, 39 % of the population, on intermittent supply in 2017) |

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (LKL-PRB-001 v0.2): problem with cited loss figures, users, operating context, constraints, out of scope, prior work (Hunaidi and Chu 1999, Gutermann ZONESCAN, World Bank NRW work), open questions and safety; co-design checklist kept.
- `docs/03-requirements.md` (LKL-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, verification method and status at TRL 2; safety requirements S1 to S4; assumptions.
- `docs/02-concept.md` (LKL-PRC-001 v0.2): how it works, 10 numbered components, design choices, data and energy budgets, battery life, magnet hold, cost, safety and open questions.
- `cad/src/concept_media.py`: massing model of the logger on a gate valve in a DN150 main's valve chamber, with the street, soil and chamber shown in section and a 1.75 m person standing on the street. Existing assets (main, valve, spindle cap) are grey and unnumbered.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` (BOM callouts 1 to 10), `cutaway.png` (logger and sensor puck interiors), `flow.png` (nightly data flow, estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 11 lines with indicative USD prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; concept rationale, burning platform, where it could be used, what sparked the idea, concept, key components and safety expanded.
- `docs/pdf/`: branded PDFs of the three controlled documents.

Media notes: the kit's cutaway cutter is centered on Z = 0, so `concept_media.py` lifts the model 400 mm for the kit media; the hero is rendered separately in true street coordinates with a plain-language note. The main and valve appear only in the hero so the exploded view and cutaway frame the logger at a readable size.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Data sampled per night | 3.84 MB (240 s at 8 kS/s, 16 bit), deleted on device | R8 met by design |
| Data sent per night | about 50 bytes, one LoRaWAN uplink plus retries | R14 |
| Energy per day | about 1.15 mAh, self-discharge included | |
| Battery life, C-size Li-SOCl2 7.7 Ah at 70 % usable | about 12.8 years on energy, taken as about 10 years | R6 met on paper (5 years) |
| Magnet hold on a painted spindle cap | about 95 N (a third of the 290 N rating) | R9 marginal (100 N) |
| Logger size and mass | 63 x 240 mm; about 0.7 kg | R12 met |
| Parts cost | about $108 | R15 met ($130) |

Requirements not met or at risk:

- **R2 (plastic pipes) at risk:** plastic pipes attenuate leak noise strongly, so 30 m detection may not be reachable.
- **R7 (radio from under a cast-iron cover) at risk:** cover loss is unknown and may block the link.
- **R9 (attachment) not met** for brass, bronze or plastic fittings, and marginal on painted iron caps.
- **R1, R4 and R13 unverified:** detection distance on iron pipes, sensor self-noise and false alarm rate need calculation at TRL 3 and field data later.

### Proposed, awaiting Amish

1. **Screening versus correlation (pitch-level).** Option A: nightly noise-level screening only (this concept; fits LoRaWAN and a primary cell). Option B: add time-synchronized raw audio for correlation between neighboring loggers (pinpoints leaks, but needs GNSS or radio time sync, much more data and a larger battery). Recommendation: A for TRL 3, with B recorded as a later variant. **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-001, LKL-DDR-002).
2. **Radio from under covers.** Option A: flat antenna under the cover (this concept). Option B: through-cover antenna in a drilled or composite cover (needs utility consent). Option C: a nearby gateway per district. Recommendation: A, with a link budget at TRL 3 deciding whether B is needed. **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-001, LKL-DDR-002).
3. **Sensor type.** Piezo disc with a charge amplifier (cheap, this concept) versus a MEMS accelerometer (simpler, likely noisier at low levels) versus a hydrophone on hydrants (hears further on plastic, needs a tapping). Recommendation: piezo disc, with the hydrophone kept as an option for plastic networks. **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-001, LKL-DDR-002).
4. **Reuse of the FieldNode radio core** (STM32WL module and payload conventions, without FieldNode's solar power). Recommendation: yes, to share fixes across the lab. **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-001, LKL-DDR-002).
5. **Primary cell size.** C size about 7.7 Ah (this concept, about 10 years) versus D size about 19 Ah (longer margin, larger tube). Recommendation: C size. **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-001, LKL-DDR-002).
6. **Privacy rule.** Raw samples never leave the device (R8). Recommendation: keep as a fixed requirement. **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-001, LKL-DDR-002).
7. **First partner utility and region** for co-design and a pilot district. No recommendation; still Proposed, awaiting Amish.
8. **Whether a vibration calibration check belongs here or in CalRig** (CalRig today covers temperature, humidity and particles only). No recommendation; still Proposed, awaiting Amish.

No change to `project.yaml`: the pitch and problem still match the numbers found, and the budget holds.

### Safety concerns

- Valve chambers are confined spaces; the design avoids entry, but a failed placement may tempt someone to climb in. Instructions must say never enter without a permit, gas test and standby person.
- Heavy covers and street work: manual handling and traffic.
- Lithium thionyl chloride primary cell: fire or explosion if shorted, crushed, heated or charged; dangerous goods rules apply to shipping.
- Strong pot magnet: pinching and implanted medical devices.
- Work on a public water network without utility permission.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to estimate leak noise attenuation and detection distance for iron and plastic pipes, the sensor noise budget, the radio link budget through covers, and the magnet hold, and to produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (LKL-DDR-001 v0.1, status proposed): six items adopted as recommended for TRL 3, open for Amish's review (D1 to D6), and two left open (O1, O2).
- `docs/04-calcs/01-sizing.md` (LKL-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: data and processing, airtime, energy and battery life, link budget through the cover, leak noise attenuation, sensor noise and resonances, detection distance, clock, magnet hold, chamber survival, size and mass, installation, false alarms and cost, with a status for every requirement. The script imports the model, reads the BOM and `project.yaml`, prints every number the note quotes and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model of the installed set (sensor puck, magnet, piezo and mass, preamplifier, cable with M12 plug, logger tube with plugs, board and capacitor, cell, desiccant, hanger and lanyard, flat antenna), with the spindle cap and cover frame as grey context. Exports `cad/step/` and `cad/stl/` for `leaklisten-assembly`, `logger` and `sensor-puck`.
- `cad/src/sheets.py` and `cad/drawings/LKL-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:5, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". LKL-DWG-001 was free because the concept blueprint is LKL-DWG-010.
- `bom/bom.csv` (11 lines, all priced with a supplier or supplier type, $109.00 against the $130 budget) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now takes the LeakListen parts from the model; all of `media/` was re-rendered and every image checked; temporary `_views` folders deleted.
- LKL-PRB-001, LKL-PRC-001 and LKL-REQ-001 revised to v0.3; `README.md` (TRL badge and line, links, concept figures) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design changes made by the calculations, within the adopted decisions: the seismic mass grows from about 11 g to about 53 g in compression and the puck from 34 to 42 mm tall (R4); the nightly summary shrinks from about 50 to 24 bytes so it fits US915 (R14); transmit power is +14 dBm in EU868, since the TRL 2 figure of +20 dBm is not permitted there; the clock takes a weekly LoRaWAN time correction (R5).

### Requirement status (LKL-CAL-001, Table 6)

2 not met, 4 at risk, 2 not verifiable at TRL 3, 4 met on paper, 3 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R2 Plastic mains | **Not met** | About 4 m on PVC and 2 m on PE for the reference leak, against 30 m |
| R7 Radio link | **Not met** | -9.7 dB at 1 km under an iron cover at an assumed 20 dB loss (EU868 SF12); range about 0.53 km |
| R1 Metallic mains | At risk | About 185 m on ductile iron; 93 to 370 m over plausible pipe losses |
| R3 Bandwidth | At risk | Magnet mount resonance about 780 to 1,550 Hz, flat only to 420 to 840 Hz |
| R4 Self-noise | At risk | 1.03 µg/√Hz against 1 µg/√Hz |
| R9 Attachment | At risk | 149 N bare, 90 N at a 0.3 mm coating, 60 N at 0.5 mm; non-ferrous fittings still need an adapter |
| R10 Install, R13 False alarms | Not verifiable at TRL 3 | 10 min task estimate; random scatter negligible, site events unknown |
| R5, R6, R12, R15 | Met on paper | 20 s clock error with weekly sync; 10.3 years or more; 63 x 267 mm, 0.93 kg; $109.00 |
| R8, R11, R14 | Met by design | |

Key numbers: 1.15 to 1.22 mAh a day; 1.97 s per uplink at SF12; 157 pC/g sensor; leak noise loss 0.011 dB/m (iron) and 0.42 dB/m (PVC) at 100 Hz.

### Decisions recorded (LKL-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (since **Decided by Amish, 2026-09-25: go with recommendation**, LKL-DDR-002): D1 nightly noise-level screening, correlation as a later variant; D2 flat antenna under the cover, with the link budget deciding whether more is needed (it is, see item 3 below); D3 piezo disc sensor, hydrophone kept as an option for plastic networks; D4 reuse of the FieldNode STM32WL core and payload conventions without its solar power; D5 C-size cell; D6 raw samples never leave the device, R8 fixed. No new budget, pitch or problem wording was recommended, so `budget_usd` stays at $130 and `project.yaml` and `README.md` keep the existing pitch and problem lines.

### Still awaiting Amish

1. **O1, first partner utility and region** for co-design and a pilot district. No preference stated.
2. **O2, vibration calibration check here or in CalRig.** No recommendation was made. CalRig's TRL 3 scope is still temperature, humidity and particles.
3. **New, radio under iron covers (R7).** Options: (a) a through-cover antenna or composite cover, which needs utility consent; (b) plan a gateway within about 0.5 km of each district (TwinKit or partner); (c) relax R7 to 0.5 km under iron covers. Recommendation: measure cover loss first; then (b) as the default because it touches no utility asset, with (a) where a utility agrees. **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-002 D7); the measurement is TRL 4 and on hold.
4. **New, plastic mains (R2).** Options: (a) restate the contact sensor's scope as metallic mains and make the hydrophone variant (D3) the answer for plastic networks; (b) keep R2 for the contact sensor and accept it is not met; (c) relax R2. Recommendation: (a). **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-002 D8); the pitch still holds, since hydrophones also mount on existing fittings.
5. **New, 42 mm pot magnet (R9).** About +$4 ($113.00, under budget); holds 125 N at a 0.5 mm coating. Recommendation: yes, with a keeper plate as for the 32 mm magnet. **Decided by Amish, 2026-09-25: go with recommendation** (LKL-DDR-002 D9).

Suggestions only, not in the repo: request the full 64-band spectrum from a flagged logger by downlink; a pointed hardened contact stud under the magnet to stiffen the mount (R3).

### Cross-repo consistency

- FieldNode (FND REVIEW, TRL 3): STM32WL-class module, +14 dBm SX1262-class radio at 45 mA, 20-byte payload, TwinKit first. LeakListen now uses the same EU868 power, noise figure, SNR limits and antenna and feeder figures; its path model is urban Hata rather than FieldNode's suburban one, because loggers sit at street level in towns. The 24-byte summary is LeakListen's own payload on FieldNode's conventions. No conflict; FieldNode not edited.
- TwinKit (TWK REVIEW, TRL 3): 8-channel LoRaWAN concentrator; gateway sensitivity assumed equal to the node's, as here. Recommendation 3(b) would add gateways at about 0.5 km spacing in districts with iron covers, which is denser than TwinKit's sizing assumes. Noted here; TwinKit not edited.
- CalRig: no vibration scope (O2 stays open). No other repo was edited.

### Safety concerns

- Confined spaces: the design still needs no chamber entry. A failed placement may tempt someone to climb in; instructions must say never enter without a permit, gas test and standby person.
- Heavy covers and street work: manual handling and traffic management, as at TRL 2.
- Lithium thionyl chloride cell: fuse or PTC, reverse protection and no charging circuit; dangerous goods rules for shipping. The hybrid layer capacitor must be fused with the cell.
- Magnets: the proposed 42 mm magnet roughly doubles the pull, and the pinch hazard with it; keeper plate fitted in transport, and the pacemaker warning on the label.
- A flooded chamber lifts the logger against its lanyard (2.8 N); the lanyard must not rely on the antenna lead.
- Utility permission before placing anything on a public network.

### Gaps and notes

- Citations: the TRL 2 note listed no unchecked citations. The new citation in LKL-CAL-001 and LKL-PRB-001 (Gao et al., 2004) was verified with WebFetch on its publisher page. WebSearch was not used (quota exhausted).
- Assumptions only tests can settle: cover loss (10 to 30 dB), leak acoustic efficiency (1e-6 to 1e-4), pipe loss factors, valve coupling (-10 dB), night background, magnet mount stiffness and the gap law for the magnet. No figure was invented to replace them.
- The kit's cutaway cuts at the mean Y of the parts; as at TRL 2, `concept_media.py` lifts the logger parts 400 mm for the kit media and renders the hero separately in street coordinates. The cutaway shows the cell, capacitor and puck interior; the main board sits in the removed half and shows in the exploded view.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. `firmware/` and `electronics/` are empty. No test, build or firmware material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on D1 to D6, O1 and O2, and items 3 to 5 above. For the record only, TRL 4 would need: a bench build of the sensor puck and logger; a lab test report (TST, `environment: lab`) covering sensor sensitivity and self-noise against a reference accelerometer on a shaker, magnet pull on coated iron caps, mounted resonance, LoRa loss through iron and composite covers, sleep and listening current, and a submersion check; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (LKL-DDR-002 v0.1). Items without a recommendation stay open. The repo stays at TRL 3.

### Decisions applied and what changed

- **D1 to D6** (LKL-DDR-001): screening, flat antenna, piezo sensor, FieldNode core, C cell, privacy rule. Already built into the TRL 3 design; LKL-DDR-001 raised to v0.2 with the new status wording.
- **D7, radio under iron covers (R7).** Measure cover loss first (TRL 4, on hold), then plan a gateway within about 0.5 km of each district with iron covers, with a through-cover antenna or composite cover where a utility agrees. R7 restated from "gateway within 1 km" to "gateway within 0.5 km under iron covers, 1 km where a composite cover or through-cover antenna is agreed". New LKL-CAL-001 line [D5]: margin at 0.5 km under a 20 dB cover +0.9 dB (EU868 SF12) and -1.2 dB (US915 SF9); -9.1 dB under a tight 30 dB cover. R7: not met (-9.7 dB at 1 km) to at risk.
- **D8, plastic mains (R2).** The contact sensor's scope is metallic mains (R1); R2 applies to the hydrophone variant, which is not yet sized. R2: not met (4 m on PVC) to open.
- **D9, 42 mm magnet (R9).** `cad/src/model.py` magnet 32 to 42 mm (rated 290 to 600 N, new parameter `magnet_rated_n`); STEP and STL re-exported; BOM line 2 $5 to $9, total $109.00 to $113.00 (budget $130 unchanged, margin $21.00 to $17.00); hold at a 0.5 mm coating 60 to 125 N, at 0.3 mm 90 to 187 N. R9: at risk to met on paper. Side effects: puck and magnet 210 to 262 g, mounted resonance 776 to 1,553 Hz becomes 695 to 1,389 Hz (flat to 376 to 752 Hz, R3 still at risk and slightly worse); total mass 0.93 to 0.98 kg (R12 met with 20 g to spare).
- Documents: LKL-PRB-001 v0.4, LKL-PRC-001 v0.4, LKL-REQ-001 v0.4, LKL-CAL-001 v0.2 (script re-run, `results.csv` rewritten), LKL-DDR-001 v0.2, new LKL-DDR-002 v0.1; LKL-DWG-001 Rev P1 to P2 (magnet); `media/` re-rendered (magnet label, key figures) and checked; `bom/bom-notes.md` updated; `project.yaml` evidence list adds LKL-DDR-002. No budget, pitch or problem change was recommended, so `budget_usd`, `pitch` and `problem` are unchanged.
- README: "What sparked the idea" rewritten around Tokyo's listening-rod leak surveys on gate valves (leakage 10.2 % in fiscal 1992 to 3.5 % in fiscal 2024, Tokyo Bureau of Waterworks); cost, mass and requirement text updated. All PDFs and drawings regenerated so the footer reads designmolecule.com.

### Requirement status (LKL-CAL-001 v0.2)

None not met (was 2), 4 at risk, 1 open, 2 not verifiable at TRL 3, 5 met on paper, 3 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R1 Metallic mains | At risk | About 185 m on ductile iron; 93 to 370 m over plausible pipe losses |
| R3 Bandwidth | At risk | Mount resonance 695 to 1,389 Hz, flat only to 376 to 752 Hz |
| R4 Self-noise | At risk | 1.03 µg/√Hz against 1 µg/√Hz |
| R7 Radio link | At risk | +0.9 dB at 0.5 km (EU868 SF12), -1.2 dB (US915 SF9); cover loss unmeasured |
| R2 Plastic mains | Open | Hydrophone variant not sized |
| R10, R13 | Not verifiable at TRL 3 | Field work needed |
| R5, R6, R9, R12, R15 | Met on paper | 20 s clock; 10.3 years; 125 N at 0.5 mm; 0.98 kg; $113.00 |
| R8, R11, R14 | Met by design | |

### Still awaiting Amish

1. **O1, first partner utility and region** for co-design and a pilot district. No recommendation.
2. **O2, vibration calibration check here or in CalRig.** No recommendation.

The two suggestions in the TRL 3 section (full spectrum by downlink; a hardened contact stud) were suggestions, not recommendations, and remain outside the repo.

### Cross-repo actions

- **TwinKit:** D7 plans a gateway within about 0.5 km of each district with cast-iron covers, denser than TwinKit's current sizing assumes. Raise with TwinKit; TwinKit not edited.
- **FieldNode:** no action; D4 (shared STM32WL core and payload conventions) is consistent with FieldNode's TRL 3 figures.
- **CalRig:** depends on O2, which is still open; no action yet.

### Safety

Unchanged, plus: the 42 mm magnet pulls about twice as hard as the 32 mm one, so the pinch hazard rises; it ships with its keeper plate fitted and the pacemaker warning stays on the label.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Decided but on hold: measuring LoRa loss through cast-iron and composite covers (D7) and any field link check. No build, test, purchasing, PCB or firmware work was done.
