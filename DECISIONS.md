# Engineering Decisions — Pressure Vessel Cost vs. Diameter

The calls that shaped the Vessel Cost Explorer: what was decided, what was rejected, and why.
Sources for each topic are in `SOURCES.md`.

*Built by Joshua Sharpes, EIT, with AI assistance (Claude) for drafting, coding and checks. Scope,
method selection, validation criteria and the corrections below are his.*

## Why this tool exists

In discussing Joshua's ammonia design, a hiring manager experienced in NH₃ plants pointed out that
loop pressure, compression cost and reactor conversion compete with each other, and the original
design hadn't fully weighed that trade-off. This tool was built to answer it. The Haber-Bosch loop
case study is a preset because of that question.

## Method

**Equation-based costing (Seider §16.5).** The Economics project was consulted first. Seider's method
runs thickness → weight → cost with worked examples to check against. Peters and Coulson give only
charts.

**Installation cost itemized, not lumped.** The brief asked for individual installation components.
No vessel-specific breakdown exists in the references, so Seider's exchanger line items (Table 16.10)
are scaled to the vessel bare-module factor. This is disclosed on the page as an assumption, and
installation is priced on the carbon-steel cost (an alloy vessel doesn't need a costlier foundation).

**Current allowable stresses.** ASME II-D (2013) values, each cited to its table line, replace the
older textbook stress tables. The data file self-checks that every material's stresses match the
code basis and never rise with temperature.

**Corrosion allowance reported honestly.** The brief's idea that a thicker wall gives more corrosion
tolerance was corrected after consulting the Materials of Construction project: pressure thickness
and corrosion allowance are additive. Real surplus exists only where minimum thickness governs, the
plate is rounded up, or the vessel is rerated, so the tool reports surplus as nominal minus required
thickness. Cracking mechanisms block the corrosion-allowance route altogether.

## Errors caught in review (Joshua)

**Cost falling with diameter.** At small diameters, cost dropped as diameter rose. Joshua flagged it
as implausible. Cause: the sweep held volume fixed with no bounds, so small diameters implied absurd
lengths (L/D ≈ 99) and wind-load thickness blew up. The default now holds L/D (scale-up), limited
to practical L/D 1.5–8, and cost is verified to rise steadily with diameter. Volume-held remains as a
"find the cheapest L/D" option, where a falling curve is real.

**Converter cost not rising with loop pressure.** Joshua expected converter capital to rise with
pressure because walls thicken. Cause: sizing by residence time at actual conditions made volume
fall as 1/P, cancelling the wall. Sizing changed to catalyst space velocity at standard conditions,
and the wall now thickens from 83 to 197 mm over 60–240 bar.

**Design basis taken from the published version.** Two local ammonia documents disagreed (150 bar vs
90 bar). The published Ammonia Plant Memoir governs; the tool lands at recycle ratio 4.9 against
the Memoir's 5 at 150 bar.

## Scope calls

**Energy cost follows heat integration; reliability left out.** Asked how reliability at high
pressure should enter, the decision was to model the steam drive integrated with the reformer in the
same plant and not to price reliability, which would need data the study doesn't have. The result:
with full integration the cheapest loop pressure is ~145 bar and 120–240 bar falls within ~5 %,
consistent with industrial practice around 150 bar.

**Proof of concept, not overbuilt.** One fixed cost index, handbook-based presets, placeholder
corrosion rates labeled as such, no cladding, vacuum or MDMT checks.

## Validation

- Seider Example 16.12: design pressure 546 psig matches exactly; wall 1.75 vs 1.875 in, explained by
  the newer ASME stress (13.7 vs 13.1 ksi). With 13.1 ksi it matches exactly.
- A unit inconsistency in Seider's platform/ladder example (text in ft, example in inches) was found
  and the equation's own units used.
- Ammonia equilibrium runs a few percent low at high pressure (fugacity neglected), disclosed.
