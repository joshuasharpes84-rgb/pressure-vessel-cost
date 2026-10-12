"""
Syncs data into 'Vessel Cost Explorer.html' (the page is its own source).

Rewrites, in place, the blocks between /*BEGIN STRESS_DATA*/.../*END STRESS_DATA*/
(from asme_iid_stress.json) and /*BEGIN PRESETS*/.../*END PRESETS*/ (from PRESETS
below). Everything else in the HTML is edited directly. The page is valid on its
own at all times; run this only after changing the JSON or the presets.
"""
import json
import os
import re

# ===========================================================================
# Paths
# ===========================================================================
HERE = os.path.dirname(os.path.abspath(__file__))
STRESS = os.path.join(HERE, "asme_iid_stress.json")
OUTPUT = os.path.join(HERE, "Vessel Cost Explorer.html")

BARG_TO_PSIG = 14.5038
C_TO_F = lambda c: c * 1.8 + 32

# ===========================================================================
# Presets
# Conditions: Meyers, Handbook for Petrochemical Production Processes
# (Textbooks (Level 1)\Process-Specific References), or the Ammonia Process project.
# Geometry is illustrative unless stated; the handbook gives no vessel dimensions.
# ===========================================================================
PRESETS = [
    {
        "name": "JM Oxo alcohols - hydroformylation reactor (245 barg)",
        "note": "Meyers Ch. 8.1 (PDF p.102, printed 8.4): olefin + 50/50 CO/H2 at 245 bar(g), "
                "95-180 C. Upper T used. Geometry assumed.",
        "set": {"orient": "V", "D": 5, "L": 30, 
                "P": round(245 * BARG_TO_PSIG), "T": round(C_TO_F(180)),
                "service": "hydrogen", "mat": "auto", "life": 20, "rateOv": "", "credit": True},
    },
    {
        "name": "Lurgi MegaMethanol - gas-cooled reactor shell (syngas)",
        "note": "Meyers Ch. 7.1 (PDF p.97, printed 7.12-7.13): GCR shell holds catalyst, "
                "WCR inlet ~240 C, GCR outlet ~220 C. Loop pressure NOT stated in the handbook: "
                "80 bar assumed (typical low-pressure methanol loop). Geometry assumed.",
        "set": {"orient": "V", "D": 14, "L": 35, 
                "P": round(80 * BARG_TO_PSIG), "T": round(C_TO_F(250)),
                "service": "hydrogen", "mat": "auto", "life": 20, "rateOv": "", "credit": True},
    },
    {
        "name": "Lurgi MegaMethanol - water-cooled reactor steam side",
        "note": "Meyers Ch. 7.1 (PDF p.98, printed 7.14): reactor raises 50-60 bar steam; shell side "
                "is boiling BFW. 60 bar, 275 C (saturation) used. Geometry assumed.",
        "set": {"orient": "V", "D": 14, "L": 35, 
                "P": round(60 * BARG_TO_PSIG), "T": round(C_TO_F(275)),
                "service": "clean", "mat": "auto", "life": 20, "rateOv": "", "credit": True},
    },
    {
        "name": "Ammonia Process - V-401 knock-out (wet CO2 syngas)",
        "note": "Design\\Ammonia Process memoir: V-401 1.8 m ID, 27 bar, L/D 3.5 (Souders-Brown K 0.107). "
                "Service assumed wet CO2 condensate (upstream of CO2 removal); 40 C assumed.",
        "set": {"orient": "V", "D": 5.9, "L": 20.7, 
                "P": round(27 * BARG_TO_PSIG), "T": round(C_TO_F(40)),
                "service": "wetco2", "mat": "auto", "life": 20, "rateOv": "", "credit": True},
    },
    {
        "name": "Generic - horizontal brine drum (chlorides, low P)",
        "note": "Illustrative low-pressure case where minimum thickness governs: shows the "
                "min-thickness corrosion-credit toggle and the CS-vs-alloy crossover.",
        "set": {"orient": "H", "D": 8, "L": 24, 
                "P": 50, "T": 120, "service": "chloride", "mat": "auto", "life": 20,
                "rateOv": "", "credit": True},
    },
]


def _sync(html, name, payload):
    pat = re.compile(r"(/\*BEGIN " + name + r"\*/).*?(/\*END " + name + r"\*/)", re.S)
    if not pat.search(html):
        raise RuntimeError(f"Marker block {name} missing from {OUTPUT}")
    return pat.sub(lambda m: m.group(1) + payload + m.group(2), html, count=1)


def build():
    with open(OUTPUT, encoding="utf-8") as f:
        html = f.read()
    with open(STRESS, encoding="utf-8") as f:
        stress = json.load(f)
    html = _sync(html, "STRESS_DATA", json.dumps(stress, ensure_ascii=False))
    html = _sync(html, "PRESETS", json.dumps(PRESETS, ensure_ascii=False, indent=1))
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Synced data into {OUTPUT} ({len(html)/1024:.0f} kB)")


if __name__ == "__main__":
    build()
