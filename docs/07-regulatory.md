---
doc_id: LKL-REG-001
title: LeakListen regulatory and standards register
project: LeakListen
doc_type: Regulatory register
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: First register, written in the kit 1.9.1 upgrade for option A (the current design) and, where it differs, options B and C; the first candidate region is the UK (LKL-DEC-001, 2026-10-02)
---

# LeakListen regulatory and standards register

LeakListen as a prototype is a battery-powered licence-exempt radio device that sits in a water utility's valve chamber, so the rules that matter are radio (G1, G2), lithium cell safety and transport (G3), safe working at the chamber (G5, G6) and, for option B only, products in contact with drinking water (G4). No certification is needed before TRL 4; a deployed product would need radio conformity (G2). The first candidate region is the UK (LKL-DEC-001, 2026-10-02), so UK rules lead. Not legal advice; anything marked "to assess" needs a qualified reviewer. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | UK Interface Requirement 2030, licence-exempt short range devices (Ofcom), and the Wireless Telegraphy exemption regulations | UK | Frequency, power and duty cycle of licence-exempt devices in the 868 MHz band | The LoRaWAN radio at +14 dBm ERP; PR-020 | Design lead | Applies (limits to confirm against the current text) |
| G2 | EU Radio Equipment Directive 2014/53/EU with ETSI EN 300 220 (short range devices, 25 to 1000 MHz) and the EMC standards for radio equipment; UK Radio Equipment Regulations 2017 | EU, UK | Radio conformity, CE or UKCA marking, spectrum use | A product with the STM32WL radio module; prototype use at TRL 3 needs no marking | Design lead | To assess (certification needed later) |
| G3 | UN3090 and UN3091 (lithium metal batteries, alone and packed with equipment) and UN Manual of Tests and Criteria section 38.3; IEC 60086-4 (safety of lithium primary batteries) | International | Transport classification and cell safety | The Li-SOCl2 C cell (BOM line 8) ships as a dangerous good; fuse and reverse protection (PR-017) | Design lead | Applies (to assess for shipping) |
| G4 | Regulation 31, Water Supply (Water Quality) Regulations (England and Wales), approval of products in contact with drinking water (DWI, WRAS) | UK | Materials and products touching drinking water | Option B only: stainless cap, EPDM gasket, potted hydrophone and cable are wetted. Option A touches no water (PR-019); option C is buried | Co-design partner | To assess (option B only) |
| G5 | Confined Spaces Regulations 1997 (SI 1997/1713) and HSE Approved Code of Practice L101 | UK | Work in confined spaces, permits, gas testing, rescue | The design avoids entry (PR-016); the crew's practice at the chamber remains the utility's | Co-design partner | Applies (design intent: no entry) |
| G6 | Safety at Street Works and Road Works, a code of practice (UK) | UK | Signing, lighting and guarding of work in the street | Lifting a cover and working at a chamber in a street | Co-design partner | To assess |
| G7 | IEC 60529, degrees of protection provided by enclosures (IP code) | International | IP68 definition | The logger housing (PR-011); the test is TRL 4 work | Design lead | Applies |
| G8 | UK GDPR and Data Protection Act 2018 (and EU GDPR) | UK, EU | Processing of personal data | A vibration sensor in the street is a poor microphone and raw samples never leave the device (PR-008), so no personal data is expected | Design lead | To assess |
| G9 | EU Batteries Regulation (EU) 2023/1542, WEEE Directive 2012/19/EU, RoHS Directive 2011/65/EU | EU | Battery labelling and end of life, electronics waste, hazardous substances | The cell and the board of a product sold in the EU; label (PR-018) | Design lead | To assess (certification needed later) |
| G10 | IATA Dangerous Goods Regulations, magnetised material (Packing Instruction 953) | International | Air shipment of strong magnets | The 42 mm pot magnet, shipped with its keeper plate | Design lead | To assess |
| G11 | ISO 11228-1, manual handling: lifting and carrying | International | Mass limits for lifting | Covers (30 kg or more) and, for option B, the 6 kg cap; the logger set is 0.96 kg | Co-design partner | To assess |
| G12 | Consent to place equipment on a utility's assets, a hydrant or a street verge | Country and utility | Permission | Every installation (option C also needs consent to dig and a services search) | Co-design partner | To assess |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- Ofcom, "IR 2030 UK Interface Requirements 2030", https://www.ofcom.org.uk/__data/assets/pdf_file/0028/84970/ir-2030.pdf, listed in search results 2026-11-01; its text was not consulted for this register (G1).
- Ofcom, "Short-range devices", https://www.ofcom.org.uk/spectrum/radio-equipment/short-range-devices, listed in search results 2026-11-01 (G1).
- Drinking Water Inspectorate, "What is Reg31?", https://www.dwi.gov.uk/?p=8284, listed in search results 2026-11-01; not consulted (G4).
- legislation.gov.uk, "The Confined Spaces Regulations 1997", https://www.legislation.gov.uk/uksi/1997/1713/section/1, and HSE, "Safe work in confined spaces" (L101), https://www.hse.gov.uk/pubns/books/l101.htm, listed in search results 2026-11-01; not consulted (G5).
- Standards G2, G3, G6 to G11 are cited by number and title only, from the author's knowledge; their texts were not consulted for this register and each applicability is to be confirmed by the role named. No standard number was invented; any number the author could not confirm is left out.
