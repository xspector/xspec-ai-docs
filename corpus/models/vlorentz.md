---
name: vlorentz
type: add  # additive
func: C_vlorentzianLine
n_params: 3
family: [vlorentz, zvlorentz]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVlorentz.tex
---

# vlorentz

**additive model** (`add`), function `C_vlorentzianLine`.

Variants documented together: `vlorentz`, `zvlorentz`.

## Description

A Lorentzian line profile with the line width in km/s.

$$A(E) = K{\sigma(E_l/c)\over{(\pi-2\arctan(-2E_L/(\sigma(E_l/c))))}}{1\over{(E-E_L)^2 + (\sigma(E_l/c)/2)^2}}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 6.5 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Width | km/s | 100 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vlorentz")
# component: m.vlorentz  (params as attributes)
```
