---
name: c6mekl
type: add  # additive
func: C_c6mekl
n_params: 11
family: [c6mekl, c6vmekl, c6pmekl, c6pvmkl]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelC6mekl.tex
---

# c6mekl

**additive model** (`add`), function `C_c6mekl`.

Variants documented together: `c6mekl`, `c6vmekl`, `c6pmekl`, `c6pvmkl`.

## Description

For `c6mekl` see `cheb6`. 

For `c6vmekl` see `vcheb6`. 

For `c6pmekl` see `expcheb6`. 

For `c6pvmkl` see `vexpcheb6`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | CPcoef1 | — | 1 | -1 | 1 | -1 | 1 | 0.1 |  |
| 2 | CPcoef2 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 3 | CPcoef3 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 4 | CPcoef4 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 5 | CPcoef5 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 6 | CPcoef6 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 7 | nH | cm^-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 8 | abundanc | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 9 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 10 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 11 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("c6mekl")
# component: m.c6mekl  (params as attributes)
```
