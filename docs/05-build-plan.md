---
doc_id: LKL-BLD-001
title: LeakListen prototype build plan
project: LeakListen
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (LKL-DDR-003)
---

# LeakListen prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order: the sensor puck (1 to 5), the logger (6 to 12) and the neck bar that hangs it in the chamber (13 to 18).*

The prototype is one LeakListen set in three parts. The sensor puck is a small turned aluminium cup with a pot magnet under it; inside, a piezo disc and a brass weight turn pipe vibration into a signal, and a small amplifier board, potted in, sends it up a 2 m cable. The logger is a sealed 63 mm PVC tube with a turned plastic plug in each end; inside, a printed frame carries the radio and processing board, a lithium cell and a desiccant pack. The neck bar is a telescopic aluminium bar that wedges across the chamber's neck, just below the cover frame, on two rubber feet; the logger hangs from it on a short wire rope, and a flat antenna sits on a bracket on top of it, just under the cover. Nine components are made in a small workshop: the puck body and the brass weight (turned), the logger tube (cut and drilled), the two end plugs (turned from plastic bar), the frame inside the logger (3D printed), the two bar tubes and the antenna bracket (cut and drilled). Everything else is bought and fitted. The parts cost about USD 141, from the bill of materials.

> **Safety:** The logger holds a lithium thionyl chloride primary cell. It must never be charged, shorted, crushed or heated; keep it in its packaging until stop point S2 (section 6). The pot magnet pulls hard enough to trap fingers and can affect pacemakers; keep its keeper plate on until the puck is at the spindle cap. Valve chambers can be confined spaces: everything in this plan is done at a bench or from the surface, and nobody enters a chamber. Turning, drilling and cutting need eye protection.

## 2. What changed to make it buildable

The concept showed what LeakListen does; some of its parts could not be made or fixed as drawn. Each change below keeps what LeakListen does, and all of them are recorded in decision record LKL-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Hanger | A stainless strap "hooked over the cover frame", which had nothing to hook over except the seat under the cover | A telescopic aluminium bar wedged across the chamber neck below the frame by two rubber feet; the logger hangs from it on a wire rope lanyard (Figures 15 and 17, steps 11 to 14) | The cover stays seated and nothing is drilled; still placed from the surface |
| Antenna mounting | Overlapping the strap, with no fixing | A small aluminium bracket bolted across the bar, the antenna's own stud through it; the antenna sits 20 mm under the cover (Figure 19) | Nothing overlaps; one bolt and one nut |
| Logger end plugs | Drawn solid with the tube, no way to hold them | Flanged plastic plugs with two O-rings each, held by three screws through the tube outboard of the O-rings (Figures 8 and 10) | Seals for submersion; the screws never cross the seal |
| Top of the logger | One gland for both the lanyard and the antenna lead | An eye bolt for the lanyard and a sealed antenna bulkhead connector, each in its own hole (Figures 6 and 12) | A rope and a connector cannot share a gland |
| Inside the logger | Board, cell and desiccant floating | A printed frame hung from the top plug, with clips and a pocket (Figures 9 and 11) | Everything is fixed and lifts out with the top plug |
| Puck base | 3 mm thick, too thin for the magnet's stud | 8 mm thick, tapped for the stud (Figures 2 and 4) | The magnet is screwed on |
| Inside the puck | Amplifier board floating above the weight; "potted" without saying where | A stepped bore: the board sits on the step clear of the weight, and potting fills only the space above the board (Figure 4) | The weight must stand free to sense correctly |

The set now weighs about 1.35 kg with the bar (the logger, cable and puck about 0.96 kg), and is about 283 mm long from socket to eye bolt.

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. Workshop tolerance is 0.2 mm on turned diameters that seal or slide and 0.5 mm elsewhere; drawings do not carry tolerances before TRL 4.

### 3.1 Sensor puck body

![Figure 2. Making sketch of the sensor puck body](../cad/drawings/LKL-DWG-101.png)

*Figure 2. Sensor puck body making sketch (LKL-DWG-101).*

**What it is and what it is made from.** The stiff cup that sits on the magnet and carries the sensor. Aluminium 6061 round bar, 45 mm, turned to 40 mm diameter and 42 mm long.

**How to make it.**

