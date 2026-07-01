---
name: cemekl
type: add  # additive
func: C_cemMekal
n_params: 7
family: [cemekl, cevmkl]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCemekl.tex
---

# cemekl

**additive model** (`add`), function `C_cemMekal`.

Variants documented together: `cemekl`, `cevmkl`.

## Description

For `cemekl` see `cempow`. 

For `cevmkl` see `vcempow`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | alpha | — | 1 | 0.01 | 10 | 0.01 | 20 | 0.01 | frozen by default |
| 2 | Tmax | keV | 1 | 0.02725 | 100 | 0.02725 | 100 | 0.01 |  |
| 3 | nH | cm^-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 4 | abundanc | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 7 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("cemekl")
# component: m.cemekl  (params as attributes)
```
