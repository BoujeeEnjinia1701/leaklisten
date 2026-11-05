---
doc_id: LKL-URS-001
title: LeakListen user requirements
project: LeakListen
doc_type: User requirements
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: First user requirements, written in the kit 1.9.1 upgrade from the users and stakeholders in LKL-PRB-001 and the TRL 2 and TRL 3 requirements R1 to R15; used to score the concept options (LKL-OPT-001)
---

# LeakListen user requirements

What users need, written from their side. The sixteen needs come from the users and stakeholders in the problem statement (LKL-PRB-001, Table 1 and Constraints) and from what the earlier requirements R1 to R15 already assumed, and they are used to score the concept options (LKL-OPT-001). Each one has at least one product requirement in LKL-PRS-001 (links in LKL-RTM-001). They are a desk draft: no utility has reviewed them, and the first candidate partner, a UK water company with metallic mains and district metered areas, has not been approached (LKL-DEC-001, 2026-10-02). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Hears leaks before they surface | The logger tells the leakage team that a hidden leak is near it, at night, without anyone listening on site | High | Small and mid-sized utility; leak detection technician (PRB Table 1) |
| UR-002 | Performance | Works on plastic mains too | Plastic (PVC and PE) mains are covered as well as metal ones, at least through a variant | Medium | Small and mid-sized utility; PRB operating context; LKL-DDR-002 |
| UR-003 | Deployment and assembly | Placed from the surface | Nobody enters a chamber or a trench to place, service or recover a logger | High | Leak detection technician; PRB Constraints and Safety |
| UR-004 | Deployment and assembly | Quick to place | One crew places or recovers a logger in minutes, with a pole or valve key and no pipe work | Medium | Leak detection technician |
| UR-005 | Performance | Reports by itself | A short nightly summary reaches the utility's server over a low-power radio, with no visit and no cabling | High | Utility manager; PRB Constraints |
| UR-006 | Environment and durability | Survives the chamber | It works in a dark, damp chamber that may flood, from cold winters to warm summers | High | Leak detection technician; PRB operating context |
| UR-007 | Maintenance | Runs for years unattended | One battery lasts years, because there is no power or sun in a chamber | High | Utility manager; PRB Constraints |
| UR-008 | Cost | Affordable for a small utility | A fleet of loggers costs far less than commercial noise loggers and their subscriptions | High | Small and mid-sized utility; community scheme (PRB problem) |
| UR-009 | Regulatory | Raw sound stays on the device | Nothing that could be heard as speech leaves the logger | High | Utility manager; regulator; LKL-DDR-001 D6 |
| UR-010 | Usability | Open data and standard radio | Works with any LoRaWAN network server and gives researchers open, documented data | Medium | Researchers and students; community scheme |
| UR-011 | Safety | Safe to handle | The lithium cell, the strong magnet and the lifting of covers do not hurt the crew | High | Leak detection technician; PRB Safety |
| UR-012 | Safety | Does not touch the water | Nothing touches drinking water or is fixed to the pipe, so water quality and the asset are untouched | High | Utility manager; PRB Constraints |
| UR-013 | Usability | Few false alarms | A flag means a crew should go and look; the flag list is short and credible | Medium | Utility manager; leak detection technician |
| UR-014 | Packaging and transport | Small and light | One person carries the logger set and it fits through a valve box or chamber neck | Medium | Leak detection technician |
| UR-015 | Maintenance | Open and repairable | A utility or a workshop can inspect, repair and adapt the logger, unlike closed commercial loggers | Medium | Community scheme; researchers; PRB problem |
| UR-016 | Regulatory | Legal to place and to transmit | It uses licence-exempt radio within the regional power limit and is placed only with the utility's permission | Medium | Regulator; utility manager; PRB Constraints |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
