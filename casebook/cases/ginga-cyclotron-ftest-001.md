---
id: ginga-cyclotron-ftest-001
title: A cyclotron line that isn't there — why the F-test over-claims, and Monte-Carlo fixes it
status: core
context:
  mission: Ginga
  instrument: LAC
  counts_regime: high
  grouped: false
  background: none
  source_type: xrb
  source_class: "accreting X-ray pulsar, candidate cyclotron line (CRSF)"
  model_family: [cutoffpl, gabs]
  statistic: chi
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: chi
    rationale: >
      ~19000 counts over 36 Ginga LAC channels is ~520 counts/bin -- richly
      Gaussian, so chi is valid and standard for this hard-band continuum.
  - point: band
    choice: "2-28 keV, ignore bad"
    rationale: "Ginga LAC calibrated hard band, where accreting-pulsar cyclotron lines fall."
  - point: add_component
    choice: "judge the candidate line by Monte-Carlo, not the F-test or sqrt(delta-chi-square)"
    rejected: "F-test / delta-chi-square -> sigma"
    trigger: >
      The candidate gabs has a bounded depth (>= 0) and an energy/width that are
      free and meaningless under the no-line null -- the F-test's assumptions fail
      (Protassov et al. 2002). Calibrated against 300 line-free simulations, a
      searched line reaches delta-chi-square > 6.63 (the chi2_1 "2.6 sigma"
      threshold) in 9.4% of cases, not 1%; the true 99th percentile is 11.5.
  - point: stop
    choice: "do not claim the CRSF unless it beats the Monte-Carlo threshold"
    rationale: >
      A delta-chi-square that the F-test calls 2.6 sigma is really below 2 sigma
      here. Report the line only if it exceeds the simulated null distribution --
      and note the effect worsens on finer, wider-band instruments (NuSTAR, XRISM).
outcome:
  verdict: bench-validated
  result:
    null_delta_chi2_99th_percentile: 11.5
    naive_chi2_1_threshold: 6.63
    false_alarm_at_naive_threshold_pct: 9.4
    nominal_false_alarm_pct: 1.0
    method: "Monte-Carlo, 300 line-free simulations (not the F-test)"
lessons: [ftest-invalid-for-line-significance]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    Null continuum: cutoffpl [PhoIndex=1.0, HighECut=15 keV, norm=1.0], response
    ginga_lac.rsp, band 2-28 keV ignore bad, ~18800 counts over 36 channels
    (exposure ~18400 s). 300 line-free fakeit realisations (seeds 5000+i); each fit
    with cutoffpl and with cutoffpl*gabs (LineE free 5-28 keV, Sigma free 0.5-8
    keV, Strength >= 0); delta-chi-square = chi2(cont) - chi2(cont+line). Null
    distribution: median 2.2, 95th 8.65, 99th 11.45, max 13.0. P(delta-chi2 > 6.63)
    = 9.4% vs the nominal 1%.
---

# A cyclotron line that isn't there

## The data

An accreting X-ray pulsar observed with Ginga LAC — a smooth `cutoffpl` continuum,
~19 000 counts across the hard band, the setting where cyclotron resonant
scattering features (CRSFs) are hunted. The question is not how to fit the
continuum but how to decide whether a dip in the residuals is a real absorption
line or a fluctuation.

## Decision 1-2 — statistic and band

`chi` on `2-28 keV, ignore bad`: 36 LAC channels holding ~520 counts each are
firmly Gaussian, and the hard band is where CRSFs live.

## Decision 3 — how to judge the line

The reflex is to add a `gabs`, read off the drop in chi-square, and turn it into a
significance — with the F-test, or the cruder `sigma = sqrt(delta-chi-square)`.
That number is not valid. The line's depth is bounded at zero, and its energy and
width mean nothing under the no-line null; the F-test assumes neither, so its
p-value is the wrong number — and because the line searches the band for the
deepest noise excursion, it is wrong in the dangerous direction, over-stating
significance.

Calibrated directly: under a pure continuum with **no line**, a searched `gabs`
reaches `delta-chi-square > 6.63` — the naive chi-square_1 "p = 0.01, 2.6 sigma"
bar — in **9.4%** of 300 line-free simulations. The real 99th percentile of the
null `delta-chi-square` is **11.5**, not 6.6. A line reported at "2.6 sigma" from
the naive threshold is really below 2 sigma.

## Decision 4 — the honest threshold, and when to stop

Report the CRSF only if its `delta-chi-square` beats the **simulated** null
distribution, not the F-test's. The right procedure is Monte-Carlo: simulate many
spectra from the best-fit no-line continuum, fit each with the searched line, and
read the p-value off the empirical distribution. The discrepancy is modest on
Ginga's 36 channels and grows sharply on NuSTAR or XRISM, where a searched line
has far more noise to find.

## Result

The false-alarm probability at the naive chi-square_1 threshold is **9.4%**, not
the nominal 1%; the Monte-Carlo 99% threshold is `delta-chi-square ~ 11.5`. The
deliverable is not a parameter but a *method*: line significance comes from
simulation, and a candidate below the simulated threshold is not a detection.

## What a careless analysis would have concluded

Add the line, see `delta-chi-square ~ 8-10`, quote "~3 sigma" from the F-test, and
announce a cyclotron line — one of the more common ways the CRSF literature has
manufactured features that later observations fail to confirm. The tell is
structural, not in the number: a bounded, searched component cannot be judged by a
test built for interior, identified parameters. Simulate the null and the "3
sigma" often falls below 2.
