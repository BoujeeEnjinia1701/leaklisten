---
doc_id: LKL-MKT-001
title: LeakListen market and viability
project: LeakListen
doc_type: Market and viability
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: First market and viability note (prices checked 2026-11-01); commercial benchmarks are few because noise logger prices are mostly quoted privately
---

# LeakListen market and viability

LeakListen is for small and mid-sized water utilities, private networks and researchers who cannot afford a closed fleet of noise loggers. Published prices are scarce; the two found are far apart and neither is a like-for-like comparison, so viability is argued from the parts cost (USD 142 against a USD 130 target) rather than a market price. Prices were checked on 2026-11-01. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Small and mid-sized water utilities | Leakage teams in the UK and Europe, first candidate region the UK (LKL-DEC-001) | SubSurface Enigma 3 Hybrid Logger System: USD 22,500 current price (USD 27,000 list) for three magnet-base loggers, three cable loggers, three hydrophone kits, three stainless 2.5 inch hydrant caps, a USB cable and cases; about USD 3,750 per logger if the rest is free | 142 in parts for option A (bom/bom.csv), no labour or board design | A fleet of open loggers at a fraction of a closed kit; data and radio open (UR-010, UR-015) |
| Community water schemes and private networks | Campuses, industrial parks, airports | An Indian listing for an "RD521 Noise Logging System" at Rs 1,900 per piece, excluding taxes, rated for 10 years of battery and a 5-year warranty (about USD 22 at Rs 85 per USD, an estimate not checked); what a piece includes is not stated | 142 | The low end is a single unit price of unknown scope and cannot be compared; LeakListen adds LoRaWAN reporting and open data |
| Researchers and students | Leak noise research, teaching | Closed commercial loggers; no open dataset found in this search | 142 | An open, documented logger and dataset (UR-015) |

The one hard benchmark (Enigma 3) shows what a utility pays today for magnet-base loggers plus hydrophones on stainless hydrant caps, which is the pairing of options A and B in this repo. The price is for a kit with host software; whether software and a receiver are included was not stated on the page. The benchmark does not show how many such kits utilities buy, and no market size is claimed here.

## Open route

A lab or a university builds the logger from the drawings, bill of materials and build plan; a utility or a research partner places it; the lab's TwinKit gateway or any LoRaWAN network server receives the 24-byte summary. CERN-OHL-S keeps changes open. The main board design (TRL 4) and a utility partner (LKL-RSK-001 P1) are the two gates to a pilot.

## Sources

- SubSurface Leak Detection (listing on Tiger Supplies). "SubSurface Enigma 3 Hybrid Logger System." https://tigersupplies.com/products/subsurface-enigma-3-hybrid-logger-system (checked 2026-11-01): current price USD 22,500.00, list USD 27,000.00; contents as stated in the text.
- IndiaMART listing. "RD521 Noise Logging System." https://m.indiamart.com/proddetail/rd521-noise-logging-system-4246181233.html (checked 2026-11-01): Rs 1,900 per piece, excluding all taxes.
- Gutermann, https://en.gutermann-water.com/, cited in LKL-PRB-001 (a commercial correlating logger, no price found).
- The exchange rate of Rs 85 per USD is an estimate, not checked.
