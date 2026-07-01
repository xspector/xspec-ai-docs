---
name: grbcomp
type: add  # additive
func: c_xsgrbcomp
n_params: 10
family: [grbcomp]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelGrbcomp.tex
---

# grbcomp

**additive model** (`add`), function `c_xsgrbcomp`.

## Description

This model has been proposed by [Titarchuk et
  al. (2012)](https://ui.adsabs.harvard.edu/abs/2012ApJ...752..116T/abstract) as a
possible scenario for the spectral emission of the prompt phase of
Gamma Ray Bursts.

It is essentially a two-phase model: up to the peak energy E$_{\rm p}$ of the
EF(E) spectrum soft thermal blackbody-like photons are comptonized by
a subrelativistic bulk outflow of thermal electrons, while the
high-energy tail is obtained by a further convolution of the formerly
comptonized spectrum with a Green's function. An example of the
application of the model to a sample of GRBs can be found in [Frontera
et al. (2013)](https://ui.adsabs.harvard.edu/abs/2013ApJ...779..175F/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kTs | keV | 1 | 0 | 20 | 0 | 20 | 0.1 |  |
| 2 | gamma | — | 3 | 0 | 10 | 0 | 10 | 0.01 |  |
| 3 | kTe | keV | 100 | 0.2 | 2000 | 0.2 | 2000 | 0.1 |  |
| 4 | tau | — | 5 | 0 | 200 | 0 | 200 | 0.01 |  |
| 5 | beta | — | 0.2 | 0 | 1 | 0 | 1 | 0.01 |  |
| 6 | fbflag | — | 0 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 7 | log_A | — | 5 | -8 | 8 | -8 | 8 | 0.01 | frozen by default |
| 8 | z | — | 0 | 0 | 10 | 0 | 10 | 1 | frozen by default |
| 9 | a_boost | — | 5 | 0 | 30 | 0 | 30 | 0.01 | frozen by default |
| 10 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("grbcomp")
# component: m.grbcomp  (params as attributes)
```
