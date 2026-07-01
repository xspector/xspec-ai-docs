---
name: compmag
type: add  # additive
func: c_xscompmag
n_params: 9
family: [compmag]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelCompmag.tex
---

# compmag

**additive model** (`add`), function `c_xscompmag`.

## Description

This model describes the spectral formation in the accretion column
onto the polar cap of a magnetized neutron star, with both thermal and
bulk Comptonization processes taken into account. The details for the
method adopted for the numerical solution of the radiative transfer
equation are reported in [Farinelli et al. (2012, A&A, 538, A67)](https://ui.adsabs.harvard.edu/abs/2012A&A...538A..67F/abstract).

This model can be used for spectral fitting of both accreting X-ray
pulsars and Supergiant Fast X-ray Trasients.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kTbb | keV | 1 | 0.2 | 10 | 0.2 | 10 | 0.1 |  |
| 2 | kTe | keV | 5 | 0.2 | 2000 | 0.2 | 2000 | 0.1 |  |
| 3 | tau | — | 0.5 | 0 | 10 | 0 | 10 | 0.1 |  |
| 4 | eta | — | 0.5 | 0.01 | 1 | 0.01 | 1 | 0.01 |  |
| 5 | beta0 | — | 0.57 | 0.0001 | 1 | 0.0001 | 1 | 0.01 |  |
| 6 | r0 | — | 0.25 | 0.0001 | 100 | 0.0001 | 100 | 0.01 |  |
| 7 | A | — | 0.001 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 8 | betaflag | — | 1 | 0 | 2 | 0 | 2 | 0.01 | frozen by default |
| 9 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("compmag")
# component: m.compmag  (params as attributes)
```