1. Face and turn the bar to 40 mm diameter; part off 42 mm long.
2. Bore the lower bore 29 mm diameter, leaving a base 8 mm thick; then bore the upper 9 mm to 32 mm diameter. The step between them is 25 mm above the base.
3. Finish the inside face of the base flat and smooth: the piezo disc is bonded to it and the signal passes through it.
4. Turn the part round. Centre drill the bottom face, drill 5 mm, 8 mm deep, and tap M6 for 6 mm of full thread.
5. Break all outside edges 0.5 mm.

**How it fits the parts next to it.** The magnet's stud screws into the base. The piezo disc is bonded to the inside of the base, the brass weight to the disc, and the round amplifier board rests on the step. Potting fills the upper bore above the board (Figure 4).

**Check before moving on.** The base face is flat when checked with a straight edge; the magnet's stud runs into the thread by hand.

### 3.2 Seismic mass

![Figure 3. Making sketch of the seismic mass](../cad/drawings/LKL-DWG-102.png)

*Figure 3. Seismic mass making sketch (LKL-DWG-102).*

**What it is and what it is made from.** The brass weight that presses on the piezo disc; its inertia is what makes the disc sense vibration. Brass round bar, 20 mm, 20 mm long, about 53 g.

**How to make it.**

1. Saw a 21 mm slice off the bar.
2. Face both ends to 20 mm long, flat and parallel, in one setting each (or lap them on fine abrasive paper on glass).
3. Break the edges 0.3 mm, weigh the part and write the mass down.
4. Degrease with alcohol just before bonding.

**How it fits the parts next to it.**

![Figure 4. Joint 1: inside the sensor puck, cut in half](05-build-plan/joint-01.png)

*Figure 4. Only the base touches the disc and only the disc touches the weight; the weight has 4.5 mm of air round it and above it.*

A thin film of rigid epoxy bonds the weight, centred, to the brass face of the piezo disc; another bonds the disc to the puck base. Nothing else touches the weight: potting must never run below the amplifier board.

**Check before moving on.** 20 mm long, faces parallel within 0.05 mm.

### 3.3 Bought parts for the sensor puck

- **Pot magnet.** 42 mm neodymium pot magnet, about 600 N rated pull on thick steel, with an M6 stud and a keeper plate. Cut the stud to 6 mm with a hacksaw, keeper plate on, and file the end.
- **Piezo disc.** 27 mm brass-backed piezo disc with a 20 mm ceramic and fine leads.
- **Amplifier board.** The charge amplifier built on a round board 31 mm in diameter, 1.6 mm thick, so it rests on the puck's step.
- **Sensor cable.** 2 m shielded four-core cable, 6 mm, with a moulded M12 plug at one end and bare wires at the other.

### 3.4 Logger tube

![Figure 5. Making sketch of the logger tube](../cad/drawings/LKL-DWG-103.png)

*Figure 5. Logger tube making sketch (LKL-DWG-103).*

**What it is and what it is made from.** The body of the logger. PVC pressure pipe, 63 mm outside diameter, 3 mm wall, cut to 232 mm.

**How to make it.**

1. Cut 232 mm with a fine saw in a mitre box; square the ends on abrasive paper laid on a flat board.
2. Chamfer the inside of both ends 1 mm at 30° so the O-rings slide in without being cut. Deburr inside and out.
3. Mark three screw positions at each end, 4 mm from the end and 120° apart, using a paper strip wrapped round the tube.
4. Drill the six holes 4.5 mm only when each plug is in place (section 3.5), so the plug is drilled through the same holes.

**How it fits the parts next to it.** Each plug's spigot slides into one end until its flange meets the tube end. Both O-rings on each plug sit inside the tube, further in than the screws (Figure 10).

**Check before moving on.** The ends are square; the 25 mm of bore at each end, where the O-rings seal, is free of scratches.

### 3.5 Top end plug

![Figure 6. Making sketch of the top end plug](../cad/drawings/LKL-DWG-104.png)

*Figure 6. Top end plug making sketch (LKL-DWG-104).*

**What it is and what it is made from.** The plug that closes the top of the logger and carries the eye bolt, the antenna connector and the internal frame. Acetal (POM) round bar, 65 mm.

**How to make it.**

1. Turn a flange 63 mm in diameter and 4 mm thick, and a spigot 57 mm in diameter and 18 mm long that pushes into the tube by hand.
2. Cut two O-ring grooves in the spigot, 2.5 mm wide and 1.8 mm deep, centred 10 and 15 mm below the flange.
3. Drill a 6.5 mm hole on the axis for the eye bolt, and a 6.5 mm hole 14 mm off the axis for the antenna connector (check its datasheet for the size).
4. On the inner face, drill and tap two M3 holes 6 mm deep for the standoffs: 18 mm each side of the axis, on a line 6 mm from the axis on the side away from the antenna connector.
5. With the plug pushed into the tube and the antenna connector hole pointing where you want it, drill the tube's three top holes 4.5 mm (section 3.4), then drill on into the plug 3.3 mm and tap M4. Put the antenna connector between two screws, not over one.

