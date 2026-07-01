---
name: vashift
type: con  # convolution
func: C_vashift
n_params: 1
family: [vashift]
energy_range: [0.0, 1.0e20]
source: manager/model.dat + XSmodelVashift.tex
---

# vashift

**convolution model** (`con`), function `C_vashift`.

## Description

This convolution model velocity shifts an additive model. It takes the calculated 
model and shifts energies $-Ev/c$.

The `energies` command must be to used to extend the energy 
range over which the model.

The parameter is:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Velocity | km/s | 0 | -10000 | 10000 | -10000 | 10000 | 10 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("vashift*powerlaw")
# component: m.vashift  (params as attributes)
```
