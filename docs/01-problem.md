---
doc_id: LKL-PRB-001
title: LeakListen problem statement
project: LeakListen
doc_type: Problem statement
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
  change: Problem, users, context, constraints, prior work and open questions for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: "TRL 3, reflect the TRL 2 review items adopted for TRL 3 (LKL-DDR-001) and the findings of LKL-CAL-001 in the constraints, prior work and open questions"
---

# LeakListen problem statement

A large share of treated city water is lost to leaks before it reaches customers, and most leaks that do not surface are found late, by slow manual listening surveys or not at all. Small and mid-sized utilities need a cheap way to listen to their network every night and point crews at the few places worth a closer look.

## The problem

Leaks cost water, energy and money in every network, and the losses are largest where utilities can least afford them.

- Globally, non-revenue water (water produced but not billed, because of physical leaks or commercial losses) is estimated at 126 billion m³ a year, worth nearly $40 billion ([World Bank](https://blogs.worldbank.org/en/ppps/what-do-private-companies-look-performance-based-non-revenue-water-project)).
- In developing countries, about 45 million m³ a day are lost through leakage in distribution networks, "enough to serve nearly 200 million people" ([Kingdom, Liemberger and Marin, World Bank, 2006](https://documents1.worldbank.org/curated/en/385761468330326484/pdf/394050Reducing1e0water0WSS81PUBLIC1.pdf)).
- Even in high-income networks the numbers are large: the United States still has about 240,000 water main breaks a year ([ASCE 2025 Report Card](https://infrastructurereportcard.org/cat-item/drinking-water-infrastructure/)), and water companies in England and Wales leaked an average of 2,967 million litres a day from April 2022 to March 2025 ([Discover Water](https://www.discoverwater.co.uk/leaking-pipes)).

Many leaks never reach the surface and can run for months because nobody hears them. Commercial acoustic noise loggers solve this, but a fleet of them plus the software subscription is beyond many small utilities, and the loggers are closed, so a utility cannot inspect, repair or adapt them.

## Users and context

| User | Need |
| --- | --- |
| Small and mid-sized water utility (network and leakage team) | A low-cost way to screen a district every night and send the leak crew to the right street |
| Leak detection technician | Loggers that are quick to place from the surface and give a clear "listen here" list for ground microphone or correlator follow-up |
| Utility manager or regulator | A simple trend of how many loggers flag a possible leak, to target repairs and show progress on losses |
| Community water scheme or campus facilities team | A few loggers on a private network (campus, industrial park, airport) without a specialist contract |
| Researchers and students | An open, documented logger and dataset for leak noise research |

**Operating context.** The logger sits in a valve chamber or surface valve box on a pressurized distribution main, typically DN80 to DN300 (3 to 12 in), cast iron, ductile iron, steel, asbestos cement or plastic. Chambers are dark, damp and may flood; the cover is often cast iron, which blocks radio. The sensor attaches by magnet to a valve spindle cap, hydrant or fitting, which carries pipe vibration well. Leaks are loudest relative to background at night, when demand and traffic are low, so the logger listens between about 02:00 and 04:00.

## Constraints

- Garage-buildable prototype, about $130 USD in parts per logger (`project.yaml`).
- No pipe work: nothing is cut, tapped or drilled on the utility's assets, and the logger must not change water quality.
- Installed and recovered from the surface with a pole or valve key; no confined space entry (see Safety).
- Runs on a primary battery for years; there is no power in a chamber and no sun for solar.
- Sends one small summary a night over LoRaWAN to any network server, including the lab's TwinKit gateway; raw vibration samples never leave the device (a fixed requirement, LKL-DDR-001 D6).
- Works only on pressurized pipes. Leaks on unpressurized or intermittent-supply pipes make little or no noise.
- Utility permission is needed before any logger is placed on a public network.

## Out of scope

- Pinpointing a leak to within a metre. LeakListen flags a likely leak near a logger; crews then pinpoint with a ground microphone or correlator. Correlation between loggers is an open question for a later phase.
- Transmission mains above DN600, sewer and gas networks.
- Customer-side leaks inside buildings.

## Prior work

- **Acoustic leak detection** is the standard method for hidden leaks. Research at the National Research Council of Canada characterized leak signals in plastic pipes and found that most of the energy measured by hydrophones was below 50 Hz and that plastic pipes attenuate leak noise strongly ([Hunaidi and Chu, *Applied Acoustics*, 1999](https://www.sciencedirect.com/science/article/pii/S0003682X99000134)). A low-cost sensor must therefore reach down to a few hertz and will hear less far on plastic pipes.
- **Commercial noise and correlating loggers** are proven. For example, Gutermann's ZONESCAN 820 loggers correlate automatically between all relevant logger pairs each day and report leak positions to better than 1 m ([Gutermann](https://en.gutermann-water.com/)). These are closed products; LeakListen aims at the simpler, cheaper noise-level screening task, with open hardware and data.
- **Performance-based non-revenue water programs** show that finding and fixing leaks pays back, which is why the World Bank promotes them ([World Bank](https://blogs.worldbank.org/en/ppps/what-do-private-companies-look-performance-based-non-revenue-water-project); [Kingdom et al., 2006](https://documents1.worldbank.org/curated/en/385761468330326484/pdf/394050Reducing1e0water0WSS81PUBLIC1.pdf)).
- **Lab siblings.** LeakListen reuses the STM32WL LoRaWAN core and payload conventions of FieldNode (not its solar power, which cannot work in a chamber), adopted for TRL 3 in LKL-DDR-001 D4, and reports to the lab's TwinKit gateway, which already lists leak detection among its water supply uses.
- **Leak noise in plastic pipes.** Gao et al. modeled leak noise in buried plastic pipes as a fluid-dominated wave with a flat source spectrum and showed that the signals are low frequency and narrow band ([Gao, Brennan, Joseph, Muggleton and Hunaidi, *Journal of Sound and Vibration*, 2004](https://www.sciencedirect.com/science/article/pii/S0022460X03011647)). LKL-CAL-001 uses the same model form to estimate detection distance.

## Open questions

- [ ] Which pipe materials and diameters dominate the first partner utility's network? LKL-CAL-001 estimates about 185 m on iron but only a few metres on plastic for a contact sensor on a valve, so the answer sets whether the hydrophone variant is needed.
- [ ] How much does a cast-iron cover attenuate LoRa in practice? LKL-CAL-001 assumes 20 dB, which limits the link to about 0.5 km; the response (through-cover antenna, composite cover or a closer gateway) awaits Amish.
- [ ] What night-time background noise (pumps, pressure reducing valves, traffic, customer use) will cause false alarms?
- [ ] Will the partner utility allow magnets on valve spindle caps and hydrants, and who may place loggers?
- [ ] Is a nightly noise-level flag enough for the utility, or is correlation between loggers needed to be useful?

## Safety

> **Safety:** Valve chambers can be confined spaces with low oxygen or toxic gas; LeakListen is designed to be placed from the surface, and nobody should enter a chamber without the utility's confined space permit, gas testing and a trained standby person. Covers are heavy: use a proper lifting key and keep hands and feet clear. Work in the street needs traffic management under the local authority's rules. The logger uses a lithium thionyl chloride primary cell, which can vent or burn if shorted, crushed, heated or charged; never charge it. The pot magnet is strong: keep it away from pacemakers and pinch points.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
