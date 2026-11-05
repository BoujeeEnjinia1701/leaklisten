"""LeakListen STEM check calculations (LKL-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. Claims S1 to S14 are for option A (the current design, a magnet-on contact
sensor); SB1 to SB4 are for option B (hydrant cap hydrophone) and SC1 to SC3 for option C (ground spike geophone).
Option A's numbers come from the calculation note (LKL-CAL-001, docs/04-calcs/sizing.py), which this script imports
(about 10 s: it builds the model). The B and C rows are first-order screens on assumed data, labelled as such; the
assumptions are named in the code and in the document. Nothing here is a measurement.
"""
import math
import sys

sys.path.insert(0, ".kit")
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX  # noqa: E402,F401

sys.path.insert(0, "docs/04-calcs")
import sizing as CAL  # noqa: E402  LKL-CAL-001, reads cad/src/model.py

c = Check()
P = CAL.P
RHO = CAL.RHO

# ------------------------------------------------------------------------------------------ option A
# Physics: the leak itself
c.order_of_magnitude("S1", "The jet of the reference leak (5 L/min at 3 bar) carries about 25 W of mechanical power, of which only a small fraction (1e-6 to 1e-4, assumed) becomes sound", "Physics", "Fluid mechanics",
                     claimed=25.0, estimate=CAL.Q * CAL.DP, unit="W", law="Jet power = volume flow x pressure drop (Bernoulli)",
                     closed_by="LKL-CAL-001 G1")
iron, pvc = CAL.rng["ductile iron DN150"], CAL.rng["PVC DN150"]
FLAG = math.sqrt(10 ** 0.6 - 1)        # the flag rule needs the night level up 6 dB: leak = 1.73 x the noise (independent review)


def detect_range_flag(pipe, eff):
    """LKL-CAL-001 detect_range with the leak required to lift the noise floor by 6 dB, not just reach it."""
    E, a, h, _ = pipe
    S = math.pi * (a - h / 2) ** 2
    w_dir = CAL.W_mech * eff / 2
    best = 0.0
    for fc in CAL.third_octaves():
        cc = 2 * math.pi * fc / CAL.wavenumber(fc, pipe).real
        p2 = w_dir * RHO * cc / S / (CAL.F_HI - CAL.F_LO)
        Ev, av, hv = CAL.VALVE
        acc = CAL.C_V * (2 * math.pi * fc) ** 2 * av ** 2 / (Ev * hv) * math.sqrt(p2) / 9.81
        n = math.hypot(CAL.background_g(fc), CAL.self_noise_g(fc)) * FLAG
        if acc > n:
            best = max(best, 20 * math.log10(acc / n) / CAL.att_db_per_m(fc, pipe))
    return best


iron_flag = {e: detect_range_flag(CAL.PIPES["ductile iron DN150"], e) for e in CAL.EFFS}
c.claim("S2", "A leak noise logger on a valve hears the reference leak 100 m along a ductile iron main", "Physics", "Acoustics and vibration",
        f"Fluid-dominated axial wave in a shell (Pinnington and Briscoe; Gao et al. 2004), flat leak spectrum, acoustic efficiency 1e-5 (assumed), 0.5 ug/rtHz background, valve coupling -10 dB (assumed). Signal equal to noise (LKL-CAL-001 G2) gives {iron[1]:.0f} m; the flag rule needs the level up 6 dB (leak 4.8 dB above the noise), which gives the value below; at efficiency 1e-6 / 1e-5 / 1e-4 it is {iron_flag[1e-6]:.0f} / {iron_flag[1e-5]:.0f} / {iron_flag[1e-4]:.0f} m. The mount's resonance (S6) is not applied to the signal",
        round(iron_flag[1e-5], 0), 100.0, "m", rule="above", margin=1.0,
        closed_by="")
