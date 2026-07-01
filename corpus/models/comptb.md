---
name: comptb
type: add  # additive
func: c_xscomptb
n_params: 7
family: [comptb]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelComptb.tex
---

# comptb

**additive model** (`add`), function `c_xscomptb`.

## Description

This model describes the Comptonization spectrum of soft photons off
electrons which are either purely thermal or additionally subjected to
an inward bulk motion. It consists of two components: one is the
direct seed photon spectrum and the other one is the Comptonized
spectrum. The latter is obtained as a self-consistent convolution of
the seed photon spectrum with the system Green's function.

The model is not specific to bulk Comptonization but it includes in a
coherent way different spectral shapes such as simple blackbody
(i.e. neither thermal nor bulk Comptonization), thermal Comptonization
(equivalent to `compTT`) and thermal plus bulk Comptonization. In the
latter case, it can be considered a completion and update of the `bmc`
model, as it includes the cut-off term in the spectrum.

All mathematical details of the model and its validity limits for
applications are reported in [Farinelli et al. (2008, ApJ 680, 602)](https://ui.adsabs.harvard.edu/abs/2008ApJ...680..602F/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kTs | keV | 1 | 0.1 | 10 | 0.1 | 10 | 0.1 |  |
| 2 | gamma | — | 3 | 1 | 10 | 1 | 10 | 0.01 | frozen by default |
| 3 | alpha | — | 2 | 0 | 400 | 0 | 400 | 0.01 |  |
| 4 | delta | — | 20 | 0 | 200 | 0 | 200 | 0.01 |  |
| 5 | kTe | keV | 5 | 0.2 | 2000 | 0.2 | 2000 | 0.1 |  |
| 6 | log_A | — | 0 | -8 | 8 | -8 | 8 | 0.01 |  |
| 7 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("comptb")
# component: m.comptb  (params as attributes)
```