**How it fits the parts next to it.** See Figure 10 and Figure 12. The flange sits on the tube end; the screws go through the tube 4 mm below the flange.

**Check before moving on.** With greased O-rings the plug pushes in by hand and the screws run in freely.

### 3.6 Bottom end plug

![Figure 7. Making sketch of the bottom end plug](../cad/drawings/LKL-DWG-105.png)

*Figure 7. Bottom end plug making sketch (LKL-DWG-105).*

**What it is and what it is made from.** The plug that closes the bottom of the logger and carries the cable socket. Acetal (POM) round bar, 65 mm.

**How to make it.**

1. Turn the flange and spigot as the top plug, with the two O-ring grooves 10 and 15 mm above the flange.
2. Drill 14.5 mm right through on the axis and tap M16 x 1.5 for the panel socket (check the socket's thread first).
3. Face the outside of the flange flat where the socket's O-ring seats.
4. Drill and tap the three radial holes through the tube, as for the top plug.

**How it fits the parts next to it.**

![Figure 8. Joint 3: bottom end plug and socket, cut in half](05-build-plan/joint-03.png)

*Figure 8. The socket screws into the plug from outside, sealed by its own O-ring; the cable's plug screws onto the socket.*

**Check before moving on.** The socket seats flat on the flange; the plug pushes in by hand.

### 3.7 Internal frame

![Figure 9. Making sketch of the internal frame](../cad/drawings/LKL-DWG-106.png)

*Figure 9. Internal frame (chassis) making sketch (LKL-DWG-106).*

**What it is and what it is made from.** A printed spine that hangs from the top plug and carries the electronics. PETG, 40 % infill.

**How to make it.**

1. Print it lying on its board face, with support under the part of the top tab that stands out on that side. The spine is 48 mm wide, 3 mm thick and 158 mm long.
2. The top tab, 48 by 18 by 4 mm, has two 3.2 mm holes 18 mm each side of centre, 6 mm out on the board side.
3. On the other face (the clip face), from the top: two clips for the capacitor, 8 and 30 mm down; a 22 by 10 by 50 mm pocket for the desiccant, open at the top; and at the bottom two clips for the cell, 10 and 40 mm up. The clips wrap about 200° round their part.
4. On the board face, drill four 2.5 mm pilot holes for the board standoffs, 30 mm apart across and 100 mm apart down, matched to your board.

**How it fits the parts next to it.** Two M3 by 20 mm standoffs screw into the top plug's inner face; two M3 screws come up through the tab into them (step 7). The board sits on four short standoffs on the board face; the cell and capacitor snap into their clips and the desiccant drops into its pocket (step 8).

![Figure 10. Joint 2: top end plug in the tube, cut in half](05-build-plan/joint-02.png)

*Figure 10. Cut through the axis and one radial screw: the screw is 4 mm in from the tube end, outboard of both O-rings, so water stops at the O-rings; a standoff hangs the frame below the plug.*

![Figure 11. Joint 4: cell, capacitor and desiccant on the frame](05-build-plan/joint-04.png)

*Figure 11. The clip face of the frame.*

**Check before moving on.** The frame slides into the tube with about 2.5 mm to spare all round; the cell snaps in and does not fall out when the frame is shaken.

### 3.8 Bought parts for the logger

- **Eye bolt.** M6 by 20 mm stainless eye bolt with a bonded sealing washer and a nyloc nut.
- **Antenna connector.** IP67 SMA female bulkhead with its O-ring and nut, with a short pigtail to the board.
- **Panel socket.** M12 A-coded IP68 front-mount panel socket with an M16 x 1.5 thread, its O-ring and lock nut, and a short four-pin lead to the board.
- **O-rings.** Four nitrile O-rings of 2.5 mm section to suit the 57 mm spigot grooves, and silicone grease.
- **Main board.** STM32WL LoRaWAN module with a 24-bit audio converter, clock, fuse and reverse protection, about 38 by 110 mm, bought or built on a maker's carrier (no board is laid out at this stage).
- **Capacitor.** Hybrid layer capacitor of 0.1 F or more, 16 mm by 30 mm.
- **Cell.** Lithium thionyl chloride C cell, 3.6 V, about 7.7 Ah, with solder tabs, wired to a two-pin plug by the supplier or at stop point S2.
- **Desiccant.** 10 g silica gel pack.
- **Fixings.** Six M4 by 10 mm stainless pan-head screws; two M3 by 20 mm male-female standoffs; four M3 by 3 mm nylon standoffs; M3 screws.

![Figure 12. Joint 8: lanyard, eye bolt and antenna connector](05-build-plan/joint-08.png)

*Figure 12. The lanyard's snap hook clips into the eye bolt; the antenna lead screws onto the connector beside it.*

#### 3.8.1 Wiring

![Figure 13. Block-level wiring](05-build-plan/wiring.png)

*Figure 13. Block-level wiring. No circuit board is laid out at this stage.*

1. Piezo disc leads to the amplifier board's input: short, twisted, soldered before the board goes into the puck.
2. Sensor cable to the amplifier board: supply, ground, signal and spare cores; shield to ground at the board.
3. Panel socket to the main board: the short four-pin lead.
4. Antenna connector to the main board's radio: the pigtail, kept away from the power wires.
5. Capacitor to the main board: 0.5 mm² (20 AWG), short.
6. Cell to the main board through its two-pin plug: 0.5 mm²; the board's fuse and reverse protection are the first things on this lead.

**Check before moving on.** Every wire continues end to end; with the cell unplugged, the cell connector on the board reads open between its pins.

### 3.9 Neck bar outer tube

![Figure 14. Making sketch of the outer tube](../cad/drawings/LKL-DWG-107.png)

*Figure 14. Neck bar outer tube making sketch (LKL-DWG-107).*

**What it is and what it is made from.** The fixed half of the bar, which carries the antenna bracket and the lanyard. Aluminium square tube, 20 by 20 by 1.5 mm, 6063 class.

**How to make it.**

1. Cut 350 mm; square and deburr both ends.
2. Measuring from the end that takes the fixed foot: a 5.5 mm hole at 130 mm for the bracket bolt, and a 6.5 mm hole at 320 mm for the locking pin, each through the top and bottom walls. Drill each pair straight through in a drill stand.
3. Press a 20 mm square tube insert with an M10 nut into the fixed-foot end.

**How it fits the parts next to it.** The inner tube slides into the open end with 0.5 mm clearance each side; the pin passes through both tubes.

![Figure 15. Joint 5: inner tube in the outer tube, cut in half](05-build-plan/joint-05.png)

*Figure 15. The two tubes and the locking pin.*

**Check before moving on.** The inner tube slides the full length without binding.

### 3.10 Neck bar inner tube

![Figure 16. Making sketch of the inner tube](../cad/drawings/LKL-DWG-108.png)

*Figure 16. Neck bar inner tube making sketch (LKL-DWG-108).*

**What it is and what it is made from.** The sliding half of the bar, which sets its length. Aluminium square tube, 16 by 16 by 1.5 mm, 6063 class.

**How to make it.**

1. Cut 350 mm; square and deburr.
2. Drill seven 6.5 mm holes through the top and bottom walls, 20 mm apart, from 20 to 140 mm from the plain end.
3. Press a 16 mm square tube insert with an M10 nut into the other end.

**How it fits the parts next to it.** Set the bar about 20 mm shorter than the neck with the pin in the right hole; the adjusting foot takes up the rest. With seven holes and about 30 mm of foot travel the bar spans necks of about 570 to 710 mm; the example chamber's 600 mm neck uses the sixth hole from the plain end.

![Figure 17. Joint 6: the fixed foot against the neck wall](05-build-plan/joint-06.png)

*Figure 17. The rubber-padded foot screws into the insert in the tube end and bears on the neck wall; the foot at the other end is the same, wound out to wedge the bar.*

**Check before moving on.** The pin drops through both tubes at every hole.

### 3.11 Antenna bracket

![Figure 18. Making sketch of the antenna bracket](../cad/drawings/LKL-DWG-109.png)

*Figure 18. Antenna bracket making sketch (LKL-DWG-109).*

**What it is and what it is made from.** A flat plate that holds the antenna on top of the bar. Aluminium flat bar, 40 by 3 mm, 6082 class.

**How to make it.**

1. Cut 100 mm; round the corners about 3 mm and deburr.
2. On the centre line, drill a 5.5 mm hole 15 mm from one end for the bolt, and a hole 60 mm from the same end to suit the antenna's centre stud (16.5 mm for an M16 stud; check the antenna's datasheet).

