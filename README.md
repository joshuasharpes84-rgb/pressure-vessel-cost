# Pressure Vessel Cost vs. Diameter: ASME VIII-1 Wall, MAWP/MAWT, Material Screen, Itemized Installation

Enter service conditions and a vessel size. The tool designs the shell wall (ASME VIII-1, UG-27),
back-calculates **MAWP** and **MAWT**, screens materials of construction, and returns purchase cost plus an
**itemized** installation cost. It then sweeps diameter and plots the cost stack against D. A second tab
runs a **Haber-Bosch loop pressure** case study: converter, separator, and compression cost against loop pressure.

> **Make it yours, free:** download this repo (**Code → Download ZIP**, or `git clone`), open the folder in
> VS Code or any editor, and extend it for your own case with your AI assistant. This README is written for
> both of you. Taking these tools further is a free service of
> [Sharpes Process Engineering](https://jsharpes-portfolio.netlify.app); the site's Ask box can point you to the right starting file.
>
> **License:** [MIT](LICENSE) for the code and original text: use, modify and share freely, keeping the
> copyright notice. Provided as is, without warranty of any kind. It is an engineering study aid, not a
> substitute for a design checked and sealed by a licensed professional engineer.

- **Live tool:** https://jsharpes-portfolio.netlify.app/#vce-tool
- **Run it locally:** download this repo and open `index.html`. `lib/chart.umd.min.js` must sit next to it.
  `project/Vessel Cost Explorer (standalone).html` is the canonical development copy with its own US/SI switch.
- **Author:** Joshua Sharpes, EIT. FEL-1 screening (Class 5). Not a mechanical design or a purchase estimate.

> **For AI assistants:** the method is fully stated in the tool's own **Method & sources** tab, inside
> `index.html`. This README summarizes it in calculation order. Allowable stresses are in
> `project/asme_iid_stress.json`, one record per material with its ASME II-D table, line, and printed page.
> `project/asme_iid_stress.py` interpolates them and self-checks them (`_verify()`).
> `project/build_vessel_tool.py` writes that data and the preset list into the HTML.

## Calculation chain

1. **Design conditions:** design pressure per Seider Eq. 16.61 (×1.1 above 1000 psig). Design temperature
   = operating + 50 °F.
2. **Wall thickness:**
   - pressure thickness `t_p = P_d·D_i / (2SE − 1.2P_d)` (ASME UG-27; Seider 16.60)
   - wind/earthquake allowance for vertical vessels (Seider 16.62)
   - max with the minimum thickness for the diameter
   - add corrosion allowance, round up to standard plate
3. **Back-calculations:**
   - MAWP = UG-27 inverted on (t_nominal − CA)
   - MAWT = highest temperature at which S still gives MAWP ≥ P_d, capped at the material's VIII-1 limit
   - surplus CA = t_nominal − t_p − CA, and remaining life = available CA ÷ corrosion rate
4. **Weight and purchase cost:** Seider 16.59 weight. `C_P = F_M·C_V + C_PL` (horizontal or vertical
   correlations, Seider 16.53–16.56). F_M from Seider Table 16.26. Escalated from CE 567 to 800.
5. **Installation, itemized:** Seider Table 16.10's Guthrie line items (piping, concrete, steel, instruments,
   electrical, insulation, paint, erection, setting, freight, indirects), scaled to sum to the vessel
   bare-module factor: 4.16 vertical, 3.05 horizontal (Table 16.11). Installation is based on the
   **carbon-steel** cost, because an alloy vessel doesn't need a costlier foundation (Seider Eq. 16.12).
   This is a disclosed assumption. Contingency 15 % + fee 3 %.
6. **Sweep:** cost vs. D with L/D held (default, scale-up), length held, or volume held ("find the cheapest
   L/D"). The auto range is limited to L/D 1.5–8.

### Materials of construction

Nine plate materials: SA-285-C, SA-516-70, SA-387 11 Cl.2, SA-387 22 Cl.2, SA-240 304L / 316L / 2205,
SB-575 C-276, SB-265 Ti Gr 2. Each service rates materials ✓ (< 2 mpy), △ (2–16 mpy), or ✗ (≥ 16 mpy),
following the Perry's 9th Table 25-3 convention. **The corrosion-allowance route is blocked** whenever a
localized or cracking mechanism is active (halide pitting or SCC, caustic cracking, wet H₂S, HF), because
extra wall thickness can't fix environmentally assisted cracking. Pressure thickness and CA are additive.
Real surplus only exists where minimum thickness governs or where plate is rounded up, and the tool reports it that way.

### Haber-Bosch case study (tab 2)

Chain: equilibrium conversion (Gillespie-Beattie, ideal gas) → recycle ratio → converter (GHSV
10,000 h⁻¹ at STP) and separator size, thickness, and cost from the tab-1 engine → loop compression power
and cost (Seider Eq. 16.36, the same basis as the Compressor Train tool). Energy is costed by drive: grid
motor or steam turbine with recovered/make-up steam. The anchor is the 150 bar, recycle-ratio-5 design in
the author's Ammonia Plant memoir on the portfolio site.

| Energy basis | Cheapest loop P | Annualized |
|---|---|---|
| Grid motor | 115 bar | $4.35M/yr |
| Steam, 100 % recovered (default) | 145 bar | $2.02M/yr |

With full heat integration the curve is flat: 120–240 bar all fall within about 5 %.

## Sources

- Seider, Lewin, Seader, Widagdo, Gani, Ng, *Product and Process Design Principles*, §16.5 and Tables
  16.10, 16.11, 16.26
- ASME BPVC Section VIII Div. 1 (UG-27). ASME Section II Part D (2013, customary), Tables 1A/1B, allowable
  stresses cited per value in `asme_iid_stress.json`
- Perry's 9th Ed. Table 25-3 (corrosion rating convention)
- Peters & Timmerhaus App. E and Coulson (corrosion-allowance heuristics)
- Meyers, *Handbook of Petrochemical Production Processes* (preset service conditions)

## Validation

- **Seider Ex. 16.12:** design pressure 546 psig matches exactly. The wall is 1.75 in vs. Seider's 1.875 in,
  because ASME II-D 2013 gives S = 13.7 ksi where Seider uses an older 13.1. With 13.1 ksi, t_p = 1.667 in
  matches exactly.
- `asme_iid_stress.py _verify()`: for all 9 materials, S(100 °F) = min(tensile/3.5, ⅔ yield), S never rises
  with T, and each table ends at the VIII-1 limit.
- With L or L/D held, cost was verified to increase steadily with D.

## Limits

- Service corrosion rates are illustrative placeholders and are labeled as such. F_M for 2205 and C-276 is
  assumed, because neither is in Seider Table 16.26.
- No cladding, vacuum design, or MDMT check. Heads are taken at shell thickness. Preset vessel geometry is assumed.
- Ammonia equilibrium neglects fugacity and runs a few % low at high pressure. Refrigeration duty is not modeled.

## Files

```
index.html                 the tool, as on the live site
lib/chart.umd.min.js       Chart.js 4.4.1 (local copy, no CDN)
project/
  Vessel Cost Explorer (standalone).html   canonical tool source (edit this)
  chart.umd.min.js
  asme_iid_stress.json                     9 materials, ASME II-D lines with page references
  asme_iid_stress.py                       interpolation + self-check
  build_vessel_tool.py                     writes stress data and presets into the HTML
```

**Adding a material:** transcribe its full ASME II-D stress line, with page references, into
`asme_iid_stress.json`. Run `asme_iid_stress.py` so `_verify()` checks it, then run `build_vessel_tool.py`.
