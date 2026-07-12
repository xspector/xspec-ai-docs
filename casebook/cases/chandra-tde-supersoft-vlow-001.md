---
id: chandra-tde-supersoft-vlow-001
title: A super-soft TDE in 81 counts — the temperature you can measure, the model you cannot
status: core
context:
  mission: Chandra
  instrument: ACIS-S
  counts_regime: vlow
  grouped: false
  background: none
  source_type: tde
  source_class: "super-soft tidal disruption event (kT ~ 0.1 keV), short pointing"
  model_family: [tbabs, bbodyrad]
  statistic: cstat
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: cstat
    rejected: chi
    rationale: >
      ~81 counts total: nearly every bin is empty or single-digit. chi's Gaussian
      per-bin assumption fails outright; cstat is the Poisson likelihood and the
      only valid choice.
  - point: band
    choice: "0.3-1.5 keV, ignore bad"
    rationale: >
      A super-soft ~0.1 keV blackbody has essentially all its flux below ~1 keV;
      the ACIS-S soft band captures the peak and there is nothing above 1.5 keV.
  - point: model
    choice: "tbabs*bbodyrad, and DECLINE to claim it over tbabs*diskbb"
    rejected: "asserting blackbody vs disk-blackbody from the fit"
    trigger: >
      Fitting the (true) blackbody gives cstat=76.3/79; fitting a disk-blackbody
      instead gives 74.7/79 -- the wrong model fits marginally BETTER, by
      delta-cstat=1.6, which is noise. At 81 counts the two are statistically
      indistinguishable; the choice is a physical assumption, not a measurement.
  - point: errors
    choice: "report the asymmetric kT interval from cstat error; goodness by Monte-Carlo"
    rationale: >
      The blackbody temperature is 0.100 keV with a 90% interval of -0.009/+0.011
      -- non-parabolic. Quote it from error/steppar, not a symmetric covariance
      sigma, and check goodness by simulation, since the reduced statistic and
      runs test are too noisy at this count level.
outcome:
  verdict: bench-validated
  fit: {statistic: 76.3, dof: 79, method: cstat}
  result:
    kT_blackbody_keV: {value: 0.100, ci90: [0.0915, 0.1110], note: "asymmetric (non-parabolic)"}
    Tin_diskbb_keV: {value: 0.123, note: "alternative model, indistinguishable fit"}
    model_discrimination: {delta_cstat_diskbb_minus_bbody: -1.6, verdict: "indistinguishable at 81 counts"}
lessons: [cstat-below-1k-counts, below-100-counts-cannot-discriminate-models]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    fakeit from tbabs*bbodyrad [nH=0.05, kT=0.10 keV, norm=1e3]; response/arf
    aciss_aimpt_cy15; band 0.3-1.5 keV ignore bad; seed 7; exposure 2000 s ->
    ~81 counts. Fit tbabs*bbodyrad (nH frozen) -> kT=0.100 [0.0915,0.1110] (90%,
    asymmetric), cstat 76.3/79. Fit tbabs*diskbb -> Tin=0.123, cstat 74.7/79;
    delta-cstat=-1.6 (the wrong model fits marginally better -- indistinguishable).
---

# A super-soft TDE in 81 counts

## The data

A super-soft tidal disruption event — a ~0.1 keV thermal source — caught in a
short Chandra pointing that yielded **~81 counts**. That is enough to measure a
temperature and not much else. The discipline here is knowing which questions the
counts can answer and which they cannot.

## Decision 1 — statistic

`cstat`, without hesitation. At 81 counts spread across the soft band, essentially
every channel is empty or holds a single count. `chi` is meaningless here; `cstat`
is the Poisson likelihood. (This is the counts-starved end of
[`cstat-below-1k-counts`](../lessons/cstat-below-1k-counts.md).)

## Decision 2 — band

`0.3-1.5 keV`. A 0.1 keV blackbody peaks near 0.3 keV and has no flux to speak of
above 1 keV; the soft ACIS-S band holds all the signal there is.

## Decision 3 — the model you cannot choose

The temperature is measurable. The *kind* of thermal source is not. Fit the true
blackbody and cstat is 76.3/79; swap in a disk-blackbody and it is **74.7/79** —
the wrong model fits marginally better, by a delta-cstat of 1.6, which at this
count level is pure noise. The data do not distinguish `bbodyrad` from `diskbb`.
That matters, because the two tell different physical stories: kT = 0.10 keV for
the blackbody, Tin = 0.12 keV for the disk, and their emitting-radius
interpretations diverge further still. The honest report picks one model on
physical grounds (a TDE early on is often disk-like) and says plainly that the
data cannot confirm the choice — see
[`below-100-counts-cannot-discriminate-models`](../lessons/below-100-counts-cannot-discriminate-models.md).

## Decision 4 — how to quote the temperature

`kT = 0.100 keV`, 90% interval **-0.009 / +0.011** — asymmetric, because at 81
counts the likelihood is not a parabola. Quote it from `error`/`steppar`, not from
a symmetric covariance sigma that would misstate both ends. Goodness, likewise,
comes from a Monte-Carlo `goodness` simulation; the reduced statistic and the runs
test are too noisy to mean anything with this many counts.

## Result

`kT ~ 0.10 keV` (90%: 0.092-0.111), emitting a blackbody-or-disk spectrum the data
cannot separate. The measurement is a temperature with an honest, asymmetric error
bar — and an explicit statement of what was *not* determined.

## What a careless analysis would have concluded

See delta-cstat = 1.6 in favour of the disk model and announce "the spectrum
prefers a disk" — a claim built entirely on noise, that a different 81-count draw
would reverse. Or quote `kT = 0.100 +/- 0.010 keV` from the covariance matrix,
hiding the asymmetry, and read a reduced statistic near 1 as a good fit without
ever simulating it. At 81 counts the discipline is modesty: measure the
temperature, report it with the interval the likelihood actually has, and refuse
the model comparison the data cannot support.