c.cited("S3", "The same contact sensor hears the reference leak 30 m along a PVC main", "Physics", "Acoustics and vibration",
        f"Axial attenuation on PVC DN150 is 0.42 dB/m at 100 Hz against 0.011 dB/m on ductile iron (LKL-CAL-001 E1); the central estimate is {pvc[1]:.0f} m",
        f"{pvc[1]:.0f} m against 30 m: the detail fails. Fix already decided by Amish (2026-09-25, LKL-DDR-002 D8): the contact sensor serves metallic mains only; plastic mains are served by a hydrophone (option B, S-B rows)",
        FIX, closed_by="LKL-DDR-002 D8; option B")
c.cited("S4", "The piezo charge amplifier reaches about 1 ug/rtHz equivalent input noise from 100 Hz to 1 kHz", "Physics", "Electromagnetism and electronics",
        f"Charge amplifier noise: voltage noise x total input capacitance, feedback resistor and ceramic loss noise, divided by charge sensitivity (53 g mass, d33 300 pC/N, 5 nV/rtHz op-amp, all assumed): {CAL.r4 * 1e6:.2f} ug/rtHz worst against 1.0, so the order is right and the margin is nil. Noise scales as 1/d33. The 24-bit audio ADC is assumed to reach about 2 uV rms over 20 kHz (adds under 0.01 ug/rtHz); a 12-bit converter would add 0.1 ug/rtHz or more",
        "Ceramic, op-amp and ADC datasheets of the chosen parts", PLAUSIBLE, closed_by="")
c.claim("S5", "The piezo and seismic mass resonate far above the 2 kHz band", "Physics", "Acoustics and vibration",
        "Spring-mass resonance, f = sqrt(k/m) / 2 pi, k of a 20 mm ceramic in compression (E 63 GPa)", round(CAL.f_seis / 1000, 0), 10.0, "kHz", rule="above",
        closed_by="LKL-CAL-001 F5")
f_lo = math.sqrt(5e6 / CAL.m_stack) / 2 / math.pi * math.sqrt(1 - 1 / math.sqrt(2))
c.cited("S6", "The magnet-mounted sensor is flat within 3 dB from 5 Hz to 2 kHz after correction", "Physics", "Acoustics and vibration",
        f"The 277 g puck and magnet on the contact stiffness of a coated cap (5e6 to 2e7 N/m) resonate at 676 to 1,352 Hz, inside the band, and are flat only to {f_lo:.0f} to {2 * f_lo:.0f} Hz (LKL-CAL-001 F6). A mounted resonance is a narrow peak that a digital equaliser can correct, if its frequency is known per mounting",
        "Needs a shaker comparison of the mounted sensor (CalRig bay, decided 2026-10-02) at TRL 4; the contact stiffness is assumed", PLAUSIBLE, closed_by="")

# Chemistry and electrochemistry: the cell and the radio pulses
life_min = min(v[1] for v in CAL.life.values())
worst_mah = max(v[0] for k, v in CAL.life.items() if "TRL 2" not in k)
q_cap = CAL.CELL_AH * CAL.USABLE * 1000 / (10 * 365)
c.claim("S7", "One C-size lithium thionyl chloride cell runs the logger for 10 years", "Chemistry", "Electrochemistry and batteries",
        "Charge budget: 7.7 Ah nominal x 0.70 usable (cold, pulses) divided by 3,650 days; daily charge from sleep, listening, radio, self-discharge and status light",
        round(worst_mah, 2), round(q_cap, 2), "mAh/day", closed_by="LKL-CAL-001 C1, C2")
cap_needed = max(max(itx - CAL.I_CELL, 0) * CAL.toa(sf, CAL.PHY) / (CAL.V_HI - CAL.V_LO) for sf, itx in ((12, 45e-3), (9, 120e-3)))
c.claim("S8", "A 0.1 F hybrid layer capacitor carries the radio pulse the cell cannot supply", "Chemistry", "Electrochemistry and batteries",
        "C = (I_tx - I_cell_max) x airtime / allowed droop 0.5 V (3.6 V to 3.1 V); I_cell_max 30 mA for a C-size Li-SOCl2 cell with a hybrid capacitor (manufacturer data, to confirm)",
        round(cap_needed, 3), 0.1, "F", closed_by="LKL-CAL-001 C3")
