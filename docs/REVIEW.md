# Review note: LeakListen

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

1. **Screening versus correlation (pitch-level).** Option A: nightly noise-level screening only (this concept; fits LoRaWAN and a primary cell). Option B: add time-synchronized raw audio for correlation between neighboring loggers (pinpoints leaks, but needs GNSS or radio time sync, much more data and a larger battery). Recommendation: A for TRL 3, with B recorded as a later variant.
2. **Radio from under covers.** Option A: flat antenna under the cover (this concept). Option B: through-cover antenna in a drilled or composite cover (needs utility consent). Option C: a nearby gateway per district. Recommendation: A, with a link budget at TRL 3 deciding whether B is needed.
3. **Sensor type.** Piezo disc with a charge amplifier (cheap, this concept) versus a MEMS accelerometer (simpler, likely noisier at low levels) versus a hydrophone on hydrants (hears further on plastic, needs a tapping). Recommendation: piezo disc, with the hydrophone kept as an option for plastic networks.
4. **Reuse of the FieldNode radio core** (STM32WL module and payload conventions, without FieldNode's solar power). Recommendation: yes, to share fixes across the lab.
5. **Primary cell size.** C size about 7.7 Ah (this concept, about 10 years) versus D size about 19 Ah (longer margin, larger tube). Recommendation: C size.
6. **Privacy rule.** Raw samples never leave the device (R8). Recommendation: keep as a fixed requirement.
7. **First partner utility and region** for co-design and a pilot district.
8. **Whether a vibration calibration check belongs here or in CalRig** (CalRig today covers temperature, humidity and particles only).

No change to `project.yaml`: the pitch and problem still match the numbers found, and the budget holds.

### Safety concerns

- Valve chambers are confined spaces; the design avoids entry, but a failed placement may tempt someone to climb in. Instructions must say never enter without a permit, gas test and standby person.
- Heavy covers and street work: manual handling and traffic.
- Lithium thionyl chloride primary cell: fire or explosion if shorted, crushed, heated or charged; dangerous goods rules apply to shipping.
- Strong pot magnet: pinching and implanted medical devices.
- Work on a public water network without utility permission.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to estimate leak noise attenuation and detection distance for iron and plastic pipes, the sensor noise budget, the radio link budget through covers, and the magnet hold, and to produce the parametric model and drawing sheet.
