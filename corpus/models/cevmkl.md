---
name: cevmkl
type: add  # additive
func: C_cemVMekal
n_params: 20
family: [cemekl, cevmkl]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCemekl.tex
---

# cevmkl

**additive model** (`add`), function `C_cemVMekal`.

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
| 4 | He | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 5 | C | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 6 | N | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 7 | O | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 8 | Ne | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 9 | Na | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 10 | Mg | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 11 | Al | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 12 | Si | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 13 | S | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 14 | Ar | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 15 | Ca | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 16 | Fe | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 17 | Ni | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 18 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 19 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 20 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("cevmkl")
# component: m.cevmkl  (params as attributes)
```
