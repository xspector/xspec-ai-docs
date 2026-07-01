---
name: dust
type: mul  # multiplicative
func: xsdust
n_params: 2
family: [dust]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelDust.tex
---

# dust

**multiplicative model** (`mul`), function `xsdust`.

## Description

A modification of a spectrum due to scattering off dust on the line-of-sight. 
The model assumes that the scattered flux goes into a uniform disk whose 
size has a 1/E dependence and whose total flux has a 1/E$^2$ dependence.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Frac | — | 0.066 | 0 | 1 | 0 | 1 | 0.001 | frozen by default |
| 2 | Halosz | — | 2 | 0 | 100000 | 0 | 100000 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("dust*powerlaw")
# component: m.dust  (params as attributes)
```
