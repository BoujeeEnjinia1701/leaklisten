# BOM notes

- Costs are indicative USD prices for one prototype logger, from typical distributor and hobby market prices in 2026. Every line is priced; supplier types are given where no supplier is chosen yet.
- Line numbers match the callouts in `media/exploded.png`. Line 11 has no callout.
- Total: $113.00 per logger against the $130 budget in `project.yaml` (checked by `docs/04-calcs/sizing.py`, LKL-CAL-001 [M1]).
- Changes at TRL 3: the seismic mass grows from about 11 g to about 53 g (line 3, +$1) and the puck from 34 mm to 42 mm tall, so the sensor meets its noise target on paper.
- Decided by Amish, 2026-09-25 (LKL-DDR-002): the 32 mm pot magnet ($5) is replaced by a 42 mm pot magnet with a keeper plate ($9), so the total rises from $109.00 to $113.00. The district gateway for iron covers is a TwinKit or partner gateway and is not in the logger's BOM; a through-cover antenna is fitted only where a utility agrees and is not in the total.
- Not included: a LoRaWAN gateway (TwinKit or a partner's network), the placement pole and cover lifting key (utility tools), and any network server costs.
