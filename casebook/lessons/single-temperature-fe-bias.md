---
id: single-temperature-fe-bias
one_line: "Fitting a single-temperature plasma to multi-phase cluster/group gas biases the measured metallicity (usually low -- the 'Fe bias'); an elevated fit statistic is the tell."
rule: >
  The intracluster/intragroup medium is rarely isothermal along a line of sight
  (cool cores, projection, multi-phase gas). A single apec/vapec/mekal fit cannot
  match the temperature-sensitive Fe-L complex (~0.7-1.3 keV) and the Fe-K line
  (~6.7 keV) at the same time, and compensates by driving the fitted iron
  abundance away from the truth -- classically LOW (the Fe bias / Fe-L bias),
  sometimes by a large factor. The signature is an elevated fit statistic
  (reduced stat >> 1, systematic residuals around Fe-L); the fix is a second
  temperature (or a differential-emission-measure model: gadem, cemekl). The
  single-temperature abundance error bar is deceptively tight and can exclude the
  true value, so a careless analyst reports a confident, wrong metallicity.
applies_when: >
  cluster / group / ICM, or any optically-thin thermal plasma, whose emission
  integrates a range of temperatures (cool-core spectra, wide extraction annuli,
  projected multi-phase gas) fit with a single thermal component; the fit leaves
  an elevated statistic or residuals concentrated near the Fe-L complex, and
  adding a second temperature both clears the residual and moves the abundance.
not_when: >
  genuinely near-isothermal gas (some relaxed-cluster annuli), where a single
  temperature is adequate and adding one is overfitting; or when the elevated
  statistic comes from background / calibration / absorption rather than
  temperature structure -- check WHERE the residuals sit (Fe-L region vs
  broadband) before blaming temperature. Note the direction is not universal: at
  high temperature (>~3-4 keV, Fe-K-dominated) a single-T fit to multi-T gas can
  bias the abundance HIGH (the inverse Fe bias) -- the sign depends on the
  temperature range spanned.
status: candidate
validation: null
evidence_cases: [chandra-cluster-fe-bias-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-12"
  reviewed_by: [kaa]
---

# A single temperature biases the cluster metallicity

Iron abundance in the ICM is read mainly off the Fe-L complex (a blend of Fe XVII-XXIV
lines near 1 keV) and the Fe-K line at 6.7 keV, and the *shape* of the Fe-L blend
changes rapidly with temperature between ~1 and ~3 keV. When the gas actually spans
a range of temperatures but is modelled with one, the fit cannot reproduce that
blend and trades abundance for the misfit — usually pushing it low.

`chandra-cluster-fe-bias-001` is stark: a two-phase ICM (1.0 and 2.5 keV, true
Fe = 0.5 solar) fit with a single apec returns `Fe = 0.17` — a **factor of three
low** — with a tight 90% interval [0.16, 0.18] that a careless analyst would quote
with confidence. The fit is not silent about the problem (cstat/dof = 5.5, a
systematic residual), and adding a second temperature restores `Fe = 0.51`
[0.46, 0.56] and a good fit. The elevated statistic was the diagnosis; the biased
abundance was the cost of ignoring it.

## The insidious version

At these counts the single-T misfit is obvious. The danger in the literature is
the *moderate*-S/N spectrum where a single-T fit looks statistically acceptable
yet the metallicity is still biased — the bias does not vanish with the residual's
visibility. Treat any single-temperature ICM metallicity as suspect until a
second temperature (or a DEM) has been tried, especially for cool cores and wide
annuli. This is the [[counts-per-bin-not-total-drives-statistic]] discipline's
cousin: the summary statistic can look fine while the physics is wrong.

## Promotion status

`candidate`. Needs a `bench/lessons/single-temperature-fe-bias.py` harness (fit
single-apec and apec+apec to the same multi-T `fakeit` twin; assert the single-T
abundance is biased away from truth while the two-T recovers it) before it can move
to `validated` (PLAN-C §4). The twin exists in `chandra-cluster-fe-bias-001`'s
provenance.
