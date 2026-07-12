---
id: counts-per-bin-not-total-drives-statistic
one_line: "The statistic is set by counts per bin, not total counts: a high-resolution spectrum with tens of thousands of counts but ~1 per fine bin still needs cstat, not chi."
rule: >
  chi's Gaussian per-bin errors are valid only when each bin is well populated
  (~20+ counts). Total counts is irrelevant to that condition. A microcalorimeter
  or grating spectrum can hold tens of thousands of counts and still have ~1 count
  in most of its fine bins, because the resolution spreads them over thousands of
  channels. In that regime chi biases the parameters that depend on the
  line-to-continuum balance (abundance high, normalisation/flux low) while
  reporting a reduced chi-square below 1 that looks like a good fit. Use cstat.
  And do not group up to reach chi's regime when doing so coarsens the bins past
  the instrumental resolution -- that trades away the very spectral resolution the
  observation was taken to get.
applies_when: >
  high-resolution data -- microcalorimeter (XRISM/Resolve, future Athena X-IFU) or
  gratings (Chandra HETG/LETG, XMM RGS) -- where total counts are high (mission
  might read `mid`/`high`/`vhigh`) but per-bin counts are low (median ~a few or
  fewer, many empty bins), and the science rests on resolved line profiles
  (widths -> turbulence/velocity, shifts, ratios).
not_when: >
  genuinely well-populated bins -- CCD data grouped to ~20+ counts/bin, or a bright
  continuum source at moderate resolution -- where chi is valid and faster to
  reason about; or a modest grouping that stays FINER than the instrumental
  resolution (grouping is not forbidden per se -- only grouping past the resolution
  to rescue chi is). The bin, not the exposure or the total, is what to look at.
status: candidate
validation: null
evidence_cases: [xrism-cluster-turbulence-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-12"
  reviewed_by: [kaa]
---

# Counts per bin, not total counts, picks the statistic

The reflex "bright source, lots of counts -> chi" is a CCD-era habit. It fails on
high-resolution data because chi's premise is about the *bin*, not the
observation: the Gaussian approximation to Poisson needs each bin well populated,
and a microcalorimeter spreads even a bright source's photons over tens of
thousands of ~eV channels, so most bins hold zero or one count regardless of the
total.

`xrism-cluster-turbulence-001` makes it concrete: a Resolve spectrum of a bright
cluster core with **27 000 total counts** — which the `counts_regime` key, keyed
on the total, calls `high` — but a **median of 1 count per bin** and a third of
its bins empty. Fitting it with chi biases the iron abundance high by ~40% (1.0
against a true 0.7) and the flux low by ~35%, all behind a reduced chi-square of
0.67 that reads as a clean fit; cstat recovers the truth, including a turbulent
velocity of 209 km/s (truth 200) from the resolved line widths.

## Two corollaries

- **Don't group to rescue chi.** Reaching chi's ~20 counts/bin from a median of 1
  means binning ~20 channels together — ~10 eV bins, coarser than Resolve's ~5 eV
  resolution and comparable to the ~12 eV Fe-line width that *encodes the
  turbulence*. You would delete the measurement to satisfy a statistic you did not
  need. cstat keeps every fine bin.
- **Per-bin blindness runs deeper than the statistic.** At ~1 count/bin the runs
  test and the reduced statistic both mislead (empty bins create long same-sign
  residual runs; the reduced chi-square sinks below 1). Judge the fit by parameter
  recovery against physical priors and by simulation-based goodness, not by those
  summaries — the same low-count discipline as [[cstat-below-1k-counts]], one
  regime further in.

## `not_when`

This is not "never group high-resolution data" and not "cstat is always safer so
always use it". Grouping that stays finer than the instrumental resolution is
fine, and well-populated bins are chi's proper home. The rule is only that the
*total* count is the wrong thing to look at — inspect the counts per bin.

## Promotion status

`candidate`. Needs a `bench/lessons/counts-per-bin-not-total-drives-statistic.py`
harness (fit chi and cstat to the same microcalorimeter `fakeit` twin; assert chi
biases the abundance/flux away from truth while cstat recovers them) before it can
move to `validated` (PLAN-C §4). The twin exists in
`xrism-cluster-turbulence-001`'s provenance.
