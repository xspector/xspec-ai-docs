---
name: optxagnf
type: add  # additive
func: optxagnf
n_params: 12
family: [optxagnf, optxagn]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelOptxagn.tex
---

# optxagnf

**additive model** (`add`), function `optxagnf`.

Variants documented together: `optxagnf`, `optxagn`.

## Description

AGN spectral energy distributions are complex, but can be
phenomenologically fit by a disc, optically thick, low temperature
thermal Comptonisation (to produce the soft X-ray excess) and an
optically thin, high temperature themal Comptonisation (to produce the
power law emission which dominates above 2 keV). Here we combine these
three components together assuming that they are all ultimately
powered by gravitational energy released in accretion. We assume that
the gravitational energy released in the disc at each radius is
emitted as a (colour temperature corrected) blackbody only down to a
given radius, $R_{corona}$. Below this radius, we further assume that the
energy can no longer completely thermalise, and is distributed between
powering the soft excess component and the high energy tail. This
imposes an important energetic self consistency on the model. The key
aspect of this model is that the optical luminosity constrains the
mass accretion rate through the outer disc, $\dot{M}$, provided there is an
independent estimate of the black hole mass (from e.g. the H$\beta$ emission
line profile). The total luminosity available to power the entire SED
is $L_{tot} = eff \dot{M} c^2$, where the efficiency is set by black hole spin
assuming Novikov-Thorne emissivity.

There are two versions of the model. `optxagnf` is the one recommended
for most purposes, and has the colour temperature correction
calculated for each temperature from the approximations given in [Done
et al. (2012)](https://ui.adsabs.harvard.edu/abs/2012MNRAS.420.1848D/abstract). `optxagn` instead allows the user to define their own
colour temperature correction, $f_{col}$, which is then applied to annuli
with effective temperature $> T_{scatt}$. In both models the flux is set by
the physical parameters of mass, $L/L){Edd}$, spin and distance, hence the
model normalisations MUST be frozen at unity.

Parameters in `optxagnf`:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | mass | solar | 10000000 | 1 | 1000000000 | 1 | 1000000000 | 0.1 | frozen by default |
| 2 | dist | Mpc | 100 | 0.01 | 1000000000 | 0.01 | 1000000000 | 0.01 | frozen by default |
| 3 | logLoLEdd | — | -1 | -10 | 2 | -10 | 2 | 0.01 |  |
| 4 | astar | — | 0 | 0 | 0.998 | 0 | 0.998 | 1 | frozen by default |
| 5 | rcor | rg | 10 | 1 | 100 | 1 | 100 | 0.1 |  |
| 6 | logrout | — | 5 | 3 | 7 | 3 | 7 | 0.01 | frozen by default |
| 7 | kT_e | keV | 0.2 | 0.01 | 10 | 0.01 | 10 | 0.01 |  |
| 8 | tau | — | 10 | 0.1 | 100 | 0.1 | 100 | 0.1 |  |
| 9 | Gamma | — | 2.1 | 1.05 | 5 | 1.05 | 10 | 0.01 |  |
| 10 | fpl | — | 0.0001 | 0 | 1 | 0 | 1 | 1e-06 |  |
| 11 | Redshift | — | 0 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 12 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("optxagnf")
# component: m.optxagnf  (params as attributes)
```
