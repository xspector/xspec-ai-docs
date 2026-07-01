---
name: compbb
type: add  # additive
func: compbb
n_params: 4
family: [compbb]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelCompbb.tex
---

# compbb

**additive model** (`add`), function `compbb`.

## Description

Comptonized blackbody model by [Nishimura, Mitsuda and Itoh
  (1986, PASJ 38, 819)](https://ui.adsabs.harvard.edu/abs/1986PASJ...38..819N/abstract). The electron temperature should normally be kept fixed
since the Compton $y$ parameter is the product of the electron
temperature and optical depth.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.01 | 100 | 0.0001 | 200 | 0.01 |  |
| 2 | kTe | keV | 50 | 1 | 200 | 1 | 200 | 1 | frozen by default |
| 3 | tau | — | 0.1 | 0 | 10 | 0 | 10 | 0.001 |  |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("compbb")
# component: m.compbb  (params as attributes)
```