c.cited("S9", "The lithium thionyl chloride cell keeps its capacity for 10 years at 2 to 20 degC and delivers the pulses after long rest (passivation)", "Chemistry", "Electrochemistry and batteries",
        "Li-SOCl2 cells self-discharge about 1 % a year but build a passivation layer that lowers the first pulse voltage; a hybrid layer capacitor is the standard remedy (Saft and Tadiran application notes, to cite from the datasheets of the chosen cell)",
        "Manufacturer datasheet and a pulse test of the chosen cell at TRL 4", PLAUSIBLE, closed_by="")

# Physics: radio, magnet, flotation
g_gw = CAL.link
eu_budget = 14.0 + CAL.G_NODE - CAL.L_NODE + CAL.G_GW - CAL.L_GW - CAL.sens(12)
m05 = eu_budget - CAL.hata_urban(868, CAL.GW_KM) - 20.0 - CAL.FADE
c.cited("S10", "A LoRa uplink leaves a chamber under a cast-iron cover and reaches a gateway 0.5 km away", "Physics", "Electromagnetism and electronics",
        f"Link budget with Hata urban path loss, 10 dB fade margin and an assumed 20 dB cover loss: {m05:+.1f} dB at 0.5 km for EU868 SF12 (LKL-CAL-001 D5), {CAL.link[('US915 SF9 +20 dBm', 'iron cover (central)')][0]:+.1f} dB at 1 km for US915 SF9 is negative; the cover loss is unmeasured and a tight flooded cover (30 dB) fails; the Hata model is stated for 1 to 20 km, so 0.5 km is an extrapolation (independent review)",
        "Cover loss to measure on a real chamber at TRL 4; gateway placement decided (LKL-DDR-002 D7)", PLAUSIBLE, closed_by="")
hold = P["magnet_rated_n"] * CAL.IRON / (1 + 0.5 / CAL.G0) ** 2
c.claim("S11", "The 42 mm pot magnet holds the puck on a spindle cap with a 0.5 mm paint and rust gap", "Physics", "Electromagnetism and electronics",
        "Pull force falls with the air gap as F = F_iron / (1 + g/g0)^2, g0 0.6 mm (a rule of thumb fitted to catalogue curves, assumed); 70 % of the rated pull on a typical cap; against 100 N (about 30 x the 3 N weight of the puck and 0.5 m of cable, LKL-CAL-001 I2); a straight pull-off only: shear or peel from a snagged cable or a knock, a sliding resistance near 0.2 x the pull, and the real contact area of a spindle cap smaller than the 42 mm pole face are not checked",
        round(hold, 0), 100.0, "N", rule="above", margin=0.3, closed_by="LKL-CAL-001 I1, I2")
c.claim("S12", "A flooded logger floats on its lanyard", "Physics", "Fluid mechanics",
        "Archimedes: logger mass against the mass of water displaced by its 63 x 240 mm body", round(CAL.logger_m, 3), round(CAL.buoy, 3), "kg",
        closed_by="LKL-CAL-001 J2")

# Mathematics
c.claim("S13", "The 24-byte summary fits every LoRaWAN rate used (EU868 SF12 limit 51 B, US915 SF9 limit 53 B)", "Mathematics", "Units and dimensional analysis",
        "Application payload limits of the LoRaWAN Regional Parameters (TS001) with 13 B of protocol overhead already counted", CAL.APP, 51, "B",
        closed_by="LKL-CAL-001 B2")
p3 = CAL.qfunc(6.0 / 2.0) ** 3
c.claim("S14", "Random night-to-night variation (2 dB) raises fewer than 1 false flag per 20 loggers per month", "Mathematics", "Statistics",
        "Gaussian tail: flag at +6 dB for 3 independent nights, p = Q(6/sigma)^3, nights taken as independent (nightly minima are in fact correlated, and the 14-night baseline error is shared); real site noise (pumps, pressure reducing valves) is not random and is not covered",
        float(f"{20 * 30 * p3:.2g}"), 1.0, "per 20 loggers per month", closed_by="LKL-CAL-001 L1")
