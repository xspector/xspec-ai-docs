---
id: xrism-cluster-turbulence-001
title: XRISM/Resolve cluster turbulence — 27000 counts, ~1 per bin, and why chi is still wrong
status: core
context:
  mission: XRISM
  instrument: Resolve
  counts_regime: high
  grouped: false
  background: none
  source_type: cluster
  source_class: "bright cluster core, Fe K turbulence (Resolve, gate-valve-closed)"
  model_family: [bapec]
  statistic: cstat
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: cstat
    rejected: chi
    rationale: >
      27128 total counts reads as `high` -- CCD instinct says chi. But Resolve
      spreads them over ~16000 fine bins in-band: median 1 count/bin, a third of
      bins empty. Fitting the same data with chi biased the iron abundance high by
      ~40% (1.00 vs a true 0.70) and the normalisation low by ~35%, behind a
      reduced chi-square of 0.67 that looks clean. cstat recovered the truth. The
      statistic is set by counts per bin, not the total.
  - point: band
    choice: "2-10 keV, ignore bad"
    rationale: >
      The Resolve gate-valve-closed effective area is useful from ~2 keV up; the
      He- and H-like Fe K complex at 6.4-7.0 keV -- the whole reason for the
      observation -- sits well inside it.
  - point: grouping
    choice: "do not group; fit every 0.5 eV bin with cstat"
    rejected: "group to ~20 counts/bin to enable chi"
    trigger: >
      From a median of 1 count/bin, reaching chi's ~20/bin means binning ~20
      channels together -- ~10 eV bins, coarser than Resolve's ~5 eV resolution
      and comparable to the ~12 eV Fe-line FWHM that encodes the turbulent
      velocity. Grouping to rescue chi would delete the measurement the
      instrument exists to make.
  - point: errors
    choice: "trust parameter recovery + cstat/dof; treat the runs test as a per-bin artifact"
    rationale: >
      assess_fit flags a systematic residual with runs-test z=-18, but the fit
      recovers every injected truth and cstat/dof=1.07. At ~1 count/bin the empty
      bins create long same-sign residual runs, so the runs test and the reduced
      statistic both mislead; goodness must come from parameter recovery and
      simulation, not those summaries.
outcome:
  verdict: bench-validated
  fit: {statistic: 17145, dof: 15995, method: cstat}
  result:
    kT_keV: {value: 5.02, ci90: [4.91, 5.13]}
    Abundanc: {value: 0.71, ci90: [0.68, 0.74]}
    Velocity_kms: {value: 209, ci90: [198, 221]}
lessons: [counts-per-bin-not-total-drives-statistic]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    fakeit from bapec, pars [kT=5.0, Abund=0.7, z=0.02, Velocity=200 km/s,
    norm=2e-2]; response rsl_Hp_L_2025.rmf + arf rsl_pntsrc_GVC_2025.arf (XRISM
    Resolve Hp, 60000 ch @ 0.5 eV, gate-valve-closed); exposure 100 ks; seed 907;
    ignore bad + 2-10 keV -> ~27128 counts over ~16000 bins, median 1/bin, 32%
    empty. cstat (z frozen) -> kT=5.02, Abund=0.71, Velocity=209 km/s,
    cstat 17145/15995. Careless chi (same data) -> Abund=1.00, norm ~35% low,
    chi/dof=0.67.
---

# XRISM/Resolve cluster turbulence

## The data

A bright cluster core observed for 100 ks with XRISM/Resolve — a microcalorimeter
that resolves the 6-7 keV iron complex at ~5 eV, the measurement CCDs cannot make.
The spectrum holds **27 000 counts**, which sounds like abundant data. But Resolve
records them across 60000 channels of 0.5 eV each; in the 2-10 keV fit band that
is ~16000 bins with a **median of 1 count** apiece and a third of them empty. Two
facts, in tension, drive the analysis: **the total is high, and the per-bin count
is ~1.** The `counts_regime` key, which reads the total, calls this `high` and so
invites exactly the wrong instinct.

## Decision 1 — statistic

`cstat`, and the total-count reflex is the trap. Fitting the *same* spectrum with
`chi` does not fail loudly: it returns a fit, with a reduced chi-square of **0.67**
that looks better than good. It is not good. The iron abundance comes out at
**1.00 solar against a true 0.70** — a ~40% overestimate — and the normalisation
~35% low. The mechanism is the sparse continuum: `chi`'s sqrt(N) weights mishandle
the mostly-empty continuum bins that anchor the abundance's line-to-continuum
ratio, so the fit over-attributes flux to the lines. `cstat`, the Poisson
likelihood, recovers `kT = 5.02`, `Abund = 0.71`, and a turbulent velocity of
`209 km/s` (truth 200) — the science payload, measured from the resolved line
widths. This is lesson
[`counts-per-bin-not-total-drives-statistic`](../lessons/counts-per-bin-not-total-drives-statistic.md).

## Decision 2 — band

`2-10 keV`, `ignore bad`. Resolve's gate-valve-closed effective area is useful
from ~2 keV, and the Fe K complex at 6.4-7.0 keV is the target. No soft extension
is worth the calibration risk below the gate-valve cutoff.

## Decision 3 — grouping, and the temptation

The way to "use chi" would be to group up until each bin holds ~20 counts. From a
median of 1, that is ~20 channels per bin — **~10 eV** bins. But Resolve's
resolution is ~5 eV, and at `kT = 5 keV` with 200 km/s of turbulence the Fe XXV
line has an intrinsic width of ~12 eV FWHM (2 eV thermal and ~4.5 eV turbulent in
quadrature, ~5 eV instrumental on top). Grouping to 10 eV bins is coarser than the
resolution and comparable to the line width itself — it smears out the very
broadening that *is* the turbulent velocity. Grouping to rescue a statistic you do
not need would throw away the measurement the observation was designed to make.
Fit the fine bins with cstat.

## Decision 4 — goodness and errors

`assess_fit` raises a systematic residual with runs-test `z = -18`. Taken at face
value that is alarming, but the fit recovers every injected parameter and
`cstat/dof = 1.07`. The runs test is fooled the same way `chi`'s reduced statistic
is: with a third of the bins empty, residuals sit in long same-sign runs by
construction, independent of any model error. At ~1 count/bin, goodness has to come
from parameter recovery against physical priors and from simulation, not from a
runs test or a reduced statistic — the low-count discipline of
[`cstat-below-1k-counts`](../lessons/cstat-below-1k-counts.md), one regime deeper.

## Result

`kT ~ 5.0 keV (90%: 4.91-5.13)`, `Abund ~ 0.71 (0.68-0.74)`, `Velocity ~ 209 km/s
(198-221)` — against truths of 5.0, 0.70, and 200. The turbulent velocity, the
headline XRISM measurement, is pinned to ~10% from the resolved line widths, and
the abundance is unbiased.

## What a careless analysis would have concluded

Read the 27 000 counts as "plenty", reach for chi because that is what one does
with bright spectra, and the reduced chi-square of 0.67 confirms the choice — a
clean-looking fit that reports a super-solar iron abundance and an underestimated
flux. Or, uneasy about the sparse bins, group to 10 eV to make chi respectable and
quietly erase the turbulent broadening, reporting a velocity consistent with zero
because the lines are now instrumentally unresolved. Both roads look reasonable and
both are wrong. The discipline is to look at the counts *per bin* rather than the
total, keep the native resolution, fit it with the Poisson likelihood, and judge
the result by what it recovers — not by a reduced statistic that sparse bins have
quietly broken.
