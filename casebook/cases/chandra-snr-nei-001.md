---
id: chandra-snr-nei-001
title: A young supernova remnant fit cool by mistake — equilibrium vs non-equilibrium plasma
status: core
context:
  mission: Chandra
  instrument: ACIS-S
  counts_regime: mid
  grouped: false
  background: none
  source_type: snr
  source_class: "young supernova remnant, under-ionized ejecta (Tau ~ 1e10)"
  model_family: [tbabs, nei]
  statistic: cstat
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: cstat
    rationale: >
      ~6000 counts over a line-rich band, ungrouped; cstat is valid throughout and
      avoids grouping away the diagnostic line ratios.
  - point: band
    choice: "0.5-8 keV, ignore bad"
    rationale: >
      Chandra ACIS-S band, holding the He- and H-like lines of Si, S, and the Fe
      complex whose ratios carry the ionization state.
  - point: model
    choice: "tbabs*nei -- non-equilibrium ionization, Tau free"
    rejected: "tbabs*apec -- collisional ionization equilibrium"
    trigger: >
      The equilibrium apec fit returns kT=0.53 keV against a true 3.0 -- a factor
      of six too low -- and an iron abundance eight times too low, at cstat/dof=2.8
      with line-ratio residuals. It read the low ionization of a young plasma as a
      cool temperature. nei recovers kT=3.2 keV and Tau=1.0e10 and drops the
      statistic by ~1070.
  - point: errors
    choice: "report Tau as a measured physical parameter (age x density)"
    rationale: >
      Tau = 9.97e9 [8.99e9, 1.10e10] is not a nuisance -- with a density estimate
      it dates the shock. Freezing it at equilibrium would discard both the
      temperature and the age.
outcome:
  verdict: bench-validated
  fit: {statistic: 341, dof: 508, method: cstat}
  result:
    kT_nei_keV: {value: 3.17, ci90: [2.49, 4.17]}
    Tau_s_per_cm3: {value: 9.97e9, ci90: [8.99e9, 1.10e10]}
    kT_apec_equilibrium_biased_keV: {value: 0.53, ci90: [0.516, 0.538], note: "wrong model; truth is 3.0"}
    delta_cstat_apec_minus_nei: 1069
lessons: [young-plasma-needs-nei-not-equilibrium]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    fakeit from tbabs*nei [nH=0.3, kT=3.0 keV, Abundanc=1.0, Tau=1e10 s/cm^3, z=0,
    norm=1e-2]; response/arf aciss_aimpt_cy15; band 0.5-8 keV ignore bad; seed 9;
    exposure ~554 s -> ~6032 counts. Fit tbabs*apec (Abund thawed, nH+z frozen) ->
    kT=0.527 [0.516,0.538], Abund=0.124, cstat 1410/509 (systematic_residual). Fit
    tbabs*nei (Abund thawed, Tau free, nH+z frozen) -> kT=3.17 [2.49,4.17],
    Tau=9.97e9 [8.99e9,1.10e10], cstat 341/508. delta-cstat(apec-nei)=1069.
---

# A young supernova remnant fit cool by mistake

## The data

A young supernova remnant on Chandra ACIS-S — ~6000 counts of a line-rich thermal
spectrum. The plasma was shocked recently enough that it has not reached
collisional ionization equilibrium: its ions sit at lower charge states than its
electron temperature would produce given time. Everything turns on recognising
that the ionization state and the temperature are two different things.

## Decision 1-2 — statistic and band

`cstat` over `0.5-8 keV, ignore bad`: ~6000 ungrouped counts across a band chosen
to hold the He- and H-like lines of Si, S, and Fe, whose ratios encode the
ionization state.

## Decision 3 — equilibrium or not, and the trap

The convenient model is `apec` — collisional ionization equilibrium, one fewer
parameter. It fails, and it fails by reading the physics backwards. Fit
`tbabs*apec` and the temperature comes back as **kT = 0.53 keV** against a true
3.0 — a factor of six too low — with the iron abundance eight times too low and
cstat/dof = 2.8, residuals sitting on the line ratios. An equilibrium model ties
ionization to temperature, so when it sees a weakly-ionized plasma it concludes
the plasma is cool. It is not cool; it is young.

Switch to `tbabs*nei`, which carries the ionization timescale `Tau` as a free
parameter, and the fit resolves: `kT = 3.2 keV`, `Tau = 1.0e10`, and the statistic
falls by ~1070. The temperature was always 3 keV; only the ionization lagged.

## Decision 4 — Tau is a measurement

`Tau = 9.97e9 [8.99e9, 1.10e10]` is not an inconvenience to freeze away. It is the
quantity a young remnant offers that an old one does not: `Tau = n_e * t`, so with
a density it dates the shock. Report it. Reaching for `apec` to avoid the extra
parameter throws away both the temperature and the age.

## Result

`kT ~ 3.2 keV` (90%: 2.5-4.2) and `Tau ~ 1.0e10 s/cm^3` — a hot, under-ionized
young plasma, correctly recovered. The equilibrium fit's 0.53 keV was an artifact
of forcing ionization and temperature to agree.

## What a careless analysis would have concluded

Fit `apec`, read `kT ~ 0.5 keV`, and describe a cool remnant with sub-solar iron —
both wrong by large factors, and both a direct consequence of the wrong plasma
model. The cstat/dof of 2.8 and the line-ratio residuals were the warning; the
physical tell is that a young remnant is out of equilibrium by definition. Fit the
ionization timescale, and the "cool, metal-poor" plasma becomes the hot,
under-ionized ejecta it always was.
