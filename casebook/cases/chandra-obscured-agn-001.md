---
id: chandra-obscured-agn-001
title: Obscured Seyfert on Chandra — why an unabsorbed fit drives the photon index flat
status: core
context:
  mission: Chandra
  instrument: ACIS-S
  counts_regime: mid
  grouped: false
  background: none
  source_type: agn
  source_class: "obscured (Compton-thin) Seyfert 2"
  model_family: [tbabs, ztbabs, powerlaw]
  statistic: cstat
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: cstat
    rejected: chi
    rationale: >
      ~8200 counts (mid regime) but ungrouped, so many bins are under-populated;
      cstat is safe across the whole count range and avoids grouping decisions.
      chi would be defensible only after grouping to >~20 counts/bin — and it is
      not the statistic that decides this case, the model is.
  - point: band
    choice: "0.5-8 keV, ignore bad"
    rationale: >
      Chandra ACIS-S calibrated band. The soft cut matters here specifically
      because the absorption turnover sits just inside it (~1-3 keV); cutting
      higher would throw away the very leverage that reveals the obscuration.
  - point: model
    choice: "tbabs*ztbabs*powerlaw"
    rejected: "tbabs*powerlaw (Galactic absorption only)"
    trigger: >
      With only Galactic absorption the power law cannot bend to the soft
      turnover, so the fit drove PhoIndex to -1.0 (an inverted, rising spectrum
      no AGN corona produces), cstat/dof=5.8, runs-test z=-16.4. Adding an
      intrinsic redshifted absorber restored Gamma~1.7 and a clean fit.
outcome:
  verdict: bench-validated
  fit: {statistic: 536.28, dof: 509, method: cstat}
  result:
    nH_intrinsic_1e22: {value: 7.92, ci90: [7.51, 8.35]}
    PhoIndex: {value: 1.73, ci90: [1.61, 1.85]}
    norm: {value: 2.70e-3, ci90: [2.20e-3, 3.32e-3]}
lessons: [flat-photon-index-means-absorption]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    fakeit from tbabs*ztbabs*powerlaw, pars [nH_gal=0.03, nH_z=8.0, z=0.05,
    Gamma=1.8, norm=3e-3]; response/arf aciss_aimpt_cy15; exposure 40000 s; seed
    51841; ignore bad + 0.5-8 keV -> ~8200 counts. Careless fit tbabs*powerlaw
    (nH frozen at Galactic 0.03) -> Gamma=-1.0, cstat 2949.3/510. Correct fit
    tbabs*ztbabs*powerlaw (nH_gal, z frozen) -> nH_z=7.92, Gamma=1.73,
    cstat 536.3/509; all three truth values recovered inside the 90% intervals.
---

# Obscured Seyfert on Chandra

## The data

A moderately obscured Seyfert 2 at z = 0.05, ~8200 counts in a 40 ks Chandra
ACIS-S pointing, ungrouped, source-dominated (no background). The source is
Compton-thin but heavily absorbed: an intrinsic column of ~8e22 cm^-2 on top of a
small Galactic 0.03e22. Nothing in the header announces the absorption — it has
to be read off the spectral shape, and that is exactly where the trap is.

## Decision 1 — statistic

`cstat`. At ~8200 total counts this is the `mid` regime, where `chi` becomes
usable *if the data are well grouped*; ungrouped, many bins are under-populated
and `chi` would bias the fit. `cstat` is correct across the whole count range and
sidesteps a grouping choice that is irrelevant to the point of this case. The
statistic is not what makes or breaks this analysis — the model is.

## Decision 2 — band

`0.5-8 keV` with `ignore bad` — the Chandra ACIS-S calibrated band. The soft edge
is load-bearing here in a way it is not for an unabsorbed source: the intrinsic
absorption rolls the spectrum over at ~1-3 keV, and that curvature is the only
direct evidence of the obscuration. Restricting to a harder band (say >2 keV)
would discard the turnover and leave the column unconstrained — a real failure
mode when analysts hard-cut to "avoid the messy soft end".

## Decision 3 — model, and the trap

The careless model assumes the source is unobscured — a Type 1 prior — and fits
`tbabs*powerlaw` with the column frozen at the Galactic value (0.03e22). It
"converges", and the result is nonsense in an *informative* way: `PhoIndex` is
driven to **-1.0**. A photon index of -1 is a spectrum that *rises* with energy;
no AGN corona produces that. The fit is contorting the one knob it has — the
slope — to imitate a curvature it cannot actually reproduce, because a power law
is scale-free and an absorption turnover is not. `assess_fit` makes the failure
unambiguous: cstat/dof = 5.8 and a runs-test z of **-16.4** (a huge correlated
residual). Note what does *not* happen: `PhoIndex` is not pegged at a hard limit,
so this is not the pegged-parameter signature of
[`peg-at-limit-means-wrong-model`](../lessons/peg-at-limit-means-wrong-model.md)
— it is the flatter, quieter tell that
[`flat-photon-index-means-absorption`](../lessons/flat-photon-index-means-absorption.md)
names: an implausible index plus a soft residual deficit.

The physics: cold gas absorbs soft flux, and so does a harder power law, so the
two are partially degenerate over a limited band. Omit the absorber and the fit
pays for the missing soft opacity with a flatter (here, inverted) slope. Add an
intrinsic redshifted absorber — `tbabs*ztbabs*powerlaw`, with the Galactic column
and the redshift frozen at their known values — and the degeneracy breaks:
`Gamma` recovers to 1.73, the intrinsic column comes out at 7.9e22, and the
runs-test systematic clears (z = -1.9, cstat/dof = 1.05).

## Result

`nH_intrinsic ~ 7.9e22 (90%: 7.5-8.4)`, `Gamma ~ 1.73 (1.61-1.85)`, in a source
whose true values were 8e22 and 1.8 — both recovered inside the 90% intervals.
The reported photon index is now a normal Seyfert coronal slope, and the column
is a measurement rather than an artifact.

## What a careless analysis would have concluded

The unabsorbed fit does not error out; it returns a number. An analyst who trusts
convergence would report a hard, even inverted, photon index and — because the
normalisation is anchored to the absorbed flux — a wrong 2-10 keV luminosity, and
might go on to describe the source as an unusually hard AGN, or invoke a reflection
or jet component to explain a "flat spectrum" that is really just cold gas. The
inverted `Gamma` should stop that story before it starts: coronal indices live in
~1.5-2.2, and a fitted value far outside that with a soft residual deficit is an
absorption symptom, not a discovery. The tell was visible without knowing the
answer — an unphysical parameter and a failed runs test — and `assess_fit`
surfaces both. The discipline is to read a flat index as a question ("what soft
opacity am I missing?"), not an answer.
