---
id: ftest-invalid-for-line-significance
one_line: "The F-test (and treating delta-chi-square as chi-square) is not valid for the significance of an added emission or absorption line; calibrate it with Monte-Carlo simulations instead."
rule: >
  Testing whether a line improves a fit puts the line's strength on the boundary
  of parameter space (a depth or flux can only be >= 0) and leaves the line's
  energy and width undefined under the null (they mean nothing when the strength
  is zero). Both violate the regularity conditions behind the F-test and the
  delta-chi-square ~ chi-square_k asymptotics (Protassov et al. 2002), and a
  searched line energy adds a look-elsewhere penalty on top. The net effect is
  that the F-test / naive delta-chi-square OVER-states the significance, often
  severalfold. Calibrate the real significance by Monte-Carlo: simulate many
  datasets from the best-fit NO-line model, fit both models to each with the line
  searched exactly as in the data, and read the p-value off the empirical
  delta-chi-square distribution.
applies_when: >
  assessing the significance of adding a narrow spectral feature whose strength is
  bounded at zero and whose energy/width are free or searched -- a cyclotron line
  (CRSF), an Fe K or other emission line, a candidate absorption feature -- from a
  delta-chi-square between a no-line and a with-line fit.
not_when: >
  comparing two nested CONTINUUM models where the extra parameter is not on a
  boundary and is meaningful under the null (adding a high-energy cutoff, freeing
  an abundance, power law vs a curved log-parabola) -- there the F-test is
  admissible. A line at a single FIXED, pre-specified energy with a two-sided
  normalisation is a milder case (a half-chi-square-1 boundary effect only), still
  best checked but less badly biased than a searched line.
status: validated
validation: bench/lessons/ftest-invalid-for-line-significance.py
evidence_cases: [ginga-cyclotron-ftest-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-12"
  reviewed_by: [kaa]
---

# The F-test does not measure line significance

A cyclotron line (CRSF) in an accreting pulsar, or any candidate line, is usually
"detected" by adding a `gabs`/`gaussian`, noting the drop in chi-square, and
converting it to a significance -- via the F-test, or the even cruder
`sigma = sqrt(delta-chi-square)`. That conversion is not valid. The line's depth
can only be positive (a boundary), and its energy and width have no meaning when
the depth is zero (unidentified nuisance parameters). The asymptotic theory the
F-test relies on assumes neither is true, so its p-value is simply the wrong
number -- and because the line hunts for the largest noise excursion in the band,
it is wrong in the anti-conservative direction.

`ginga-cyclotron-ftest-001` calibrates it directly. Under a pure `cutoffpl`
continuum with **no line**, adding a searched `gabs` (energy and width free, depth
>= 0) reaches `delta-chi-square > 6.63` -- the chi-square_1 "p = 0.01, 2.6 sigma"
threshold -- in **9.4%** of line-free simulations, not 1%. The empirical 99th
percentile of the null `delta-chi-square` is **11.5**, not 6.6. So a line reported
at "2.6 sigma" from the naive threshold is really below 2 sigma, and the honest
bar is nearly twice as high. The gap widens with a finer, wider-band instrument
(NuSTAR, XRISM) where the searched line has far more noise to find.

## The fix

Simulate many spectra from the best-fit no-line model (`fakeit`), fit each with
the same continuum and with the searched line, and build the empirical
`delta-chi-square` distribution. The fraction exceeding the observed value is the
real p-value. This is the only defensible significance for a searched line -- see
also [[systematics-dominate-above-1e5-counts]] for why, at high counts, such a
feature can be real *and* small.

## `not_when`

The F-test is fine where its assumptions hold: nested continuum models with an
interior, identified extra parameter -- a spectral break, a cutoff, a freed
abundance. The failure is specific to bounded, searched line components.

## Promotion status

`validated`. The harness `bench/lessons/ftest-invalid-for-line-significance.py`
runs 150 line-free `cutoffpl` simulations, fits each with a searched `gabs`, and
asserts the false-alarm rate at the naive chi-square_1 1% threshold is several
times too high (~8%) while the null distribution stays sane (median ~2). Both
conditions hold.

Not yet eligible for *promotion* into a guide/skill: that needs
`len(evidence_cases) >= 3` (PLAN-C §4), and there is one so far. The blazar
curvature case (the F-test's admissible `not_when`) would add a contrasting
evidence case.
