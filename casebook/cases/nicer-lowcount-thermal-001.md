---
id: nicer-lowcount-thermal-001
title: Low-count NICER quiescent neutron star — cstat, and why bbodyrad is the wrong model
status: core
context:
  mission: NICER
  instrument: XTI
  counts_regime: low
  grouped: false
  background: modeled
  source_type: isolated_ns
  source_class: "quiescent LMXB neutron star (globular-cluster field)"
  model_family: [tbabs, nsatmos]
  statistic: cstat
  abund: wilm
  xsect: vern
decisions:
  - point: statistic
    choice: cstat
    rejected: chi
    rationale: >
      ~600 total counts and ungrouped: the Gaussian approximation behind chi
      fails on under-populated bins and biases the fit; the NICER background is
      modelled (not subtracted), so cstat is valid and correct here.
  - point: band
    choice: "0.3-8 keV, ignore bad"
    rationale: >
      NICER's calibrated soft band; below 0.3 keV optical-loading/noise dominate,
      and above ~8 keV a soft NS is swamped by the modelled background.
  - point: model
    choice: "tbabs*nsatmos"
    rejected: "tbabs*bbodyrad"
    trigger: >
      bbodyrad drove kT to its soft-max and left a runs-test systematic
      (z=-3.0) in 0.5-2 keV; a blackbody cannot describe an H-atmosphere
      spectrum, which is spectrally hardened.
outcome:
  verdict: bench-validated
  fit: {statistic: 511.8, dof: 498, method: cstat}
  result:
    nH_1e22: {value: 0.14, ci90: [0.09, 0.21]}
    logTeff_K: {value: 6.08, ci90: [6.02, 6.13]}
    R_km: {value: 11.5, ci90: [9.8, 13.9]}
lessons: [cstat-below-1k-counts, peg-at-limit-means-wrong-model]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-02"
  reviewed_by: [kaa]
  synthetic_twin: null
---

# Low-count NICER quiescent neutron star

## The data

A quiescent low-mass X-ray binary in a globular-cluster field, ~600 counts in a
short NICER pointing, ungrouped. NICER is non-imaging, so there is no local
background to subtract — the instrumental/sky background is *modelled*
simultaneously. Two facts drive everything: **few counts** and **background
modelled, not subtracted**.

## Decision 1 — statistic

With ~600 counts spread over hundreds of channels, most bins hold single-digit
counts. `chi` assumes Gaussian per-bin errors; that approximation breaks on
under-populated bins and biases the best fit (and, classically, pulls fluxes
low). `cstat` is the Poisson likelihood and is unbiased in this regime. It is
also *valid* here specifically because the background is modelled: `cstat` on
background-**subtracted** data is not correct, but that is not this case. So
cstat, not chi — see lesson [`cstat-below-1k-counts`](../lessons/cstat-below-1k-counts.md).

## Decision 2 — band

`0.3-8 keV` with `ignore bad`. The soft cut is NICER calibration (optical
loading and detector noise dominate below ~0.3 keV); the hard cut is where a
soft thermal source falls under the modelled background. Fitting outside the
calibrated band injects garbage that the fit will happily absorb into
parameters.

## Decision 3 — model, and the trap

The obvious first model is `tbabs*bbodyrad` — an absorbed blackbody. It fits
badly in an *informative* way: `bbodyrad`'s temperature runs up to its soft
maximum and `assess_fit` flags a runs-test systematic (z = -3.0) in 0.5-2 keV.
A pegged parameter plus correlated residuals is the signature of a
*structurally wrong* model, not a bad starting point — lesson
[`peg-at-limit-means-wrong-model`](../lessons/peg-at-limit-means-wrong-model.md).

The physics: a neutron-star surface has a light-element atmosphere that
redistributes flux to higher energies (spectral hardening), so a fitted
blackbody reports a temperature that is too high and, through the Stefan-
Boltzmann normalisation, an emitting radius far too small. `nsatmos` (an
H-atmosphere model) encodes this. Swapping to `tbabs*nsatmos` removes the pegged
parameter and the residual structure, and yields a physically sensible neutron-
star radius.

## Result

`nH ~ 0.14e22`, `log Teff ~ 6.08` (~110 eV), `R ~ 11.5 km` — a plausible
neutron-star radius, with 90% intervals from `error` after re-fitting.

## What a careless analysis would have concluded

`chi` + `bbodyrad` would have "worked": it converges and returns tight error
bars. It would report a hotter, *much* smaller emitting region (a few km) — and
quote confident uncertainties on it. Both the value and its error would be
wrong: the value because a blackbody is the wrong spectral shape for an
atmosphere, the error because chi mis-estimates it at these counts. For a
neutron-star radius — an equation-of-state constraint — that is not a harmless
slip. The tell was visible without knowing the answer: a pegged parameter and a
failed runs test. `assess_fit` surfaces both; the discipline is to act on them
rather than report the first fit that converges.