**How it fits the parts next to it.**

![Figure 19. Joint 7: antenna bracket on the bar](05-build-plan/joint-07.png)

*Figure 19. Seen from below: one M5 bolt through the bracket and the outer tube, nyloc nut under the tube; the antenna's stud nut sits under the bracket, clear of the tube.*

The bracket lies flat across the top of the outer tube with its bolt hole over the tube; the antenna's centre is 45 mm off the bar's centre line.

**Check before moving on.** With the bolt tight the bracket cannot be turned by hand.

### 3.12 Bought parts for the neck bar

- **Feet.** Two M10 levelling feet with 40 mm rubber pads and at least 40 mm of thread.
- **Tube inserts.** One 20 mm and one 16 mm square tube insert, each with an M10 nut, for 1.5 mm wall.
- **Locking pin.** 6 mm pin about 30 mm long with an R-clip.
- **Lanyard.** 3 mm stainless wire rope, about 150 mm, with a loop and ferrules at one end and a stainless snap hook at the other.
- **Antenna.** Flat puck antenna about 70 mm across for the regional LoRaWAN band, with a threaded centre stud and nut, and a 1 m low-loss lead ending in an SMA plug.
- **Fixings.** One M5 by 30 mm stainless bolt with a nyloc nut.

## 4. Putting it together

