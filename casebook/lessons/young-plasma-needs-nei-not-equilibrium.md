---
id: young-plasma-needs-nei-not-equilibrium
one_line: "A young / under-ionized plasma (SNR ejecta, recent shock) must be fit with a non-equilibrium model (nei/vnei/pshock), not an equilibrium one (apec/mekal), which reads the low ionization as a low temperature and gets kT badly wrong."
rule: >
  In a young supernova remnant the plasma has not had time to reach collisional
  ionization equilibrium: the ionization state lags the electron temperature and
  is set by the ionization timescale Tau = n_e * t. An equilibrium model (apec,
  mekal, vapec) has no such freedom -- it ties ionization to temperature -- so it
  interprets the low ionization as a low temperature and badly underestimates kT,
  dragging the abundances with it. Fit an NEI model (nei, vnei, pshock, sedov)
  and treat Tau as a physical parameter (age times density), not a nuisance. The
  tell is a poor equilibrium fit with residuals at the He- and H-like line ratios
  of Si, S, and Fe.
applies_when: >
  young or recently-shocked optically-thin thermal plasma -- SNR ejecta or shell,
  typically ages below a few thousand years, or a low ionization timescale
  Tau ~ 1e10-1e11 s/cm^3; an equilibrium fit leaves line-ratio residuals or returns
  an implausibly low temperature.
not_when: >
  an old, relaxed remnant or diffuse ISM that has reached equilibrium
  (Tau > ~1e12 s/cm^3), where apec is correct and adding Tau just overfits; or a
  plasma whose temperature is independently pinned (e.g. by a bright continuum) and
  whose ionization is consistent with that temperature. NEI is for the
  counts-carrying under-ionized case, not every thermal spectrum.
status: candidate
validation: null
evidence_cases: [chandra-snr-nei-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-12"
  reviewed_by: [kaa]
---

# A young remnant is not in equilibrium

The ionization state of a hot plasma is not a proxy for its temperature unless the
plasma has had time to relax. In a young SNR it has not: shocked only recently,
its ions sit at lower charge states than their electron temperature would produce
in equilibrium. The single number that governs this is the ionization timescale
`Tau = n_e * t` -- and an equilibrium model does not have it.

`chandra-snr-nei-001` shows what the omission costs. A `nei` plasma at
`kT = 3.0 keV` with `Tau = 1e10` (young, under-ionized) fit with equilibrium `apec`
returns `kT = 0.53 keV` -- a **factor of six** too low -- and an iron abundance
eight times too low, with cstat/dof = 2.8 and residuals across the line ratios.
`apec` read the low ionization as a cool plasma. Switching to `nei` recovers
`kT = 3.2 keV` and `Tau = 1.0e10` and drops the statistic by ~1070; the
temperature was never cool, only under-ionized.

## Tau is physics, not a nuisance

The temptation is to treat `Tau` as an inconvenient extra knob and freeze it, or
to reach for `apec` because it has fewer parameters. But `Tau` *is* the
measurement a young remnant offers -- combined with a density estimate it dates
the shock. Fit it, and report it. Freezing it at equilibrium throws away both the
temperature and the age.

## `not_when`

An old, relaxed remnant that has reached equilibrium (`Tau` above ~1e12) is
correctly described by `apec`, and forcing an NEI model there only adds an
unconstrained parameter. The rule is for the young, under-ionized regime; check
whether the ionization state is actually out of equilibrium before committing to
NEI.

## Promotion status

`candidate`. Needs a `bench/lessons/young-plasma-needs-nei-not-equilibrium.py`
harness: fake a low-Tau `nei` twin, fit equilibrium `apec` and assert kT is badly
underestimated with a much worse statistic, while `nei` recovers kT and Tau. The
twin exists in `chandra-snr-nei-001`'s provenance.
