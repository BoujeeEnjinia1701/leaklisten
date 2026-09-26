# BOM notes

- Costs are indicative USD prices for one prototype logger, from typical distributor and hobby market prices in 2026. Every line is priced; supplier types are given where no supplier is chosen yet.
- Line numbers match the callouts in `media/exploded.png`. Line 11 has no callout.
- Total: $109.00 per logger against the $130 budget in `project.yaml` (checked by `docs/04-calcs/sizing.py`, LKL-CAL-001 [M1]).
- Changes at TRL 3: the seismic mass grows from about 11 g to about 53 g (line 3, +$1) and the puck from 34 mm to 42 mm tall, so the sensor meets its noise target on paper.
- Proposed, awaiting Amish (not in the total): a 42 mm pot magnet (about +$4) for coated spindle caps; a through-cover antenna or district gateway for iron covers (see `docs/REVIEW.md`).
- Not included: a LoRaWAN gateway (TwinKit or a partner's network), the placement pole and cover lifting key (utility tools), and any network server costs.