In each picture the parts already fitted are grey and the parts being fitted are in colour, with an arrow showing the way they go in.

### Step 1: piezo disc and seismic mass into the puck

![Step 1](05-build-plan/step-01.png)

A thin film of rigid epoxy under the disc and another under the weight, both centred. Cure flat for 24 hours.

### Step 2: amplifier board and cable

![Step 2](05-build-plan/step-02.png)

Pass the cable's bare end down through the puck's mouth and solder it and the disc leads to the board, then lay the board on the step. **Hold point:** the board sits flat on the step and the weight is free (look from the side with a lamp).

### Step 3: pot the top of the puck

![Step 3](05-build-plan/step-03.png)

Pour potting compound to the rim, above the board only. Hold the cable upright until it sets.

### Step 4: pot magnet onto the puck

![Step 4](05-build-plan/step-04.png)

Medium threadlocker on the stud; screw the magnet into the base hand tight. Leave the keeper plate on.

### Step 5: fit the top end plug

![Step 5](05-build-plan/step-05.png)

Eye bolt with its sealing washer outside and nyloc nut inside; antenna connector with its O-ring outside and nut inside; the two standoffs into the inner face; greased O-rings into both grooves.

### Step 6: fit the bottom end plug

![Step 6](05-build-plan/step-06.png)

Socket in from outside with its O-ring, lock nut inside; greased O-rings into both grooves.

### Step 7: frame onto the top plug

![Step 7](05-build-plan/step-07.png)

Two M3 screws up through the frame's tab into the standoffs, before anything else goes on the frame.

### Step 8: electronics onto the frame

![Step 8](05-build-plan/step-08.png)

Board on its four standoffs on the board face; antenna pigtail to the board; capacitor into its clips; desiccant into its pocket; the cell into its clips last, its plug left unplugged. **Hold point:** stop point S2 before the cell is plugged in.

### Step 9: bottom plug into the tube

![Step 9](05-build-plan/step-09.png)

Push the plug in until its flange meets the tube end; three M4 screws through the tube into the plug.

### Step 10: close the logger

![Step 10](05-build-plan/step-10.png)

Plug the socket's lead into the board, slide the frame into the tube and push the top plug home; three M4 screws. **Hold point:** stop point S3.

### Step 11: assemble the neck bar

![Step 11](05-build-plan/step-11.png)

Slide the inner tube into the outer, pin it at the hole that suits the neck, and screw a foot into each insert, the fixed foot fully home.

### Step 12: antenna bracket and antenna onto the bar

![Step 12](05-build-plan/step-12.png)

Bolt the bracket across the outer tube; put the antenna's stud through the bracket and fit its nut underneath.

### Step 13: hang the logger and connect the antenna

![Step 13](05-build-plan/step-13.png)

Loop the lanyard round the outer tube beside the bracket, clip the snap hook into the eye bolt, and screw the antenna lead onto the connector. Coil the spare lead and tie it to the lanyard.

### Step 14: set the bar in the chamber neck

![Step 14](05-build-plan/step-14.png)