c.cited("S15", "Site noise (pumps, pressure reducing valves, night use) does not mimic a leak in a way a 14-night baseline cannot remove", "Engineering and technology",
        "Signal processing and standards practice",
        "Commercial noise loggers rely on night-time minimum levels and trends, and still produce false positives that need a follow-up survey (Gutermann, Hunaidi and Chu 1999)",
        "Field data from a partner network at TRL 4", PLAUSIBLE, closed_by="")
c.cited("S16", "Nothing in option A touches drinking water or changes its quality", "Biology", "Microbiology and public health",
        "The magnet sits on a spindle cap in the chamber air; the housing is PVC pipe outside the water; no part is fixed to the pipe. A design review, not a calculation",
        "Confirmed by the model: no part of option A passes through a pipe wall", WITHIN, closed_by="LKL-CAL-001 J; design review")

# ------------------------------------------------------------------------------------------ option B
# Hydrophone on a hydrant cap: pressure of the leak noise in the water column against the hydrophone's noise
KT = CAL.KT
A_el = math.pi * 11.6e-3 * 20e-3                   # electrode area of the 11.6 mm x 20 mm tube, m2
T_W, R_O = 2.3e-3, 5.8e-3                          # wall and outer radius, m
D31 = 130e-12                                      # C/N, soft PZT (assumed)
Q_PER_PA = D31 * (R_O / T_W) * A_el                # C/Pa, hoop stress p r / t on a radially poled tube (first order)
C_TUBE = 8.854e-12 * 1800 * A_el / T_W
BG_PA = 0.1                                        # Pa/rtHz background in the pipe water at night (assumed; 0.01 to 1 bracket)


def hydro_noise_pa(f):
    en = CAL.EN * math.sqrt(1 + CAL.F_CORNER / f)
    q_v = en * (C_TUBE + CAL.C_F_AMP)
    q_r = math.sqrt(4 * KT / CAL.R_F) / (2 * math.pi * f)
    q_l = math.sqrt(4 * KT * C_TUBE * CAL.TAND / (2 * math.pi * f))
    return math.sqrt(q_v ** 2 + q_r ** 2 + q_l ** 2) / Q_PER_PA


def hydro_range(pipe, eff, bg, k=FLAG):
    E, a, h, _ = pipe
    S = math.pi * (a - h / 2) ** 2
    w_dir = CAL.W_mech * eff / 2
    best = 0.0
    for fc in CAL.third_octaves():
        cc = 2 * math.pi * fc / CAL.wavenumber(fc, pipe).real
        p = math.sqrt(w_dir * RHO * cc / S / (CAL.F_HI - CAL.F_LO))
        n = math.hypot(bg * max(1.0, 100.0 / fc), hydro_noise_pa(fc)) * k
        if p > n:
            best = max(best, 20 * math.log10(p / n) / CAL.att_db_per_m(fc, pipe))
    return best


pvc_pipe, pe_pipe = CAL.PIPES["PVC DN150"], CAL.PIPES["PE100 DN150 SDR11"]
rb = {bg: hydro_range(pvc_pipe, 1e-5, bg) for bg in (0.01, 0.1, 1.0)}
rb_eff = {e: hydro_range(pvc_pipe, e, BG_PA) for e in (1e-6, 1e-5, 1e-4)}
c.claim("SB1", "A hydrophone on a hydrant cap hears the reference leak 30 m along a PVC main", "Physics", "Acoustics and vibration",
        f"Leak pressure in the water column (flat source spectrum, efficiency 1e-5, wave speed and attenuation of LKL-CAL-001 E1) against a {BG_PA} Pa/rtHz night background at 100 Hz and above, rising as 1/f below (assumed) and the tube's charge-amplifier noise ({hydro_noise_pa(100) * 1e3:.2f} mPa/rtHz at 100 Hz); background 0.01 / 0.1 / 1 Pa/rtHz gives {rb[0.01]:.0f} / {rb[0.1]:.0f} / {rb[1.0]:.0f} m on PVC; PE100 at 0.1 Pa/rtHz {hydro_range(pe_pipe, 1e-5, 0.1):.0f} m; efficiency 1e-6 / 1e-5 / 1e-4 at 0.1 Pa/rtHz gives {rb_eff[1e-6]:.0f} / {rb_eff[1e-5]:.0f} / {rb_eff[1e-4]:.0f} m; the 6 dB flag rule is applied; branch and hydrant insertion losses are not",
        round(rb[BG_PA], 0), 30.0, "m", rule="above", margin=3.0, closed_by="")
