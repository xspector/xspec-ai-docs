---
name: lorentz
type: add  # additive
func: C_lorentzianLine
n_params: 3
family: [lorentz, zlorentz]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelLorentz.tex
---

# lorentz

**additive model** (`add`), function `C_lorentzianLine`.

Variants documented together: `lorentz`, `zlorentz`.

## Description

A Lorentzian line profile.

$$A(E) = K{\sigma\over{(\pi-2\arctan(-2E_L/\sigma))}}{1\over{(E-E_L)^2 + (\sigma/2)^2}}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 6.5 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Width | keV | 0.1 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("lorentz")
# component: m.lorentz  (params as attributes)
```
