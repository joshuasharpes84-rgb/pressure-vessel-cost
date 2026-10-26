# Sources — Pressure Vessel Cost vs. Diameter

Where each type of information in the Vessel Cost Explorer (vessel tab, Haber-Bosch loop case study,
method tab) comes from. Topic-level, not number-by-number: the aim is to show nothing was invented,
and to point a reader to the right book and section if they want to dig.

**Tiers**
- **Library** — reference textbook in `Downloads\ChemE\Textbooks (Level 1)\` (used across projects)
- **Project PDF** — standard or excerpt held in this folder
- **Web** — public page, URL given
- **Print only** — book cited from a paper copy; no digital copy for page lookup
- **Own work** — derived, fitted or chosen in this project; the basis is stated

Copyrighted PDFs are cited here but never published.

| Topic | Source | Tier | Location |
|---|---|---|---|
| Design pressure and temperature, wall thickness (UG-27), wind/earthquake allowance, minimum thickness, vessel weight | Seider, Lewin, Seader, Widagdo, *Product and Process Design Principles*, §16.5, Eq. 16.59–16.62 | Library | `Textbooks (Level 1)\Process & Plant Design\Product and Process Design Principles (Sieder, Lewin) ...pdf` |
| Purchase cost (horizontal/vertical correlations, platforms and ladders), material factors F_M | Seider Eq. 16.53–16.56, Table 16.26 | Library | as above |
| Itemized installation cost (piping, concrete, steel, instruments, electrical, insulation, paint, erection, freight, indirects) | Seider Table 16.10 line items (Guthrie), scaled to the vessel bare-module factor 4.16 vertical / 3.05 horizontal (Table 16.11) | Library + Own work | as above; scaling disclosed on the page |
| Installation priced on carbon-steel cost | Seider Eq. 16.12 | Library | as above |
| Contingency 15 % + fee 3 % | Seider basis | Library | as above |
| Validation case | Seider Example 16.12 | Library | as above |
| Allowable stress vs temperature, 9 plate materials (tensile ÷ 3.5 basis), VIII-1 temperature limits | ASME BPVC Section II Part D (2013, customary), Tables 1A/1B, cited per value | Project PDF | `Asme-Section-II-materials-part-d-properties-customary-2013-...pdf`; transcribed in `asme_iid_stress.json` |
| ASME pressure-vessel background, heads | Peters & Timmerhaus Ch. 12; Coulson & Richardson Vol. 6 Ch. 13; Perry's 9th Sec. 10 | Library | `Textbooks (Level 1)\Process & Plant Design\` |
| Corrosion rating convention (✓ < 2 mpy, △ 2–16, ✗ ≥ 16) | Perry's 9th, Table 25-3 | Library | `Textbooks (Level 1)\Handbooks & Quick Reference\Perry's 9th Edition.pdf` |
| Corrosion allowance heuristics (3.8 / 9 mm; 2 mm minimum for CS) | Peters & Timmerhaus App. E; Coulson | Library | `Textbooks (Level 1)\Process & Plant Design\` |
| Material screening method (per-mechanism, UNS naming, cracking mechanisms block the CA route) | Materials of Construction project methodology | Own work | `ChemE\Plant Resources\Materials of Construction\` |
| Cladding economics (~25 mm), alloy premium narrowing with thickness | Perry's; Coulson p. 310 | Library | as above |
| Preset service conditions (oxo hydroformylation, Lurgi methanol) | Meyers, *Handbook of Petrochemical Production Processes*, Ch. 7.1, 8.1 | Library | `Textbooks (Level 1)\Process-Specific References\Handbook for Petrochemical Production Processes.pdf` |
| Haber-Bosch design basis (150 bar, recycle ratio 5, V-401) | Joshua's Ammonia Plant Memoir, as published on the portfolio site | Own work | `ChemE\Design\Ammonia Process\` |
| NH₃ equilibrium | Gillespie–Beattie correlation (ideal gas; fugacity neglected, disclosed) | Own work | tool Method tab |
| Compressor cost in the loop study | Seider Eq. 16.36 (same basis as the Compressor Train tool) | Library | Seider Ch. 16.5 |
| Make-up steam price $17.60/t (450 psig) | Seider Table 17.1 | Library | Seider Ch. 17 |
| Turbine steam rate 3.45 kg/kWh (105 bar / 510 °C to 0.1 bar, 80 % isentropic) | IAPWS-95 via `thermo` | Own work | computed |
| Cost index CE 567 → 800 | Single fixed escalation (proof of concept) | Own work | stated on page |
| Service corrosion rates; F_M for 2205 and C-276 | Illustrative placeholders / assumed (not in Seider Table 16.26) | Own work | labeled on page |
| Cr-Mo converter shell for hot hydrogen service | Nelson curve / API 941 (inference; standard not held) | Own work | — |
