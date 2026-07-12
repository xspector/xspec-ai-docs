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
status: candidate
validation: null
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

**Validation (PLAN-C L3):** a `bench/lessons/` harness would fakeit data from a
two-component (or atmosphere) truth, fit the deliberately-wrong one-component
model, and assert that `assess_fit` raises both `pegged_limit` and
`systematic_residual` — i.e. that the signal fires when the model is known to be
wrong and stays quiet when it is right. Not yet built, so `status: candidate`.