For the prototype, use a bench frame with two walls 600 mm apart. From above, lower the set until the bar is below the frame, put the fixed pad against one wall and wind the other foot out by hand until the bar does not move when pushed. **Hold point:** stop point S5.

### Step 15: sensor puck onto the spindle cap

![Step 15](05-build-plan/step-15.png)

Take the keeper plate off only at the cap; lower the puck by its cable (or on a placing pole) until the magnet takes hold; screw the cable's plug onto the logger's socket.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of LKL-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Logger seals | R11 | Logger closed with no electronics, submerged under 1 m of water for 1 hour, then opened | No water inside; a paper tissue in the tube stays dry |
| Weight stands free | R3, R4 | Look into the puck from the side with a lamp before potting | Light all round the weight; nothing touches it but the disc |
| Sensor responds | R4 | Puck on a steel block on the bench; tap the block lightly; read the amplifier output on an oscilloscope | A clean response that dies away; no output when the block is still |
| Magnet hold | R9 | Spring balance hooked to the puck on a painted steel cap | 100 N or more before it lets go |
| Cell and supply | R6 | Cell plugged in; measure current in sleep and while listening | Near the 4 µA and 12 mA of LKL-CAL-001 |
| Radio | R7, R14 | Logger and antenna on the bar under a steel plate in place of the cover; one uplink to a nearby gateway | The 24-byte summary is received |
| Bar holds | R10 | Bar set in a 600 mm bench frame; logger hung; push and pull on the logger | The bar does not move; the pads do not slip |
| Size and mass | R12 | Measure and weigh the logger, cable and puck, then the bar | 70 mm or less across, 300 mm or less long; record both masses |
| Install time | R10 | Time steps 14 and 15 at the bench frame | Recorded against the 10 min target |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the cell comes into the workshop.** The cell is in its packaging, undamaged, with its maker's datasheet; it is stored away from metal and heat. A non-combustible surface (a ceramic tile or steel tray) and a fire extinguisher for electrical fires are within reach of the bench.
- **S2. Before the cell is plugged in.** The board's fuse and reverse protection are fitted and checked with a meter; the cell plug's polarity matches the board, checked with a meter, not by wire colour; no charging circuit of any kind is connected. The cell has never been soldered near its body.
- **S3. Before the logger is closed.** The cell is plugged in only if the bench check of its current has been done; every wire is clear of the O-rings; a fresh desiccant pack is in its pocket.
- **S4. Before the magnet's keeper plate comes off.** The puck is at the cap or on a steel block; hands are clear of the gap; nobody with a pacemaker or implant is close.
- **S5. Before any trial in a real chamber (outside this plan).** The utility's written permission; the cover lifted with a lifting key by two people; traffic management in place; nobody enters the chamber, and nobody leans into the opening without the utility's gas test and confined space rules.

## 7. Tools, skills and workspace

**Tools.** Lathe with a boring bar (or a machining service) for the puck body, the brass weight and the two end plugs; hacksaw and mitre box; bench drill or a drill in a stand; drills 2.5 to 16.5 mm; M3, M4, M6 and M16 x 1.5 taps with their drills; deburring tool; files; calipers, steel rule and square; 3D printer that prints PETG; soldering iron; wire strippers; multimeter; oscilloscope (for the first checks); spring balance to 200 N; scale to 2 kg; stopwatch.

**Skills.** No certified trade is needed. Basic turning, drilling and tapping; through-hole and fine-wire soldering; mixing and pouring two-part potting and epoxy; care with lithium primary cells and strong magnets. All circuits are extra-low voltage, 3.6 V at the cell; no mains wiring is part of this build.

**Workspace.** A bench about 1.2 by 0.6 m; a turning and drilling corner kept apart from the electronics so chips stay off the boards; a ventilated place for potting and printing; the cell area of S1; a bench frame with two solid walls 600 mm apart for steps 14 and 15.

**Personal protective equipment.** Safety glasses for turning, drilling, cutting and soldering; nitrile gloves for epoxy and potting; no gloves near a turning lathe or drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/LKL-DWG-101` to `LKL-DWG-109`.
- General arrangement: `cad/drawings/LKL-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (LKL-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; mass [K1], cable reach [K2], install time [K3], flooding [J2], resonance [F6].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (LKL-DDR-003), with LKL-DDR-001 and LKL-DDR-002; open items in `docs/06-design-decisions.md` (LKL-DEC-001).
- Requirements: `docs/03-requirements.md` (LKL-REQ-001 v0.5).
