---
id: polarization-below-mdp-not-a-detection
one_line: "Polarization degree is positive-definite, so an unpolarized source still returns a non-zero measured PD; judge a detection against the MDP, not the PD/error ratio."
rule: >
  The polarization degree PD = sqrt(Q^2 + U^2)/I is a positive-definite quantity,
  so even a truly unpolarized source returns a measured PD > 0 (Rice/Rayleigh
  distributed, median ~1.25 sigma, never zero). Its formal ratio PD/sigma_PD is
  NOT Gaussian: under the unpolarized null it exceeds 2 about 15% of the time and 3
  about 1.5% of the time, so a "2-3 sigma polarization" is frequently just noise.
  The honest detection threshold is the Minimum Detectable Polarization,
  MDP99 = 4.29/(mu*sqrt(N)) ~ 3*sigma_PD: claim a polarization only if the measured
  PD exceeds the MDP, and de-bias the estimate when it is comparable to it. (Fit
  the Stokes I/Q/U with chistokes on real data, so the Q/U covariance is handled;
  the positive-bias phenomenon itself is independent of the statistic.)
applies_when: >
  X-ray polarimetry (IXPE, and future missions) -- estimating a polarization
  degree and angle from Stokes I/Q/U spectra with polconst/pollin/polpow (or the
  physical stokes models); a measured PD with a formal error is being read as a
  detection.
not_when: >
  PD well above the MDP -- a high-significance detection, where the positive bias
  is negligible and PD/sigma is meaningful (a genuinely polarized source at
  PD >> MDP is recovered cleanly). Also, the caution is about the positive-definite
  amplitude PD; the signed normalised Stokes parameters q=Q/I and u=U/I
  individually are unbiased and may be treated normally.
status: validated
validation: bench/lessons/polarization-below-mdp-not-a-detection.py
evidence_cases: [ixpe-polarization-mdp-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-12"
  reviewed_by: [kaa]
---

# A measured polarization below the MDP is noise

Polarization is measured as an amplitude, PD = sqrt(Q^2 + U^2)/I, and an amplitude
cannot be negative. So the measurement is biased: scatter Q and U around zero (an
unpolarized source) and the length of the resulting vector is always positive,
never zero. Reporting that length as "the polarization degree", with its formal
error bar, manufactures a detection out of noise.

`ixpe-polarization-mdp-001` quantifies it on the toy IXPE example. For a truly
**unpolarized** source (~10^6 counts), 200 realizations give a measured PD with a
median of **0.18%** and a 99th percentile of **0.48%** -- never zero, always
positive. The formal significance misleads badly: `PD/sigma_PD` exceeds 2 in
**15.5%** of the unpolarized realizations and 3 in **1.5%**, so a naively-quoted
"2.5 sigma polarization" is really a ~1-in-6 fluctuation. The honest bar is the
MDP: here MDP99 = 0.48% = 3.0 * sigma_PD, and a measured PD below it is not a
detection. A genuinely polarized source (PD = 10%) sits at 64 sigma, far above the
MDP -- detected without ambiguity.

## The pattern

This is the same positive-definite / boundary problem as
[[ftest-invalid-for-line-significance]] (a line depth bounded at zero) and the
low-count boundary in [[cstat-below-1k-counts]]: a quantity pinned at a boundary
has a non-Gaussian null distribution, and its naive error-ratio over-states
significance. For polarimetry the fix has a name and a formula -- the MDP -- so use
it: report PD only above MDP99, and de-bias (or give an upper limit) below it.

## `not_when`

Well above the MDP the bias is negligible and PD/sigma is meaningful; a strong
polarization detection needs no special handling. And the signed Stokes parameters
q, u are individually unbiased -- it is only their positive-definite combination PD
that carries the bias.

## Promotion status

`validated`. The harness `bench/lessons/polarization-below-mdp-not-a-detection.py`
simulates unpolarized Stokes triplets on the toy IXPE responses and asserts the
measured PD is positive-biased (median > 0), `PD/sigma > 2` in ~14% of null
realizations (vs the Gaussian ~2.3%), and MDP99 ~ 3 sigma — while a genuine 10%
polarization is recovered at ~63 sigma, far above the MDP. Both directions.

Not yet eligible for *promotion* into a guide/skill: that needs
`len(evidence_cases) >= 3` (PLAN-C §4), and there is one so far.
