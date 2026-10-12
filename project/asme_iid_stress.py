"""
ASME II-D (2013, Customary) allowable stress lookup for Section VIII Div. 1.

Data: asme_iid_stress.json (transcribed from the scanned local PDF; page refs inside).
S(T) is linearly interpolated between tabulated temperatures (permitted by II-D).
Returns None above the material's Section VIII-1 maximum temperature (MAWT cap).
"""
import json
import os

# ===========================================================================
# Configuration
# ===========================================================================
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "asme_iid_stress.json")
T_MIN_F = -20.0          # lower bound of the first tabulated column ("-20 to 100")

with open(DATA_FILE, encoding="utf-8") as f:
    MATERIALS = json.load(f)["materials"]


# ===========================================================================
# Lookup
# ===========================================================================
def allowable_stress_ksi(material, T_F, g5=False):
    """Maximum allowable stress S [ksi] at metal temperature T_F [degF]."""
    m = MATERIALS[material]
    table = m["S_ksi_G5"] if (g5 and "S_ksi_G5" in m) else m["S_ksi"]
    temps = sorted(float(t) for t in table)
    vals = [table[str(int(t))] for t in temps]
    if T_F > m["max_T_VIII1_F"]:
        return None
    if T_F <= temps[0]:              # -20 to 100 F column
        return vals[0]
    for (t1, s1), (t2, s2) in zip(zip(temps, vals), zip(temps[1:], vals[1:])):
        if T_F <= t2:
            return s1 + (s2 - s1) * (T_F - t1) / (t2 - t1)
    return None


def max_temperature_for_stress(material, S_required_ksi, g5=False):
    """Highest metal temperature [degF] at which S >= S_required (for MAWT). None if never."""
    m = MATERIALS[material]
    table = m["S_ksi_G5"] if (g5 and "S_ksi_G5" in m) else m["S_ksi"]
    temps = sorted(float(t) for t in table)
    vals = [table[str(int(t))] for t in temps]
    if vals[0] < S_required_ksi:
        return None
    best = temps[0]
    for (t1, s1), (t2, s2) in zip(zip(temps, vals), zip(temps[1:], vals[1:])):
        if s2 >= S_required_ksi:
            best = t2
            continue
        if s1 > s2:                  # crossing inside this interval
            best = t1 + (s1 - S_required_ksi) * (t2 - t1) / (s1 - s2)
        break
    return min(best, m["max_T_VIII1_F"])


# ===========================================================================
# Transcription check
# ===========================================================================
def _verify():
    """
    Checks against the 2013 II-D Mandatory Appendix 1 basis at room temperature:
    S(100F) = min(tensile/3.5, 2/3 yield), rounded to 0.1 ksi. Also checks that
    S is non-increasing with T, and that tables stop at the VIII-1 max temperature.
    """
    ok = True
    for name, m in MATERIALS.items():
        expected = round(min(m["tensile_ksi"] / 3.5, 2.0 / 3.0 * m["yield_ksi"]), 1)
        for key in ("S_ksi", "S_ksi_G5"):
            if key not in m:
                continue
            t = m[key]
            temps = sorted(int(k) for k in t)
            vals = [t[str(k)] for k in temps]
            if abs(vals[0] - expected) > 0.05:
                print(f"FAIL {name} {key}: S(100F)={vals[0]} expected {expected}")
                ok = False
            if any(b > a for a, b in zip(vals, vals[1:])):
                print(f"FAIL {name} {key}: S increases with T")
                ok = False
            if temps[-1] != m["max_T_VIII1_F"]:
                print(f"FAIL {name} {key}: last T {temps[-1]} != VIII-1 limit {m['max_T_VIII1_F']}")
                ok = False
    return ok


if __name__ == "__main__":
    print("Transcription check:", "PASS" if _verify() else "FAIL")
    print(f"\n{'Material':<14}{'UNS':<8}{'S@100F':>8}{'S@500F':>8}{'S@700F':>8}{'Tmax F':>8}")
    for name, m in MATERIALS.items():
        s = [allowable_stress_ksi(name, T) for T in (100, 500, 700)]
        fmt = [f"{x:8.1f}" if x is not None else f"{'NP':>8}" for x in s]
        print(f"{name:<14}{m['uns']:<8}{''.join(fmt)}{m['max_T_VIII1_F']:8d}")
    print("\nExample: SA-516-70 MAWT for S >= 15 ksi:",
          round(max_temperature_for_stress("SA-516-70", 15.0)), "F")
