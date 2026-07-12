---
id: below-100-counts-cannot-discriminate-models
one_line: "Below ~100 counts, continuum models of similar shape (blackbody vs disk-blackbody, thermal vs power law) fit equally well -- do not claim one over the other, and report non-parabolic intervals."
rule: >
  With of order 100 counts the data cannot resolve the difference between models
  of similar spectral shape. A delta-fit-statistic of a couple between, say,
  blackbody and disk-blackbody is pure noise -- the WRONG model can even fit
  marginally better by chance. Fit with the model you have physical reason to
  prefer, but state that the data do not constrain the choice; quote the
  temperature/flux with the asymmetric, non-parabolic interval from cstat `error`
  or `steppar` (not the covariance sigma); take goodness from Monte-Carlo, not the
  reduced statistic. Do not build a physical story on a model choice the counts
  cannot support -- and remember the derived quantities (emitting radius, inner
  disk radius) differ between the models even when the fits do not.
applies_when: >
  counts_regime vlow (< ~100 total counts), comparing continuum models of similar
  shape (blackbody / disk-blackbody / bremsstrahlung, or thermal vs a soft power
  law); a small delta-fit-statistic is being read as evidence for one model.
not_when: >
  enough counts that the models genuinely diverge -- a well-measured spectral
  shape does separate blackbody from disk-blackbody -- or models that differ
  sharply even at low counts (a strong line vs none at a known energy; a hard
  power law vs a soft thermal peak). The rule is about similar-shaped continua in
  the counts-starved regime, not a claim that models are never distinguishable.
status: validated
validation: bench/lessons/below-100-counts-cannot-discriminate-models.py
evidence_cases: [chandra-tde-supersoft-vlow-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-12"
  reviewed_by: [kaa]
---

# Below ~100 counts you cannot choose the model

A super-soft transient caught in a short pointing gives you tens of counts and a
temperature to measure. The temptation is to also decide *what kind* of thermal
source it is -- a bare blackbody, or a disk. At these counts you cannot.

`chandra-tde-supersoft-vlow-001` makes it concrete: ~81 counts from an absorbed
`bbodyrad` (kT = 0.10 keV). Fit the true blackbody and you get cstat = 76.3; fit a
`diskbb` instead and you get **74.7** -- the wrong model fits *better*, by
delta-cstat = 1.6, which is noise. Neither the reduced statistic nor the
delta-cstat can tell them apart. What differs is the physics you would report: the
blackbody gives kT = 0.10 keV, the disk gives Tin = 0.12 keV, and their emitting-
radius interpretations diverge further -- a distinction the data simply do not
make.

Two corollaries at this count level, both faces of [[cstat-below-1k-counts]]:

- **The error bars are not parabolic.** The blackbody temperature is
  0.100 keV with a 90% interval of -0.009 / +0.011 -- asymmetric. Quote it from
  `error` or `steppar`, not from a symmetric covariance sigma that assumes a
  parabola the likelihood does not have.
- **Goodness comes from simulation.** With ~80 counts spread over the band, the
  reduced statistic and the runs test are too noisy to trust; a Monte-Carlo
  `goodness` is the only honest check.

## `not_when`

Give the same source enough counts and the models *do* separate -- a blackbody and
a disk-blackbody have genuinely different curvature that a well-measured spectrum
resolves. The rule is specific to the counts-starved regime; it is not a claim
that spectral models are forever indistinguishable.

## Promotion status

`validated`. The harness `bench/lessons/below-100-counts-cannot-discriminate-models.py`
fakes the blackbody twin at ~80 and ~40000 counts: at 80 counts blackbody and
disk-blackbody are indistinguishable (delta-cstat = -1.6, the wrong model even
wins), while at 40000 counts diskbb is decisively worse (delta-cstat = +170) —
both directions.

Not yet eligible for *promotion* into a guide/skill: that needs
`len(evidence_cases) >= 3` (PLAN-C §4), and there is one so far.
