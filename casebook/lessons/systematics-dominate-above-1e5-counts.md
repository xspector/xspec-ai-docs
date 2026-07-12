---
id: systematics-dominate-above-1e5-counts
one_line: "Above ~10^5 counts the statistical error bars shrink below the ~1-2% calibration floor, so they no longer represent the real uncertainty -- you are systematics-limited, and a reduced statistic above 1 usually flags an unmodelled few-percent feature."
rule: >
  At very high counts (>~10^5) the Poisson error on a well-constrained parameter
  falls to sub-percent -- below the ~1-2% accuracy of the effective-area and
  energy-scale calibration. Quoting the statistical error alone then overstates
  the precision by an order of magnitude; fold in a systematic term before
  comparing parameters to models or to other instruments. In the same regime,
  features contributing only a few percent -- a weak line, an edge, a calibration
  residual -- become highly significant, so a reduced statistic a little above 1
  usually means an unmodelled small feature (add it, or absorb it into a
  systematic), not that the continuum is wrong. And the non-detection of such a
  feature at lower counts is not evidence of its absence -- significance scales
  with counts.
applies_when: >
  total counts above ~10^5 -- bright Galactic sources (X-ray binaries, the Crab),
  long exposures, or stacked spectra -- with per-bin counts high enough that chi
  is valid; you are about to quote parameter uncertainties or interpret a reduced
  statistic that sits a little above 1.
not_when: >
  moderate or low counts, where statistical errors genuinely dominate and the
  goodness reflects the physics; or a reduced statistic FAR above 1, which is a
  structurally wrong model (wrong continuum, missing component -- see the model
  lessons), not the sub-percent-systematics regime. This is about statistics
  having shrunk below systematics, not a licence to ignore real misfits.
status: candidate
validation: null
evidence_cases: [chandra-bhxrb-vhigh-systematics-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-12"
  reviewed_by: [kaa]
---

# Above ~10^5 counts you are systematics-limited

Two things change when a spectrum crosses ~10^5 counts, and both mislead an
analyst who is still thinking statistically.

**The error bars stop meaning what they say.** In `chandra-bhxrb-vhigh-systematics-001`
a bright soft-state black-hole binary with ~10^6 counts gives a disk temperature
of `0.703 keV` with a 90% statistical interval of **+/-0.34%**. No CCD's energy
scale and effective area are calibrated to 0.34%; the real uncertainty is the
~1-2% calibration floor, several times larger. Quoting the statistical error
alone would claim a precision the instrument does not have. The fix is to add a
systematic term (a fixed percentage, via a systematic error or a calibration
nuisance model) before the number is compared to anything.

**Small features become large.** The same weak Fe line (a modest `gaussian`) is a
**6.4-sigma** detection (delta-chi = 40.6) at 10^6 counts and a **0-sigma**
non-event (delta-chi = 0) at 10^4 counts -- identical line, identical model, only
the exposure differs. So at high counts a reduced statistic a little above 1 is
usually one such few-percent feature (or a calibration residual), not a broken
continuum; you model it, or fold it into a systematic, rather than distrust the
whole fit -- and you do not read the line's absence at lower counts as physics.

## `not_when`

The rule is about the regime where statistics have shrunk below systematics. A
reduced statistic *far* above 1 is a different problem -- a structurally wrong
model -- and belongs with the model lessons ([[flat-photon-index-means-absorption]],
[[single-temperature-fe-bias]]), not here. And at moderate counts the statistical
error is the real error; do not inflate it with a systematic you do not need.

## Promotion status

`candidate`. Needs a `bench/lessons/systematics-dominate-above-1e5-counts.py`
harness: fake one bright twin at ~10^6 and ~10^4 counts and assert (a) the
statistical error on the disk temperature is sub-percent at 10^6, and (b) a fixed
weak line is highly significant at 10^6 but insignificant at 10^4. The twin exists
in `chandra-bhxrb-vhigh-systematics-001`'s provenance.
