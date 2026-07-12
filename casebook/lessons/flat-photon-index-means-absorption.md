---
id: flat-photon-index-means-absorption
one_line: "A power-law fit that drives the photon index implausibly flat (Gamma < ~1) is usually signalling missing low-energy absorption, not a hard intrinsic spectrum."
rule: >
  When a soft-band CCD spectrum is fit with a power law and only Galactic (or no)
  absorption, unmodelled intrinsic absorption removes soft flux and rolls the
  spectrum over at low energy. The minimiser cannot bend a single power law, so it
  flattens Gamma -- sometimes past 1, occasionally to an unphysical negative
  (rising) index -- to fake the curvature, and leaves a low-energy deficit in the
  residuals. The fix is to add an intrinsic cold absorber (ztbabs / zphabs, or
  tbabs at the source redshift), not to accept a hard Gamma. Coronal Gamma for AGN
  and XRBs lives in ~1.5-2.2; a fitted Gamma well below that with a soft residual
  deficit is an absorption symptom until proven otherwise.
applies_when: >
  soft-band data that reach below ~2 keV (Chandra, XMM, Swift-XRT, eROSITA,
  ~0.3-10 keV) of an AGN or X-ray binary; a power law with Galactic-only (or no)
  absorption returns Gamma well below ~1.5 AND leaves a systematic deficit at the
  low-energy end (runs test / residuals); adding an intrinsic absorber restores a
  normal Gamma and clears the residual.
not_when: >
  hard-band-only data (e.g. NuSTAR above 3 keV) where the absorption turnover is
  out of band and Gamma is set by other physics; genuinely flat or hard intrinsic
  spectra (some blazars, flat-spectrum sources, or reflection-dominated /
  Compton-thick sources where the observed continuum really is flat); or a flat
  Gamma accompanied by a soft EXCESS rather than a deficit (that is the opposite
  problem -- an extra soft component, not absorption).
status: validated
validation: bench/lessons/flat-photon-index-means-absorption.py
evidence_cases: [chandra-obscured-agn-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-12"
  reviewed_by: [kaa]
---

# A flat photon index is usually hidden absorption

Absorption and photon index are partially degenerate over a limited band: cold
absorption eats soft flux, and a flatter (harder) power law also has relatively
less soft flux. So when intrinsic absorption is present but omitted from the
model, the fit trades it for a flatter `Gamma`. The trade is imperfect — a power
law is scale-free and cannot reproduce the *curvature* of an absorption
turnover — so the tell is not just the flat index but the flat index **plus** a
correlated low-energy residual.

`chandra-obscured-agn-001` shows the extreme form: an absorbed Seyfert
(intrinsic nH ~ 8e22) fit with Galactic-only absorption drives `Gamma` to
**-1.0** — an inverted, rising spectrum that no AGN corona produces — with
cstat/dof ~ 5.8 and a runs-test z of -16. Restoring the intrinsic absorber
recovers `Gamma ~ 1.7` and a clean fit. The flat index was never a measurement;
it was the fit's way of complaining about a missing component.

## Why `not_when` matters

The rule is a retrieval hypothesis, not a reflex. A flat `Gamma` is only an
absorption tell when the band actually samples the turnover — hard-band-only
data (NuSTAR above 3 keV) can have a genuinely flat continuum with no soft
leverage. And some sources really are hard: flat-spectrum blazars, and
reflection-dominated or Compton-thick AGN whose *observed* continuum is
intrinsically flat. The discriminator is the residual: absorption leaves a soft
**deficit**; if instead you see a soft **excess**, the missing component is an
extra soft emitter, not an absorber. Check the residual sign before reaching for
`ztbabs`.

## Promotion status

`validated`. The harness `bench/lessons/flat-photon-index-means-absorption.py`
fits the careless Galactic-only model to an absorbed `fakeit` twin and asserts
the signal fires (`Gamma = -1.0` + `systematic_residual`, and *not*
`pegged_limit` — that would be the sibling lesson), then fits the correct
absorbed model and asserts it stays quiet (`Gamma = 1.73`, clean). Both
directions pass, so the lesson is re-verified on every run.

Not yet eligible for *promotion* into a guide/skill: that needs `len(evidence_cases) >= 3`
(PLAN-C §4), and there is one so far. Cases 2 and 4 in the roadmap will add
independent evidence.
