---
name: sirf
type: add  # additive
func: C_sirf
n_params: 10
family: [sirf]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelSirf.tex
---

# sirf

**additive model** (`add`), function `C_sirf`.

## Description

The multi-blackbody ``Self-IrRadiated Funnel'' model is designed to
model optically-thick outflow-dominated accretion. The basic idea is
simple: you just assume a lot of matter, angular momentum and energy
emerges in a limited volume. Momentum conservation leads to
non-sphericity of the flow that has subsequently conical (funnel-like)
shape. The model calculates temperature distribution at the funnel
walls (taking into account irradiation by iterative process) and the
outer photosphere. We also assume that inside the cone there is a deep
pseudo-photosphere. Relativistic boosts are taken into account for
high velocities. For a comprehensive description of the physical
model, see: [Abolmasov, Karpov & Kotani (2009)](https://ui.adsabs.harvard.edu/abs/2009PASJ...61..213A/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | tin | keV | 1 | 0.01 | 100 | 0.01 | 1000 | 0.01 |  |
| 2 | rin | rsph | 0.01 | 1e-05 | 1 | 1e-06 | 10 | 0.001 |  |
| 3 | rout | rsph | 100 | 0.1 | 100000000 | 0.1 | 100000000 | 0.01 |  |
| 4 | theta | deg | 22.9 | 1 | 89 | 0 | 90 | 0.001 |  |
| 5 | incl | deg | 0 | -90 | 90 | -90 | 90 | 1 | frozen by default |
| 6 | valpha | — | -0.5 | -1 | 2 | -1.5 | 5 | 1 | frozen by default |
| 7 | gamma | — | 1.333 | 0.5 | 10 | 0.5 | 10 | 1 | frozen by default |
| 8 | mdot | — | 1000 | 0.5 | 10000000 | 0.5 | 10000000 | 1 | frozen by default |
| 9 | irrad | — | 2 | 0 | 10 | 0 | 20 | 1 | frozen by default |
| 10 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("sirf")
# component: m.sirf  (params as attributes)
```