p_cap = 10e5                                       # Pa, assumed worst hydrant static pressure 10 bar (16 bar rated surge to assess)
r_stub = 0.032
sig_cap = 3 * (3 + 0.3) * p_cap * r_stub ** 2 / (8 * 0.016 ** 2)      # simply supported circular plate, Roark
f_bolt = p_cap * math.pi * r_stub ** 2
sig_bolt = f_bolt / 4 / 84.3e-6                                          # four M12 bolts, tensile stress area 84.3 mm2
c.claim("SB2", "The 16 mm stainless cap and four M12 bolts hold a 10 bar hydrant, with a 3 x margin", "Physics", "Strength of materials",
        f"Simply supported circular plate, sigma = 3 (3 + nu) p r^2 / (8 t^2), nu 0.3, r 32 mm; the water acts on the 64 mm bore (the plate between the bore and the 170 mm bolt circle rests on the flange); bolt preload and gasket load are not included; bolts at {f_bolt / 1e3:.1f} kN shared by four M12 (84.3 mm2); plate {sig_cap / 1e6:.1f} MPa and bolts {sig_bolt / 1e6:.0f} MPa against the 205 MPa proof of 316 and 450 MPa of A4-70, both divided by 3",
        round(max(sig_cap / 205e6, sig_bolt / 450e6) * 3, 2), 1.0, "ratio to proof",
        closed_by="")
c.cited("SB3", "A stainless cap, EPDM gasket and PU-potted hydrophone do not change drinking water quality", "Biology", "Microbiology and public health",
        "Products in contact with drinking water need approval in many jurisdictions (UK Regulation 31, DWI and WRAS); stainless steel and EPDM grades with approvals exist, the potting compound and cable jacket do not yet have a chosen approved grade",
        "Approved grades to select with the partner utility; not assessed here", PLAUSIBLE, closed_by="")
c.cited("SB4", "The cap bolts to the hydrant outlet", "Engineering and technology", "Manufacturing tolerances",
        "The model assumes a four-bolt 170 mm flange outlet (an assumption). Commercial hydrophone caps are made for threaded 2.5 inch outlets (SubSurface Enigma 3 kit lists 2.5 inch stainless hydrant caps); outlet type varies by country and utility",
        "Outlet type and thread to confirm with the partner; the cap interface would be redesigned for it", PLAUSIBLE, closed_by="")

# ------------------------------------------------------------------------------------------ option C
# Geophone in the verge: ground-borne leak noise radiating from a buried main
RHO_SOIL, C_SOIL, Q_SOIL = 1800.0, 200.0, 20.0     # kg/m3, m/s (shear-dominated, loose soil), quality factor (assumed)
SENS_GEO, EN_GEO = 28.8, 5e-9                      # V/(m/s) (typical 4.5 Hz geophone), V/rtHz preamp
V_BG = 1e-8                                        # m/s/rtHz urban ground noise at night, 50 to 500 Hz (assumed; 1e-9 to 1e-7 bracket)


def geo_snr_db(offset_m, eff=1e-5, f=100.0, v_bg=V_BG):
    w = CAL.W_mech * eff                           # W, radiated into the ground (a pessimistic share of the leak power)
    inten = w / (2 * math.pi * offset_m ** 2) * math.exp(-2 * math.pi * f / (Q_SOIL * C_SOIL) * offset_m * 2)
    v = math.sqrt(inten / (RHO_SOIL * C_SOIL)) / math.sqrt(CAL.F_HI - CAL.F_LO)
    n = math.hypot(v_bg, EN_GEO / SENS_GEO)
    return 20 * math.log10(v / n)


