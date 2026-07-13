---
id: ixpe-polarization-mdp-001
title: A polarization that isn't there — the MDP, and why PD/error lies
status: core
context:
  mission: IXPE
  instrument: "GPD (toy telescope example)"
  counts_regime: vhigh
  grouped: false
  background: none
  source_type: xrb
  source_class: "IXPE spectro-polarimetry, toy point source (Stokes I/Q/U)"
  model_family: [polconst, powerlaw]
  statistic: chi
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: chi
    rejected: chistokes
    rationale: >
      The Stokes I/Q/U triplet is fit jointly against the polconst*powerlaw model
      via the Stokes XFLT dispatch. On the toy spectra the Q/U errors are
      independent (no XCOV covariance column), so chi is exact and recovers the
      injected polarization (A=0.498 vs a true 0.4986). Real IXPE data carry the
      Q/U cross-spectrum covariance and must use chistokes -- but the positive-bias
      of the polarization degree, the point of this case, is independent of the
      statistic.
  - point: band
    choice: "2-8 keV, ignore bad"
    rationale: "The IXPE / GPD calibrated band."
  - point: errors
    choice: "judge the polarization against the MDP99, not PD/sigma_PD"
    rejected: "reporting PD +/- sigma_PD and reading PD/sigma as a significance"
    trigger: >
      PD = sqrt(Q^2+U^2)/I is positive-definite. For a truly UNPOLARIZED source
      (~10^6 counts), 200 realizations give a measured PD of median 0.18% and 99th
      percentile 0.48% -- never zero. PD/sigma_PD exceeds 2 in 15.5% of them and 3
      in 1.5%, so a "2-3 sigma polarization" is often noise. The MDP99 = 0.48% =
      3.0*sigma_PD is the honest threshold.
  - point: stop
    choice: "claim polarization only above the MDP; de-bias or give an upper limit below it"
    rationale: >
      A genuinely polarized source (PD=10%) is recovered at 64 sigma, far above the
      MDP -- no ambiguity. The discipline bites only near and below the MDP, exactly
      where positive bias masquerades as signal.
outcome:
  verdict: bench-validated
  result:
    unpolarized_measured_PD_median_pct: 0.18
    MDP99_pct: 0.48
    MDP99_over_sigma: 3.04
    sigma_PD_pct: 0.16
    false_positive_rate_PD_over_sigma_gt2_pct: 15.5
    false_positive_rate_PD_over_sigma_gt3_pct: 1.5
    polarized_source_A0p10_recovered: {value: 0.101, significance_sigma: 64}
lessons: [polarization-below-mdp-not-a-detection]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    Toy IXPE example: load Stokes I/Q/U (toy_point_source_du1_pha1{,q,u}.fits) into
    one data group, responses toyteldu1fictionalv002.rmf with .arf (I) and .mrf
    (Q/U); band 2-8 keV. Model polconst*powerlaw. UNPOLARIZED twin (A=0, Gamma=2,
    norm=10, exposure 5000 s -> ~1.17e6 I-counts): 200 fakeit realisations (seeds
    700+i), each fit with chi and A free in [0,1]. Measured PD: median 0.18%,
    99th pct (MDP99) 0.48%, median sigma_PD 0.16% (MDP99 = 3.04 sigma). P(PD/sigma
    >2)=15.5%, P(>3)=1.5%. Polarized twin (A=0.10) -> measured 0.101, 64 sigma.
    (chistokes needs the XCOV covariance that grouped real data carry; the toy
    spectra are independent, so chi is used.)
---

# A polarization that isn't there

## The data

An IXPE spectro-polarimetry observation — the Stokes I, Q, and U spectra of a
point source, fit jointly with a polarization model. (This uses the manual's toy
telescope responses; the numbers are illustrative, the phenomenon is real.) The
question is whether a measured polarization degree is a detection, and the trap is
that the polarization degree cannot be measured as zero even when it is.

## Decision 1 — statistic

`chi` here, `chistokes` in production. The `polconst*powerlaw` model is evaluated
for each Stokes spectrum through the `Stokes` XFLT dispatch, and fit jointly. On
the toy spectra the Q and U errors are independent (no `XCOV` covariance column),
so `chi` is exact — it recovers the injected polarization (A = 0.498 against a true
0.4986). Real IXPE spectra carry the Q/U cross-spectrum covariance and must be fit
with `chistokes`. None of this changes the point below, which is a property of the
polarization *degree*, not of the statistic.

## Decision 2 — band

`2-8 keV`, the GPD calibrated band.

## Decision 3 — the measurement that cannot be zero

`PD = sqrt(Q^2 + U^2)/I` is an amplitude, so it is positive-definite: scatter Q and
U around zero and the vector length is always positive. Simulate a truly
**unpolarized** source (~10^6 counts) 200 times and the measured PD has a median of
**0.18%** and a 99th percentile of **0.48%** — it is never zero. Worse, the formal
significance lies: `PD/sigma_PD` exceeds 2 in **15.5%** of the unpolarized
realizations and 3 in **1.5%**. A "2.5-sigma polarization" quoted from `PD/sigma`
is, under the null, about a one-in-six event — not a detection.

## Decision 4 — use the MDP, and know where it bites

The honest threshold is the **Minimum Detectable Polarization**,
`MDP99 = 4.29/(mu*sqrt(N)) ~ 3*sigma_PD` — here **0.48%**, exactly 3.0 times the
`sigma_PD` of 0.16%. Claim a polarization only above it; below it, de-bias the
estimate or report an upper limit. And know where the caution applies: a genuinely
polarized source at `PD = 10%` is recovered at **64 sigma**, far above the MDP,
with no ambiguity at all. Positive bias is a near-threshold problem.

## Result

For the unpolarized source the deliverable is an *upper limit* (PD < MDP99 =
0.48%), not a detection — despite a fit that returns PD = 0.18% +/- 0.16% and a
tempting `PD/sigma` around 1-2. For the polarized source, a clean 10% detection.
The measurement of record is the one compared to the MDP.

## What a careless analysis would have concluded

Fit the Stokes spectra, read `PD = 0.35% +/- 0.16%`, note `PD/sigma ~ 2.2`, and
announce a "~2-sigma hint of polarization" — a claim that a re-observation of the
same unpolarized source would fail to reproduce, because 15% of unpolarized draws
clear that bar. The tell is structural: a positive-definite quantity has a
non-Gaussian null, so its error ratio is not a significance. Compare to the MDP,
and the "hint" becomes the upper limit it always was.
