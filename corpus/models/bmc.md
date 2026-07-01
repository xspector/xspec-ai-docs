---
name: bmc
type: add  # additive
func: xsbmc
n_params: 4
family: [bmc]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelBmc.tex
---

# bmc

**additive model** (`add`), function `xsbmc`.

## Description

This is an analytic model describing Comptonization of soft photons by
matter undergoing relativistic bulk-motion. The typical scenario
involves thermal X-rays from the inner region of an accretion disk in
a black-hole binary illuminating in-falling matter in close proximity
to the black-hole event horizon. 

For a detailed description of the model, refer to [Titarchuk,
Mastichiadis & Kylafis 1997, ApJ, 487, 834](https://ui.adsabs.harvard.edu/abs/1997ApJ...487..834T/abstract); [Titarchuk & Zannias, 1998,
ApJ, 493, 863](https://ui.adsabs.harvard.edu/abs/1998ApJ...493..863T/abstract); [Laurent & Titarchuk 1999, ApJ, 511, 289](https://ui.adsabs.harvard.edu/abs/1999ApJ...511..289L/abstract); [Borozdin, Revnivtsev, Trudolyubov, Shrader, & Titarchuk, 1999, ApJ,
517, 367](https://ui.adsabs.harvard.edu/abs/1999ApJ...517..367B/abstract); or [Shrader & Titarchuk 1999, ApJ 521, L121](https://ui.adsabs.harvard.edu/abs/1999ApJ...521L.121S/abstract).

The model parameters are the characteristic black-body temperature of
the soft photon source, a spectral (energy) index, and an illumination
parameter characterizing the fractional illumination of the
bulk-motion flow by the thermal photon source. It must be emphasized
that this model is not an additive combination of power law and
thermal sources, rather it represents a self-consistent
convolution. The bulk-motion up-scattering and Compton recoil combine
to produce the hard spectral tail, which combined with the thermal
source results in the canonical high-soft-state spectrum of black hole
accretion. The position of the sharp high energy cutoff (due to
recoil) can be determined using the theta function
$\theta(E_c-E)$. The model can also be used for the general
Comptonization case when the energy range is limited from above by the
plasma temperature (see `compTT` and `compST`).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.01 | 100 | 0.0001 | 200 | 0.05 |  |
| 2 | alpha | — | 1 | 0.01 | 4 | 0.0001 | 6 | 0.01 |  |
| 3 | log_A | — | 0 | -6 | 6 | -8 | 8 | 0.01 |  |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bmc")
# component: m.bmc  (params as attributes)
```