c.cited("SC1", "A geophone at 0.5 m depth in the verge hears the reference leak from a main 3 m away", "Physics", "Acoustics and vibration",
        f"Hemispherical spreading of the leak's ground-borne power (efficiency 1e-5, soil density {RHO_SOIL:.0f} kg/m3, wave speed {C_SOIL:.0f} m/s, Q {Q_SOIL:.0f}) against {V_BG:.0e} m/s/rtHz urban ground noise (assumed): signal to noise {geo_snr_db(3.0):+.0f} dB at 3 m, {geo_snr_db(3.0, v_bg=1e-7):+.0f} dB with 10 x the ground noise, {geo_snr_db(3.0, eff=1e-6):+.0f} dB at 10 x less efficiency, {geo_snr_db(10.0):+.0f} dB at 10 m. Reach is a few metres, not the 100 m of option A",
        "Ground noise and efficiency are unknown; a recording beside a known leak is TRL 4 work", PLAUSIBLE, closed_by="")
p_soil = 0.5 * 18e3 * 0.5                          # Pa, K0 0.5 x unit weight 18 kN/m3 x depth 0.5 m
sig_wall = 0.75 * p_soil * 0.30 ** 2 / 0.010 ** 2
E_CREEP = 250e6                                    # Pa, HDPE long-term modulus for a lid and wall under years of load (estimate, grade to confirm)
defl = 5 * (p_soil * 1.0) * 0.30 ** 4 / (384 * E_CREEP * (1.0 * 0.010 ** 3 / 12))
c.cited("SC2", "The 10 mm HDPE wall of the ground box carries the soil pressure at 0.5 m depth", "Physics", "Strength of materials",
        f"One-way strip of the 0.30 m short side, sigma = 0.75 p L^2 / t^2 = {sig_wall / 1e6:.2f} MPa at the at-rest pressure {p_soil / 1e3:.1f} kPa, against the 5 MPa long-term design stress used for HDPE in the sister repo TideFlap (an estimate); but the creep deflection of the strip at a long-term modulus of {E_CREEP / 1e6:.0f} MPa is {defl * 1e3:.0f} mm, about {defl / 0.30 * 100:.0f} % of the span, so the wall needs ribs or more thickness; traffic or foot surcharge on the verge and the lid (not rated for vehicles) are not checked",
        "Stress passes, stiffness does not: ribs or a 15 mm wall to propose (LKL-RSK-001)", PLAUSIBLE, closed_by="")
c.cited("SC3", "A stainless spike driven 0.5 m into soil couples the geophone to the ground and survives driving", "Engineering and technology", "Manufacturing tolerances",
        "A 22 mm spike with a cone tip is a standard geophone spike geometry; driving through stony or compacted verge may bend it and a buried pipe can be struck (a strike hazard, risk register)",
        "Soil and utility records to check at each site; no test at TRL 3", PLAUSIBLE, closed_by="")

if __name__ == "__main__":
    print(f"Hydrophone: {Q_PER_PA * 1e12:.2f} pC/Pa, tube {C_TUBE * 1e9:.1f} nF, noise {hydro_noise_pa(100) * 1e3:.3f} mPa/rtHz at 100 Hz; ranges on PVC at 0.01/0.1/1 Pa: {rb}")
    print(f"Cap: plate {sig_cap / 1e6:.1f} MPa, bolt force {f_bolt / 1e3:.2f} kN, bolt stress {sig_bolt / 1e6:.0f} MPa")
    print(f"Geophone SNR at 3 m {geo_snr_db(3.0):+.1f} dB, 10 m {geo_snr_db(10.0):+.1f} dB; ground box wall {sig_wall / 1e6:.2f} MPa, soil {p_soil:.0f} Pa")
    c.write()
