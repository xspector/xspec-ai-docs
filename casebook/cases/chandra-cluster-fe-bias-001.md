---
id: chandra-cluster-fe-bias-001
title: Cluster metallicity on Chandra — how a single temperature biases the iron abundance threefold
status: core
context:
  mission: Chandra
  instrument: ACIS-S
  counts_regime: high
  grouped: false
  background: none
  source_type: cluster
  source_class: "multi-temperature ICM (cool-core / wide-annulus, ~1-2.5 keV)"
  model_family: [tbabs, apec]
  statistic: cstat
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: cstat
    rejected: chi
    rationale: >
      48600 counts reads `high`, but a cluster CCD spectrum is peaked: the Fe-L
      complex and soft continuum are bright while the hard Fe-K tail is sparse
      (55% of bins hold <20 counts here). chi would be invalid across that tail
      without heavy grouping; cstat is correct across the whole band and keeps the
      Fe-K line unbinned.
  - point: band
    choice: "0.5-7.0 keV, ignore bad"
    rationale: >
      Chandra ACIS-S calibrated band, spanning both abundance diagnostics: the
      Fe-L blend (~0.7-1.3 keV) and the Fe-K line (~6.7 keV).
  - point: model
    choice: "tbabs*(apec+apec) -- two temperatures"
    rejected: "tbabs*apec -- single temperature"
    trigger: >
      The single-T fit leaves cstat/dof=5.5 with a systematic residual and drives
      the iron abundance to 0.17 -- a factor of three below the true 0.50 -- with a
      deceptively tight 90% interval [0.16, 0.18]. Adding a second temperature
      clears the residual (cstat/dof=1.10), recovers the two phases (kT ~ 1.0 and
      2.5 keV), and returns Fe = 0.51 [0.46, 0.56].
  - point: errors
    choice: "distrust the single-T error bar; report the two-T interval"
    rationale: >
      The single-T abundance interval [0.16, 0.18] is tight and excludes the truth
      -- false precision from a wrong model. An elevated statistic in a cluster is
      usually unmodelled temperature structure, not a measurement; the honest error
      is the wider two-T interval on the correct model.
outcome:
  verdict: bench-validated
  fit: {statistic: 482, dof: 439, method: cstat}
  result:
    Abundanc_two_temperature: {value: 0.51, ci90: [0.46, 0.56]}
    Abundanc_single_temperature_biased: {value: 0.17, ci90: [0.16, 0.18]}
    kT_cool_keV: {value: 0.99, ci90: [0.98, 1.00]}
    kT_hot_keV: {value: 2.47, ci90: [2.39, 2.56]}
lessons: [single-temperature-fe-bias]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    fakeit from tbabs*(apec+apec), pars [nH=0.02, kT1=1.0, Abund=0.5, z=0.05,
    norm1=1e-2, kT2=2.5, Abund=0.5, z=0.05, norm2=2e-2]; response/arf
    aciss_aimpt_cy15; exposure 8000 s; seed 4401; ignore bad + 0.5-7 keV ->
    ~48609 counts, median 14/bin. Single-T tbabs*apec (Abund thawed, nH+z frozen)
    -> Fe=0.169 [0.160,0.178], kT=1.31, cstat 2407/441 (systematic_residual).
    Two-T tbabs*(apec+apec) (Abund thawed + tied across components) -> Fe=0.510
    [0.460,0.564], kT 0.99/2.47, cstat 482/439 -- truth recovered.
---

# Cluster metallicity on Chandra

## The data

A bright cluster/group core on Chandra ACIS-S — ~48 600 counts, source-dominated.
The gas is not isothermal: the extraction blends a cool ~1 keV phase and a hotter
~2.5 keV phase (a cool core, or simply a wide annulus along which temperature
varies). The abundance is what we are after, and it is read off two
temperature-sensitive features — the Fe-L blend near 1 keV and the Fe-K line at
6.7 keV.

## Decision 1 — statistic

`cstat`. The counts are high, but a cluster CCD spectrum is sharply peaked: the
Fe-L complex and soft continuum are bright while the hard tail carrying Fe-K is
thin — here 55% of the in-band bins hold fewer than 20 counts. `chi` would be
invalid across that tail unless the spectrum were heavily grouped, and grouping
coarsens the Fe-K line. `cstat` is valid across the whole band at any per-bin
count — the same counts-per-bin reasoning that governs high-resolution data, met
here on a CCD.

## Decision 2 — band

`0.5-7.0 keV`, `ignore bad` — the ACIS-S calibrated band, chosen to span both
abundance diagnostics rather than the Fe-K line alone.

## Decision 3 — one temperature or two, and the trap

Fit a single `tbabs*apec` and it fails informatively: `cstat/dof = 5.5` with a
systematic residual concentrated at the Fe-L complex, because one temperature
cannot shape that blend for gas that spans 1-2.5 keV. The minimiser buys the
misfit by collapsing the abundance — iron comes out at **0.17, a factor of three
below the true 0.50** — and, worse, quotes a *tight* 90% interval [0.16, 0.18]
around that wrong value.

Add a second temperature, `tbabs*(apec+apec)` with the abundance tied across the
two phases, and everything resolves: the residual clears (`cstat/dof = 1.10`), the
two temperatures come back at 0.99 and 2.47 keV, and the iron abundance recovers to
**0.51 [0.46, 0.56]** — the truth, with an honest, wider error. See lesson
[`single-temperature-fe-bias`](../lessons/single-temperature-fe-bias.md).

## Decision 4 — which error bar to believe

The single-T interval [0.16, 0.18] is precise and wrong; the two-T interval
[0.46, 0.56] is wider and right. The lesson is not "quote bigger error bars" — it
is that a confidence interval is only as trustworthy as the model under it, and an
elevated statistic tells you that model is incomplete.

## Result

Two-temperature ICM: `kT ~ 0.99` and `2.47 keV`, `Fe ~ 0.51 (90%: 0.46-0.56)` —
recovering the injected 1.0/2.5 keV phases and Fe = 0.50. The single-temperature
metallicity of 0.17 was an artifact of the missing phase.

## What a careless analysis would have concluded

Fit one temperature, read off `Fe ~ 0.17 ± 0.01`, and report a metal-poor cluster
with confidence — a threefold error dressed in a tight error bar. The `cstat/dof`
of 5.5 was shouting that the model was wrong, and the residual pointed straight at
the Fe-L complex; ignoring it turned a modelling shortfall into a false physical
result. At these counts the bad fit is obvious, but the same bias operates, less
visibly, in moderate-S/N spectra where a single-temperature fit can look
acceptable — which is why an ICM metallicity should never be trusted until a
second temperature (or a DEM) has been tried.
