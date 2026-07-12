---
id: chandra-grb-afterglow-001
title: Faint GRB afterglow at low counts — cstat over chi, and freezing what the data cannot constrain
status: core
context:
  mission: Chandra
  instrument: ACIS-S
  counts_regime: low
  grouped: false
  background: none
  source_type: grb
  source_class: "GRB X-ray afterglow, faint follow-up snapshot at z=0.5"
  model_family: [tbabs, ztbabs, powerlaw]
  statistic: cstat
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: cstat
    rejected: chi
    rationale: >
      ~566 total counts over ~470 channels (~1 count/bin). Fitting the same data
      with chi (standard weighting) biased the normalisation low by nearly a
      factor of two (0.62e-3 vs a true 1.2e-3 -- the classic low-count flux
      pull), softened Gamma to 1.81, and returned a spurious reduced chi-square
      of 0.49 that reads as a "great fit" while hiding the bias. cstat is the
      Poisson likelihood and recovered the truth.
  - point: band
    choice: "0.5-8 keV, ignore bad"
    rationale: >
      Chandra ACIS-S calibrated band. With so few counts there is nothing to gain
      and calibration edges to lose by pushing wider.
  - point: model
    choice: "freeze Galactic nH at the LAB value and z at the optical redshift; fit only intrinsic nH, Gamma, norm"
    rejected: "thaw all five parameters"
    trigger: >
      566 counts cannot constrain five parameters. Freeing the Galactic column
      and the redshift too drove nH_Gal to peg at 0, pulled z to 0.281 (the
      optical value is 0.5), and improved cstat by only 0.8 for two extra
      parameters -- a false, unphysical minimum bought with freedom the data do
      not support.
  - point: errors
    choice: "wide 90% intervals; goodness by Monte-Carlo simulation"
    rationale: >
      assess_fit's runs test flagged a systematic (z=-3.5), but the fit recovers
      the injected truth with cstat/dof=0.91 and a Monte-Carlo goodness of 93%
      (not rejected). At ~1 count/bin the runs test is oversensitive to Poisson
      quantisation; the simulated goodness is the correct arbiter, and the honest
      result is a set of wide, correlated intervals -- not a tight number.
outcome:
  verdict: bench-validated
  fit: {statistic: 462.6, dof: 509, method: cstat}
  result:
    nH_intrinsic_1e22: {value: 11.45, ci90: [9.56, 13.54]}
    PhoIndex: {value: 2.02, ci90: [1.66, 2.38]}
    norm: {value: 1.21e-3, ci90: [0.71e-3, 2.12e-3]}
lessons: [cstat-below-1k-counts]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    fakeit from tbabs*ztbabs*powerlaw, pars [nH_gal=0.08, nH_z=12.0, z=0.5,
    Gamma=2.0, norm=1.2e-3]; response/arf aciss_aimpt_cy15; exposure 6000 s; seed
    202; ignore bad + 0.5-8 keV -> ~566 counts. Disciplined cstat (nH_gal, z
    frozen) -> nH_z=11.45, Gamma=2.02, norm=1.21e-3, cstat 462.6/509, goodness 93%
    -- truth recovered. Careless chi (same data) -> Gamma=1.81, norm=0.62e-3,
    chi/dof=0.49. Careless free-everything cstat -> nH_gal pegged 0, z=0.281,
    Delta-cstat=-0.8 (false minimum).
---

# Faint GRB afterglow at low counts

## The data

A GRB X-ray afterglow caught in a short, faint Chandra snapshot — ~566 counts,
ungrouped, source-dominated. The redshift (z = 0.5) is known from the optical
afterglow, and the Galactic column is known from the LAB/HI4PI 21 cm surveys.
Two facts set the whole analysis: **few counts**, and **two absorbers** — a
Galactic screen and a host-galaxy column at the source redshift — that ~566
counts cannot both constrain. The workflow here is identical for a Swift-XRT,
Einstein-Probe, or eROSITA soft-band snapshot; the twin uses a Chandra ACIS-S
response only because that is the calibrated soft-band response on hand.

## Decision 1 — statistic

`cstat`, and here the choice has teeth. Fitting the *same* data with `chi`
(standard weighting) does not fail loudly — it returns a fit. But the
normalisation comes out at `0.62e-3`, nearly **half** the true `1.2e-3`: the
classic low-count flux bias, where `chi`'s sqrt(N) errors over-weight the empty
bins and drag the continuum down. It softens `Gamma` to 1.81, and — most
insidiously — reports a reduced chi-square of **0.49**, which a careless analyst
reads as an excellent fit rather than as the symptom of broken weighting that it
is. `cstat`, the Poisson likelihood, recovers `norm = 1.21e-3` and `Gamma =
2.02`. This is exactly the regime of lesson
[`cstat-below-1k-counts`](../lessons/cstat-below-1k-counts.md).

## Decision 2 — band

`0.5-8 keV`, `ignore bad` — the Chandra ACIS-S calibrated band. At these counts
there is no signal to be won by pushing to the noisy edges, only calibration
systematics to let in.

## Decision 3 — freedom, and the trap

The model — `tbabs*ztbabs*powerlaw` — is right; the trap is *how many of its
parameters you free*. The disciplined choice freezes the Galactic column at its
LAB value and the redshift at the optical value, and fits only the three things
the data can actually speak to: the host column, `Gamma`, and the normalisation.

Thawing everything is the mistake. Freeing the Galactic `nH` and `z` as well
drives `nH_Gal` to peg at **0** (unphysical — there is always a Galactic screen),
pulls the fitted redshift to **0.281** (flatly contradicting the optically
measured 0.5), and improves `cstat` by all of **0.8** for the two extra
parameters. That is no improvement at all; it is the minimiser wandering through
a degenerate valley that ~566 counts cannot resolve, and landing on a
physically wrong point that a reader might then over-interpret. Known quantities
measured by *other* instruments (the Galactic column, the redshift) are inputs,
not free parameters, when the counts are this thin.

## Decision 4 — goodness and errors

`assess_fit` flags a systematic residual (runs-test z = -3.5). Taken alone that
looks like trouble, but the fit recovers the injected truth on all three free
parameters, `cstat/dof = 0.91`, and a 1000-trial Monte-Carlo `goodness` returns
**93%** — below the 95% rejection line, i.e. acceptable. At ~1 count per bin the
runs test is oversensitive to Poisson quantisation; the simulated goodness is the
right arbiter (another face of the low-count lesson — goodness by Monte-Carlo,
not by a reduced statistic). The honest deliverable is a set of **wide,
correlated** 90% intervals, not a tight central value.

## Result

`nH_intrinsic ~ 11.5e22 (90%: 9.6-13.5)`, `Gamma ~ 2.02 (1.66-2.38)`, `norm ~
1.21e-3 (0.71-2.12e-3)` — against injected truths of `12e22`, `2.0`, and
`1.2e-3`, all three recovered. The error bars are broad because the data are
thin, and saying so is part of the result.

## What a careless analysis would have concluded

Two failure modes, both quiet. Use `chi` and you would report a source about half
as bright as it is, with a softened slope, under cover of a reduced chi-square
near 0.5 that looks *better* than a good fit — a low-count flux bias dressed as a
clean result. Or free every parameter and you would report a host redshift of
0.28 that disagrees with the optical value, and a Galactic column of zero, quoting
their formal error bars as if they meant something. Both fits "converge" and
return numbers. The discipline is to pick the statistic that is unbiased on
Poisson data, freeze what other instruments already measured, judge goodness by
simulation rather than a reduced statistic, and report intervals wide enough to
tell the truth about ~566 counts.
