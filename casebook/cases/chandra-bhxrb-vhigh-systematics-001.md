---
id: chandra-bhxrb-vhigh-systematics-001
title: A million-count black-hole binary — where the error bars stop meaning what they say
status: core
context:
  mission: Chandra
  instrument: ACIS-S
  counts_regime: vhigh
  grouped: false
  background: none
  source_type: xrb
  source_class: "bright black-hole X-ray binary, soft/thermal state (~1e6 counts)"
  model_family: [tbabs, diskbb, powerlaw, gaussian]
  statistic: chi
  abund: angr
  xsect: vern
decisions:
  - point: statistic
    choice: chi
    rejected: cstat
    rationale: >
      This is the one regime where chi is unambiguously right: ~10^6 counts over
      ~500 bins is a median of ~330 counts/bin, so every bin is richly Gaussian
      and chi is valid and standard. cstat would also be fine; grouping is
      unnecessary.
  - point: band
    choice: "0.5-8 keV, ignore bad"
    rationale: "Chandra ACIS-S calibrated band; a soft-state disk plus a hard tail sit inside it."
  - point: errors
    choice: "add a systematic error before quoting uncertainties"
    rejected: "quote the statistical 90% interval as the uncertainty"
    trigger: >
      At 10^6 counts the statistical interval on the disk temperature is
      0.703 keV +/-0.34% -- an order of magnitude tighter than the ~1-2%
      effective-area/energy-scale calibration. The statistical error is no longer
      the real error; the observation is systematics-limited, and quoting +/-0.34%
      would claim a precision the detector does not have.
  - point: add_component
    choice: "model the weak line (or fold it into a systematic); do not distrust the continuum"
    trigger: >
      A modest Fe Ka line is a 6.4-sigma detection (delta-chi=40.6) at 10^6 counts
      but a 0-sigma non-event at 10^4 counts -- same line, same model, only the
      exposure differs. A reduced statistic just above 1 at these counts is such a
      few-percent feature, not a wrong continuum.
outcome:
  verdict: bench-validated
  fit: {statistic: 517, dof: 507, method: chi}
  result:
    Tin_keV: {value: 0.703, ci90_stat_pct: 0.34, note: "statistical only; << ~1-2% calibration floor"}
    PhoIndex: {value: 2.67, ci90_stat_pct: 3.65}
    FeKa_line_significance: {at_1e6_counts: "6.4 sigma (dChi 40.6)", at_1e4_counts: "0 sigma (dChi 0.0)"}
lessons: [systematics-dominate-above-1e5-counts]
provenance:
  source: hand-authored
  contributor: kaa
  date: "2026-07-12"
  reviewed_by: [kaa]
  synthetic_twin: >
    fakeit from tbabs*(diskbb+powerlaw+gaussian), pars [nH=0.5, Tin=0.7,
    dnorm=1000, Gamma=2.5, plnorm=0.1, LineE=6.4, Sigma=0.05, gnorm=3e-4];
    response/arf aciss_aimpt_cy15; band 0.5-8 keV, ignore bad; seed 20219. Faked
    at exposure 2424 s (~1.0e6 counts, median ~330/bin) and 24 s (~1.0e4 counts).
    At 1e6: full-model chi 517/507; disk Tin 0.703 with a +/-0.34% statistical
    interval; Fe line delta-chi 40.6 (6.4 sigma). At 1e4: Fe line delta-chi 0.0.
    The ACIS response is a soft-band-CCD vehicle; the vhigh regime is what NICER /
    NuSTAR / stacked spectra reach.
---

# A million-count black-hole binary

## The data

A bright black-hole X-ray binary in its soft/thermal state — a multicolour disk
(`diskbb`, Tin ~ 0.7 keV) plus a steep Comptonized tail (`powerlaw`, Gamma ~ 2.5)
— accumulated to **~10^6 counts**. At this depth the arithmetic of uncertainty
inverts: the thing that limits you is no longer how many photons you caught but
how well the instrument is calibrated. (The twin uses a Chandra ACIS-S response
as a generic soft-band CCD; the count regime is what NICER, NuSTAR, or stacked
spectra reach in practice.)

## Decision 1 — statistic

`chi`. This is the one regime where the CCD-era reflex is correct: ~10^6 counts
over ~500 channels is a median of ~330 counts per bin, so every bin is firmly in
the Gaussian limit and `chi` is valid and standard. `cstat` would serve equally;
no grouping is needed. (Contrast the earlier cases, where sparse bins made `chi`
the wrong call — here the counts really are everywhere.)

## Decision 2 — band

`0.5-8 keV`, `ignore bad` — the ACIS-S band, spanning the disk and the hard tail.

## Decision 3 — the error bars stop meaning what they say

Fit the model and the disk temperature comes back as `Tin = 0.703 keV` with a 90%
statistical interval of **+/-0.34%**. That precision is fictional. No CCD's
effective area and gain are known to 0.34%; the honest floor is the ~1-2%
calibration systematic, several times wider. Reporting +/-0.34% would assert a
temperature measured to a third of a percent that the instrument cannot actually
deliver. At >10^5 counts the statistical error is the *smaller* of the two
uncertainties and no longer the relevant one — a systematic term has to be folded
in before the number is compared to a model, another epoch, or another
instrument. (Note also how uneven the shrinkage is: the subdominant power law's
Gamma still carries a ~3.7% statistical error, because it is poorly separated from
the disk in this band — high counts do not rescue a degeneracy.)

## Decision 4 — a reduced statistic above 1 is usually a small feature

The same regime makes small things loud. A modest Fe Ka line — one `gaussian` —
is a **6.4-sigma** detection (delta-chi = 40.6) at 10^6 counts and a **0-sigma**
non-event (delta-chi = 0) at 10^4 counts. Nothing about the line changed; only the
exposure did. So a reduced chi-square sitting a little above 1 at these counts is
almost always one such few-percent feature (a weak line, an edge, a calibration
residual), and the response is to model it or absorb it into a systematic — not to
conclude the continuum is wrong, and not to chase every wiggle as if it were the
statistic's due. Equally, the line's *absence* at 10^4 counts is not evidence it
is not there.

## Result

`Tin ~ 0.703 keV` (statistical +/-0.34%, but calibration-limited to ~1-2%),
`Gamma ~ 2.67` (+/-3.7% statistical), with a 6.4-sigma Fe Ka line that a 10^4-count
snapshot of the same source would miss entirely. The measurement of record is the
one with a systematic error attached.

## What a careless analysis would have concluded

Report `Tin = 0.703 +/- 0.002 keV` and treat it as a third-of-a-percent
measurement — then find it "disagrees at many sigma" with the next epoch or with
another instrument, and invent physics to explain a difference that is entirely
cross-calibration. Or see the reduced chi-square above 1, distrust the disk-plus-
powerlaw model, and start swapping continua, when the excess is one weak line that
a systematic error or a single `gaussian` would absorb. At a million counts the
discipline is to stop reading the statistical error bar as the uncertainty, add a
systematic, and treat marginal reduced-statistic excesses as small features to
model — not as verdicts on the continuum.
