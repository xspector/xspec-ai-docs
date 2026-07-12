---
id: chandra-blazar-curvature-001
title: Blazar curvature — when the F-test IS valid, and how chi fakes curvature
status: core
context:
  mission: Chandra
  instrument: ACIS-S
  counts_regime: high
  grouped: false
  background: none
  source_type: agn
  source_class: "blazar, log-parabola X-ray continuum (synchrotron curvature)"
  model_family: [logpar]
  statistic: cstat
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: cstat
    rejected: chi
    rationale: >
      A trap within the trap: on ~20000-count power-law data, chi with standard
      weighting does not merely mis-size errors -- it INVENTS curvature. Adding a
      log-parabola beta to curvature-free data improves chi by a median
      delta-chi-square of 17 (beta ~ 0.2 out of nothing), while cstat gives the
      correct median delta of 0.46. chi would manufacture the very curvature under
      test; cstat does not.
  - point: band
    choice: "0.5-8 keV, ignore bad"
    rationale: "Chandra ACIS-S band for the blazar continuum."
  - point: add_component
    choice: "test the curvature with the F-test / likelihood-ratio -- here it IS valid"
    rationale: >
      Unlike a searched line, the log-parabola curvature `beta` is an INTERIOR
      parameter (it can be positive or negative) and is identified under the null
      (a power law is beta=0, with the slope still meaningful). So the regularity
      conditions hold: under a power-law null the delta-cstat for adding beta
      follows chi-square_1 almost exactly (median 0.46, 95th 3.48, 99th 5.80;
      P>6.63 = 1.0%), and the F-test p-value is correct. A genuine curvature
      (beta=0.4) is detected at delta-cstat = 73.
  - point: stop
    choice: "trust the F-test here; contrast the searched-line case"
    rationale: >
      This is the `not_when` of ftest-invalid-for-line-significance: the F-test
      fails for bounded, searched lines (Ginga cyclotron case: 9% false alarms at
      the 1% bar) but is well-calibrated for interior nested continuum parameters
      like curvature (1% here). The discriminator is boundary + identifiability,
      not "lines vs continua" per se.
outcome:
  verdict: bench-validated
  result:
    null_delta_cstat_matches_chi2_1: {median: 0.46, p95: 3.48, p99: 5.80}
    false_alarm_at_chi2_1_1pct_threshold: {value_pct: 1.0, nominal_pct: 1.0, verdict: "calibrated -- F-test valid"}
    curved_truth_beta_0p4_detection_delta_cstat: 73.0
    chi_induced_spurious_curvature_median_delta: 17.0
lessons: [ftest-invalid-for-line-significance]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    Null continuum: logpar [alpha=1.8, beta=0, pivotE=1, norm=1] (= a power law),
    response/arf aciss_aimpt_cy15, band 0.5-8 keV ignore bad, ~20000 counts
    (exposure ~30 s). 200 curvature-free fakeit realisations (seeds 9000+i); each
    fit with beta frozen at 0 and with beta free (interior, -1..1). With cstat the
    null delta-cstat matches chi-square_1 (median 0.46, 95th 3.48, 99th 5.80;
    P>3.84 = 5.0%, P>6.63 = 1.0%). A curved truth (beta=0.4) gives delta-cstat=73.
    With chi (standard weighting) the same null gives a median delta-chi-square of
    ~17 -- spurious curvature from the weighting bias.
---

# Blazar curvature

## The data

A blazar with a curved X-ray continuum — the log-parabola shape a synchrotron peak
imprints — at ~20 000 counts on Chandra ACIS-S. The question is whether the
curvature is real, and it is a good setting to see two things at once: a statistic
trap, and the case where the F-test is actually allowed.

## Decision 1 — statistic, and a trap within the trap

`cstat`, and here `chi` fails in a way that is specific and dangerous. On
curvature-free (pure power-law) data, adding a log-parabola `beta` and fitting with
`chi` improves the fit by a **median delta-chi-square of 17** — the fit finds a
curvature of `beta ~ 0.2` in data that have none. `cstat` on the same data gives
the correct median delta of **0.46**. The mechanism is `chi`'s standard weighting
(sqrt of the data): it biases the fit in a way a smooth curvature term absorbs, so
`chi` *manufactures* the very curvature you are trying to measure. Use `cstat`
before you even ask whether the curvature is significant.

## Decision 2 — band

`0.5-8 keV`, the ACIS-S continuum band.

## Decision 3 — the F-test, and why it works here

With `cstat`, ask whether `beta` is significant. This is the mirror image of the
cyclotron-line case [`ftest-invalid-for-line-significance`](../lessons/ftest-invalid-for-line-significance.md):
there the F-test badly over-claimed, here it is exactly right. The difference is
the parameter. Curvature `beta` is *interior* — it can be positive or negative, so
`beta = 0` is not a boundary — and it is *identified* under the null, because a
power law is simply `beta = 0` with the slope still meaningful. The regularity
conditions the F-test needs are met, and the numbers confirm it: under a power-law
null the `delta-cstat` for adding `beta` follows chi-square_1 almost perfectly
(median 0.46 vs 0.45, 99th percentile 5.80 vs 6.63, and a **1.0%** false-alarm rate
at the nominal 1% threshold). A genuinely curved blazar (`beta = 0.4`) is detected
at `delta-cstat = 73` — about 8.5 sigma, correctly.

## Decision 4 — the discriminator

The lesson is not "trust the F-test for continua, distrust it for lines". It is:
**is the extra parameter on a boundary, and is it identified under the null?**
Curvature passes both tests; a searched line (bounded depth, free energy) fails
both. When in doubt, do what the line case forced — simulate — but for an interior,
identified nested parameter the F-test is sound.

## Result

The curvature test is well-calibrated: `beta` is significant only when
`delta-cstat` clears the chi-square_1 threshold, which under the null it does at
exactly the nominal rate. The blazar's `beta = 0.4` curvature is a real, ~8.5-sigma
detection.

## What a careless analysis would have concluded

Two ways to go wrong, both avoided here. Fit with `chi` and "discover" curvature in
a source that has none — a `beta ~ 0.2` artifact of the weighting, not the
spectrum. Or, having internalised the cyclotron-line lesson too broadly, distrust a
real curvature and simulate needlessly. The right reading is specific: switch to
`cstat` so the statistic does not invent curvature, then trust the F-test because
this parameter, unlike a line, satisfies its assumptions.
