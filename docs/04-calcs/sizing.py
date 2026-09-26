"""LeakListen sizing calculations, LKL-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[B3] that the note cites, and the requirement status table is also written to
docs/04-calcs/results.csv. Geometry comes from cad/src/model.py (PARAMS and derived), the parts
cost from bom/bom.csv and the budget from project.yaml. First-principles estimates for a paper
proof of concept; not a substitute for tests.
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, build_parts  # noqa: E402

D = derived(P)
LOG10 = math.log10


def tag(t, text):
    print(f"[{t}] {text}")


def db(x):
    return 10 * LOG10(x)


print("LeakListen sizing, LKL-CAL-001 v0.1")
print(f"Geometry from cad/src/model.py: logger {P['tube_od']:.0f} x {P['logger_len']:.0f} mm, "
      f"puck {P['puck_d']:.0f} x {P['puck_h']:.0f} mm, seismic mass {P['mass_d']:.0f} x {P['mass_h']:.0f} mm brass")

# ================================================================== A. Data and processing (R5, R8)
print("\nA. Nightly data, processing and payload")
FS = 8000            # S/s
WIN, NWIN = 20.0, 12  # s per window, windows per night
BANDS, F_LO, F_HI = 64, 5.0, 2000.0
raw = NWIN * WIN * FS * 2
tag("A1", f"sampled per night {NWIN} x {WIN:.0f} s x {FS} S/s x 2 B = {raw / 1e6:.2f} MB; "
          f"12 spectra x {BANDS} bands x 2 B = {NWIN * BANDS * 2 / 1e3:.2f} kB kept in RAM")
ratio = (F_HI / F_LO) ** (1 / BANDS)
bw = lambda f: f * (ratio - 1)
stages = [("full rate", FS, 1024, 80.0, F_HI), ("decimate by 8", FS / 8, 1024, 10.0, 80.0),
          ("decimate by 32", FS / 32, 512, F_LO, 10.0)]
ram = 0
for name, fs, n, lo, hi in stages:
    res = fs / n
    ok = res <= bw(lo)
    ram += n * 2 * 2 + n * 2 * 2          # double input buffer (q15) + complex q15 work buffer
    tag("A2", f"{name}: {fs:.0f} S/s, {n}-point FFT, {res:.2f} Hz bins for bands {lo:g} to {hi:g} Hz "
              f"(narrowest band {bw(lo):.2f} Hz): {'resolved' if ok else 'NOT resolved'}")
ram += BANDS * 4 * 2 + NWIN * BANDS * 2
STACK = 32 * 1024
tag("A3", f"signal RAM {ram / 1024:.1f} kB + LoRaWAN stack allowance {STACK // 1024} kB = "
          f"{(ram + STACK) / 1024:.1f} kB of 64 kB (STM32WLE5); fixed-point q15 (no FPU on the STM32WL)")
PAYLOAD = {"night minimum level": 1, "10th percentile level": 1, "16 band levels, 1 dB steps": 16,
           "peak band index": 1, "steadiness index": 1, "battery voltage": 1, "temperature": 1,
           "flags and sequence": 2}
APP = sum(PAYLOAD.values())
tag("A4", f"summary payload {APP} bytes (was about 50 at TRL 2): " + ", ".join(f"{k} {v}" for k, v in PAYLOAD.items()))

# ================================================================== B. LoRaWAN airtime (R7, R14)
print("\nB. LoRaWAN airtime and payload limits")
OVERHEAD = 13        # MHDR 1 + FHDR 7 + FPort 1 + MIC 4


def toa(sf, pl, bw=125e3, cr=1, preamble=8):
    """LoRa time on air (s), Semtech AN1200.13 formula, explicit header, CRC on."""
    ts = 2 ** sf / bw
    de = 1 if ts > 0.016 else 0
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (preamble + 4.25) * ts + n * ts


PHY = APP + OVERHEAD
for sf in (7, 9, 10, 12):
    tag("B1", f"SF{sf}: {PHY} B PHY payload, {toa(sf, PHY) * 1000:.0f} ms on air; TRL 2 50 B summary "
              f"{toa(sf, 50 + OVERHEAD) * 1000:.0f} ms")
tag("B2", f"payload limits: EU868 SF12 51 B, US915 SF10 11 B, US915 SF9 53 B, so {APP} B needs SF9 or faster "
          f"in US915; US915 400 ms dwell: SF9 {toa(9, PHY) * 1000:.0f} ms, SF10 with 50 B "
          f"{toa(10, 50 + OVERHEAD) * 1000:.0f} ms")
TX_PER_NIGHT = 3
day_air = TX_PER_NIGHT * toa(12, PHY)
tag("B3", f"worst case 3 transmissions at SF12: {day_air:.1f} s a day, {day_air / 30 * 100:.0f} % of The Things "
          f"Network's 30 s fair use; {toa(12, PHY) / 0.01:.0f} s off-time per uplink under the 1 % duty cycle")

# ================================================================== C. Energy and battery life (R6)
print("\nC. Energy and battery life")
I_SLEEP = 4e-6
I_LISTEN = 12e-3
T_LISTEN = NWIN * (WIN + 1.0)          # 1 s preamp settling per window (3 Hz high-pass, 10 time constants 0.53 s)
RX = (2, 0.2, 5e-3)                     # receive windows per uplink, s each, A
SELF = 0.01                             # per year
CELL_AH, USABLE = 7.7, 0.70
CASES = {"EU868 SF7 +14 dBm": (7, 45e-3), "EU868 SF12 +14 dBm": (12, 45e-3),
         "US915 SF9 +20 dBm": (9, 120e-3), "TRL 2 case, 50 B SF12 +20 dBm": (12, 120e-3)}
life = {}
for name, (sf, itx) in CASES.items():
    pl = 50 + OVERHEAD if "TRL 2" in name else PHY
    q_sleep = I_SLEEP * 24 * 1000
    q_listen = I_LISTEN * T_LISTEN / 3.6
    q_radio = TX_PER_NIGHT * (toa(sf, pl) * itx + RX[0] * RX[1] * RX[2]) / 3.6
    q_self = SELF * CELL_AH * 1000 / 365
    tot = q_sleep + q_listen + q_radio + q_self
    yrs = CELL_AH * USABLE * 1000 / tot / 365
    life[name] = (tot, yrs)
    tag("C1", f"{name}: sleep {q_sleep:.3f} + listening {q_listen:.3f} + radio {q_radio:.3f} + self-discharge "
              f"{q_self:.3f} = {tot:.2f} mAh/day; {yrs:.1f} years on {CELL_AH * USABLE:.2f} Ah usable")
worst = max(v[0] for v in life.values())
tag("C2", f"listening is {I_LISTEN * T_LISTEN / 3.6 / worst * 100:.0f} % of the worst-case day; life taken as "
          f"10 years (cell and seal ageing), energy alone gives {min(v[1] for v in life.values()):.1f} years or more")
I_CELL = 30e-3
V_HI, V_LO = 3.6, 3.1
for name, (sf, itx) in (("EU868 SF12 +14 dBm", (12, 45e-3)), ("US915 SF9 +20 dBm", (9, 120e-3)),
                        ("US915 SF12-length burst +20 dBm", (12, 120e-3))):
    c = max(itx - I_CELL, 0) * toa(sf, PHY) / (V_HI - V_LO)
    tag("C3", f"hybrid capacitor for {name}: ({itx * 1000:.0f} - {I_CELL * 1000:.0f} mA) x {toa(sf, PHY):.2f} s / "
              f"{V_HI - V_LO:.1f} V = {c:.2f} F")

# ================================================================== D. Link budget through the cover (R7)
print("\nD. Radio link from under the cover")
NF, FADE = 6.0, 10.0
SNR = {7: -7.5, 9: -12.5, 10: -15.0, 12: -20.0}
G_NODE, L_NODE, G_GW, L_GW = -3.0, 0.5, 2.0, 2.0
HB, HM = 30.0, 1.0


def sens(sf):
    return -174 + db(125e3) + NF + SNR[sf]


def hata_urban(f, d_km, hb=HB, hm=HM):
    a = (1.1 * LOG10(f) - 0.7) * hm - (1.56 * LOG10(f) - 0.8)
    return 69.55 + 26.16 * LOG10(f) - 13.82 * LOG10(hb) - a + (44.9 - 6.55 * LOG10(hb)) * LOG10(d_km)


def range_km(f, budget_left):
    a = (1.1 * LOG10(f) - 0.7) * HM - (1.56 * LOG10(f) - 0.8)
    l1 = 69.55 + 26.16 * LOG10(f) - 13.82 * LOG10(HB) - a
    return 10 ** ((budget_left - l1) / (44.9 - 6.55 * LOG10(HB)))


RADIO = {"EU868 SF12 +14 dBm": (868, 14.0, 12), "US915 SF9 +20 dBm": (915, 20.0, 9),
         "EU868 SF7 +14 dBm": (868, 14.0, 7)}
COVERS = {"composite cover": 10.0, "iron cover (central)": 20.0, "tight iron cover, flooded": 30.0}
link = {}
for rname, (f, ptx, sf) in RADIO.items():
    budget = ptx + G_NODE - L_NODE + G_GW - L_GW - sens(sf)
    pl1 = hata_urban(f, 1.0)
    tag("D1", f"{rname}: sensitivity {sens(sf):.1f} dBm, link budget {budget:.1f} dB; urban Hata path loss at 1 km "
              f"{pl1:.1f} dB")
    for cname, lc in COVERS.items():
        margin = budget - pl1 - lc - FADE
        rng = range_km(f, budget - lc - FADE)
        link[(rname, cname)] = (margin, rng)
        tag("D2", f"   {cname} {lc:.0f} dB: margin at 1 km after 10 dB fade margin {margin:+.1f} dB; range {rng:.2f} km")
need = {r: link[(r, "iron cover (central)")][0] for r in RADIO}
tag("D3", f"cover loss that still closes 1 km with fade margin: EU868 SF12 "
          f"{20 + need['EU868 SF12 +14 dBm']:.1f} dB, US915 SF9 {20 + need['US915 SF9 +20 dBm']:.1f} dB")
tag("D4", "EU868 limit 14 dBm ERP (16.15 dBm EIRP): the TRL 2 figure of +20 dBm is not permitted in EU868")

# ================================================================== E. Leak noise attenuation (R1, R2)
print("\nE. Leak noise attenuation along the pipe (fluid-dominated axial wave)")
RHO, B_W, C_F = 1000.0, 2.2e9, 1480.0
PIPES = {  # name: (E Pa, mean radius m, wall m, loss factor incl. soil coupling)
    "ductile iron DN150": (170e9, 0.082, 0.006, 0.02),
    "cast iron DN150": (100e9, 0.085, 0.010, 0.02),
    "PVC DN150": (3.3e9, 0.076, 0.0077, 0.065),
    "PE100 DN150 SDR11": (1.2e9, 0.073, 0.0146, 0.10),
}


def wavenumber(f, pipe):
    E, a, h, eta = pipe
    kf = 2 * math.pi * f / C_F
    nu = 2 * B_W * a / (E * h)
    return kf * complex(1 + nu / complex(1, eta)) ** 0.5


def att_db_per_m(f, pipe):
    return 8.686 * abs(wavenumber(f, pipe).imag)


def c_eff(pipe, f=100.0):
    return 2 * math.pi * f / wavenumber(f, pipe).real


for name, pipe in PIPES.items():
    tag("E1", f"{name}: wave speed {c_eff(pipe):.0f} m/s; attenuation "
              + ", ".join(f"{f} Hz {att_db_per_m(f, pipe):.3f}" for f in (20, 100, 500, 1000)) + " dB/m")
for name, pipe in PIPES.items():
    d = 100 if "iron" in name else 30
    tag("E2", f"{name}: loss over {d} m at 50 / 200 / 800 Hz = "
              + " / ".join(f"{att_db_per_m(f, pipe) * d:.1f}" for f in (50, 200, 800)) + " dB")

# ================================================================== F. Sensor sensitivity, noise and bandwidth (R3, R4)
print("\nF. Sensor: sensitivity, self-noise and resonances")
KT = 1.38e-23 * 293
D33 = 300e-12                       # C/N, soft PZT buzzer ceramic (assumed)
m_seis = math.pi * (P["mass_d"] / 2000) ** 2 * (P["mass_h"] / 1000) * 8500
m_trl2 = math.pi * 0.009 ** 2 * 0.005 * 8500
Sq = D33 * m_seis * 9.81            # C per g
Sq2 = D33 * m_trl2 * 9.81
C_P = 8.854e-12 * 1800 * math.pi * 0.010 ** 2 / 0.00023   # 20 mm ceramic, 0.23 mm, er 1800
TAND, C_F_AMP, F_HP = 0.02, 1e-9, 3.0
R_F = 1 / (2 * math.pi * F_HP * C_F_AMP)
EN, F_CORNER = 5e-9, 10.0


def self_noise_g(f, sq=Sq):
    en = EN * math.sqrt(1 + F_CORNER / f)
    q_v = en * (C_P + C_F_AMP)
    q_r = math.sqrt(4 * KT / R_F) / (2 * math.pi * f)
    q_l = math.sqrt(4 * KT * C_P * TAND / (2 * math.pi * f))
    return math.sqrt(q_v ** 2 + q_r ** 2 + q_l ** 2) / sq


tag("F1", f"seismic mass {m_seis * 1000:.1f} g (TRL 2: {m_trl2 * 1000:.1f} g); charge sensitivity {Sq * 1e12:.0f} pC/g "
          f"(TRL 2: {Sq2 * 1e12:.0f} pC/g); piezo {C_P * 1e9:.1f} nF; feedback {C_F_AMP * 1e9:.0f} nF and {R_F / 1e6:.0f} MOhm")
for f in (10, 100, 300, 1000):
    tag("F2", f"self-noise at {f} Hz: {self_noise_g(f) * 1e6:.2f} ug/rtHz (TRL 2 mass: {self_noise_g(f, Sq2) * 1e6:.2f})")
r4 = max(self_noise_g(f) for f in (100, 150, 200, 300, 500, 700, 1000))
tag("F3", f"worst self-noise 100 Hz to 1 kHz {r4 * 1e6:.2f} ug/rtHz against 1 ug/rtHz")
v_out = Sq / C_F_AMP
adc_in = 2e-6 / math.sqrt(20e3) / 100      # 2 uV rms over 20 kHz, referred through 40 dB of gain
tag("F4", f"charge amp output {v_out * 1000:.0f} mV/g; ADC noise referred to input "
          f"{adc_in / v_out * 1e6:.4f} ug/rtHz after 40 dB gain (negligible)")
k_comp = 63e9 * math.pi * 0.010 ** 2 / 0.00023
f_seis = math.sqrt(k_comp / m_seis) / (2 * math.pi)
tag("F5", f"seismic resonance in compression {f_seis / 1000:.0f} kHz (flat to 2 kHz)")
parts = build_parts(P)
m_stack = parts[1].volume * 1e-9 * 2700 + parts[2].volume * 1e-9 * 7500 + m_seis + 0.020   # +potting, preamp
for kc in (5e6, 2e7):
    fm = math.sqrt(kc / m_stack) / (2 * math.pi)
    flat = fm * math.sqrt(1 - 1 / math.sqrt(2))
    tag("F6", f"magnet mount contact stiffness {kc:.0e} N/m, puck and magnet {m_stack * 1000:.0f} g: mounted resonance "
              f"{fm:.0f} Hz, within +3 dB up to {flat:.0f} Hz")

# ================================================================== G. Detection distance (R1, R2)
print("\nG. Detection distance for a 5 L/min leak at 3 bar")
Q, DP, CD = 5 / 60000, 3e5, 0.6
v_jet = math.sqrt(2 * DP / RHO)
A_or = Q / (CD * v_jet)
W_mech = Q * DP
tag("G1", f"jet {v_jet:.1f} m/s, orifice {math.sqrt(4 * A_or / math.pi) * 1000:.1f} mm, mechanical power {W_mech:.1f} W, "
          f"Mach {v_jet / C_F:.4f}")
EFFS = (1e-6, 1e-5, 1e-4)
C_V = 10 ** (-10 / 20)                  # valve and spindle cap coupling, -10 dB (assumed)
VALVE = (170e9, 0.080, 0.010)           # ductile iron valve body: E, radius, wall


def third_octaves():
    fc = [1000 * 2 ** (n / 3) for n in range(-24, 4)]
    return [f for f in fc if F_LO <= f <= F_HI]


def background_g(f):
    return 0.5e-6 * max(1.0, 100 / f)


def detect_range(pipe, eff, noise=True, want_band=False):
    E, a, h, _ = pipe
    S = math.pi * (a - h / 2) ** 2
    w_dir = W_mech * eff / 2
    best, band = 0, None
    for fc in third_octaves():
        c = 2 * math.pi * fc / wavenumber(fc, pipe).real
        p2 = w_dir * RHO * c / S / (F_HI - F_LO)                      # Pa^2/Hz, flat spectrum
        Ev, av, hv = VALVE
        acc = C_V * (2 * math.pi * fc) ** 2 * av ** 2 / (Ev * hv) * math.sqrt(p2) / 9.81   # g/rtHz at the leak
        n = math.hypot(background_g(fc), self_noise_g(fc)) if noise else background_g(fc)
        if acc <= n:
            continue
        d = 20 * LOG10(acc / n) / att_db_per_m(fc, pipe)
        if d > best:
            best, band = d, fc
    return (best, band) if want_band else best


rng = {}
for name, pipe in PIPES.items():
    rs = [detect_range(pipe, e) for e in EFFS]
    rng[name] = rs
    _, fb = detect_range(pipe, 1e-5, want_band=True)
    tag("G2", f"{name}: detection range at acoustic efficiency 1e-6 / 1e-5 / 1e-4 = "
              + " / ".join(f"{r:.0f}" for r in rs) + f" m; limiting band at central efficiency {fb:.0f} Hz")
for name in ("ductile iron DN150", "PVC DN150"):
    pipe = PIPES[name]
    tag("G3", f"{name}, central efficiency, loss factor halved / doubled: "
              f"{detect_range((*pipe[:3], pipe[3] / 2), 1e-5):.0f} / {detect_range((*pipe[:3], pipe[3] * 2), 1e-5):.0f} m")

# ================================================================== H. Clock (R5)
print("\nH. Clock drift")
PPM_25, K_PAR = 20.0, 0.034
for t in (5.0, 10.0, 20.0):
    ppm = PPM_25 + K_PAR * (t - 25) ** 2
    tag("H1", f"chamber {t:.0f} degC: {ppm:.1f} ppm worst case = {ppm * 1e-6 * 30 * 86400:.0f} s in 30 days free running")
ppm_w = PPM_25 + K_PAR * 20 ** 2
tag("H2", f"with a weekly network time correction (LoRaWAN 1.0.3 DeviceTimeReq): {ppm_w * 1e-6 * 7 * 86400:.0f} s worst")

# ================================================================== I. Magnet hold (R9)
print("\nI. Magnet hold on the spindle cap")
G0, IRON = 0.6, 0.7
for rated, label in ((290.0, "32 mm pot magnet (fitted)"), (600.0, "42 mm pot magnet (option)")):
    vals = [rated * IRON / (1 + g / G0) ** 2 for g in (0.1, 0.3, 0.5, 1.0)]
    tag("I1", f"{label}, rated {rated:.0f} N: on iron with a 0.1 / 0.3 / 0.5 / 1.0 mm coating gap "
              + " / ".join(f"{v:.0f}" for v in vals) + " N")
w_hang = (m_stack + 0.055 * 0.5) * 9.81
tag("I2", f"static load on the magnet: puck and 0.5 m of cable {w_hang:.1f} N (sits on top of the cap)")

# ================================================================== J. Chamber survival (R11)
print("\nJ. Chamber survival")
tag("J1", f"1 m submersion: {RHO * 9.81 * 1 / 1000:.1f} kPa on the O-rings and M12 socket")
DENS = {1: 2700, 2: 7500, 4: 1850, 6: 1400, 9: 7900}
masses = {k: parts[k].volume * 1e-9 * DENS[k] for k in DENS}
masses[3] = m_seis + parts[3].volume * 0 + 0.003
masses[1] += 0.012                  # potting in the puck
masses[4] = 0.004
masses[5] = 0.055 * P["cable_len"] / 1000 + 0.030
masses[7] = 0.035
masses[8] = 0.090
masses[10] = 0.040 + 0.030
masses[11] = 0.012
logger_m = masses[6] + masses[7] + masses[8] + masses[11]
buoy = D["logger_vol_l"]
tag("J2", f"logger body {logger_m * 1000:.0f} g against {buoy * 1000:.0f} g of displaced water: "
          f"{'floats' if logger_m < buoy else 'sinks'} when flooded, held by the lanyard ({(buoy - logger_m) * 9.81:.1f} N up)")
air_l = math.pi * (D['tube_id'] / 2000) ** 2 * D['free_len'] / 1000 * 1000
tag("J3", f"free air in the tube about {air_l * 0.6:.2f} L holds {air_l * 0.6 * 17.3:.0f} mg of water at 20 degC saturation; "
          f"a 10 g silica gel pack holds about 2,000 mg")

# ================================================================== K. Size, mass and installation (R10, R12)
print("\nK. Size, mass and installation")
total_m = sum(masses.values())
tag("K1", f"logger {P['tube_od']:.0f} mm diameter, {P['logger_len']:.0f} mm tube, "
          f"{P['logger_len'] + 27:.0f} mm with socket and gland; mass by part: "
          + ", ".join(f"{k} {masses[k] * 1000:.0f} g" for k in sorted(masses)) + f"; total {total_m:.2f} kg")
SLACK = 300.0
plug_depth = abs(D["logger_bot_z"]) + 15.0 + P["m12_len"]
reach = plug_depth + P["cable_len"] - SLACK
tag("K2", f"cable plug {plug_depth / 1000:.2f} m below the street; 2 m cable with 0.3 m slack reaches a spindle cap "
          f"{reach / 1000:.2f} m below the street (chambers up to 1.5 m deep)")
TASKS = {"set out cones and lift cover": 3, "lower puck by pole onto cap": 2, "hang logger and antenna": 1,
         "check join by app or LED": 2, "replace cover and clear site": 2}
tag("K3", "install task estimate " + ", ".join(f"{k} {v}" for k, v in TASKS.items()) + f" min: {sum(TASKS.values())} min")

# ================================================================== L. False alarms (R13)
print("\nL. False alarms from random night-to-night variation")


def qfunc(z):
    return 0.5 * math.erfc(z / math.sqrt(2))


for sigma in (1.0, 2.0, 3.0):
    p1 = qfunc(6.0 / sigma)
    p3 = p1 ** 3
    tag("L1", f"sigma {sigma:.0f} dB, flag at +6 dB for 3 nights: one night {p1:.1e}, three independent nights {p3:.1e}; "
              f"{20 * 30 * p3:.1e} per 20 loggers per month")

# ================================================================== M. Cost (R15)
print("\nM. Parts cost")
rows = list(csv.DictReader(open(ROOT / "bom" / "bom.csv")))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
budget = float(re.search(r"^budget_usd:\s*([\d.]+)", (ROOT / "project.yaml").read_text(), re.M).group(1))
tag("M1", f"{len(rows)} BOM lines, all priced: ${cost:.2f} against budget_usd ${budget:.0f} (margin ${budget - cost:.2f})")

# ================================================================== N. Status
print("\nN. Requirement status")
iron = rng["ductile iron DN150"]
pvc = rng["PVC DN150"]
eu = link[("EU868 SF12 +14 dBm", "iron cover (central)")]
STATUS = [
    ("R1", f"{iron[1]:.0f} m on ductile iron at central efficiency ({iron[0]:.0f} to {iron[2]:.0f} m)", "100 m on iron", "At risk"),
    ("R2", f"{pvc[1]:.0f} m on PVC at central efficiency ({pvc[0]:.0f} to {pvc[2]:.0f} m)", "30 m on plastic", "Not met"),
    ("R3", f"mounted resonance {math.sqrt(5e6 / m_stack) / 2 / math.pi:.0f} to {math.sqrt(2e7 / m_stack) / 2 / math.pi:.0f} Hz", "5 Hz to 2 kHz within 3 dB", "At risk"),
    ("R4", f"{r4 * 1e6:.2f} ug/rtHz", "1 ug/rtHz or less", "Met on paper" if r4 <= 1e-6 else "At risk"),
    ("R5", f"{ppm_w * 1e-6 * 7 * 86400:.0f} s with weekly time sync", "under 60 s a month", "Met on paper"),
    ("R6", f"{min(v[1] for v in life.values()):.1f} years or more on energy", "5 years", "Met on paper"),
    ("R7", f"{eu[0]:+.1f} dB at 1 km under an iron cover (EU868 SF12); range {eu[1]:.2f} km", "90 % delivery at 1 km", "Not met"),
    ("R8", "raw samples processed and deleted on device", "only levels leave", "Met by design"),
    ("R9", f"{290 * IRON / (1 + 0.3 / G0) ** 2:.0f} N at a 0.3 mm coating", "100 N", "At risk"),
    ("R10", f"{sum(TASKS.values())} min task estimate", "10 min, no entry", "Not verifiable at TRL 3"),
    ("R11", "IP68 by design; logger floats on its lanyard", "IP68, -20 to +50 degC", "Met by design"),
    ("R12", f"63 x {P['logger_len'] + 27:.0f} mm, {total_m:.2f} kg", "70 x 300 mm, 1.0 kg", "Met on paper"),
    ("R13", "random variation negligible; site events unknown", "1 per 20 loggers per month", "Not verifiable at TRL 3"),
    ("R14", f"{APP} B LoRaWAN 1.0.3 uplink", "standard LoRaWAN", "Met by design"),
    ("R15", f"${cost:.2f}", f"${budget:.0f}", "Met on paper"),
]
with open(ROOT / "docs" / "04-calcs" / "results.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "value", "target", "status"])
    for r in STATUS:
        w.writerow(r)
        tag("N", " | ".join(r))
