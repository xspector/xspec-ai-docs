---
name: zashift
type: con  # convolution
func: C_zashift
n_params: 1
family: [zashift]
energy_range: [0.0, 1.0e20]
source: manager/model.dat + XSmodelZashift.tex
---

# zashift

**convolution model** (`con`), function `C_zashift`.

## Description

This convolution model redshifts an additive model. It takes the calculated 
model and shifts energies by 1/(1+z) then applies an additional 
1/(1+z) factor to the model values.

The `energies` command must be to used to extend the maximum energy 
over which the model is being calculated to (1+z) times the maximum energy 
in the response.

The parameter is:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zashift*powerlaw")
# component: m.zashift  (params as attributes)
```
