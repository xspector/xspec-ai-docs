---
id: peg-at-limit-means-wrong-model
one_line: "A parameter pegged at a limit plus correlated residuals means the model is structurally wrong, not just badly initialised."
rule: >
  When a free parameter sits at its soft limit AND the residuals are correlated
  (runs-test failure), the fit is telling you the model cannot describe the data
  — the minimiser is pushing a parameter to an extreme to compensate for missing
  physics. The fix is a different/additional component, not a new starting value
  or a widened limit. Widening the limit or re-seeding only hides the symptom.
applies_when: >
  a thawed parameter is pegged at soft-min or soft-max (assess_fit `pegged_limit`)
  AND a systematic-residual flag is present (assess_fit `systematic_residual`).
not_when: >
  the peg is physical and the residuals are clean (e.g. a genuinely unconstrained
  normalisation, or an abundance truly at solar) — then the limit is informative,
  not a defect; OR the parameter is pegged only because its start value was
  absurd and a re-fit from a sensible value frees it.
status: validated
validation: bench/lessons/peg-at-limit-means-wrong-model.py
evidence_cases: [nicer-lowcount-thermal-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-02"
  reviewed_by: [kaa]
---

# Pegged limit + correlated residuals = wrong model

The two flags together are the signal; either alone is weaker. A pegged
parameter with *clean* residuals can be a genuine physical bound. Correlated
residuals with *no* peg point to a missing component but not necessarily a
mis-specified one. Both at once is the classic "the minimiser is contorting one
parameter to paper over missing physics" pattern — seen in
[`nicer-lowcount-thermal-001`](../cases/nicer-lowcount-thermal-001.md) where a
blackbody's temperature pegged high while an atmosphere model was needed.

**Validation:** `bench/lessons/peg-at-limit-means-wrong-model.py` fakes an
absorption-free power law plus a strong broad emission line, then fits
`tbabs*powerlaw` (the wrong model): absorption cannot add a line, so `nH` is
driven to its floor (pegged at soft min) while the missing line leaves strongly
correlated residuals — `assess_fit` raises **both** `pegged_limit` and
`systematic_residual`. The correct model (`powerlaw + gaussian`), initialised at
the truth, raises **neither**. Because the signal fires when the model is wrong
*and* stays quiet when it is right, the lesson is `validated`. (The construction
differs from the case's blackbody-vs-atmosphere story but exercises the same
signal.)
