---
name: vvoigtabs
type: mul  # multiplicative
func: C_vvoigtAbsorptionLine
n_params: 4
family: [vvoigtabs, zvvoigtabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVvoigtabs.tex
---

# vvoigtabs

**multiplicative model** (`mul`), function `C_vvoigtAbsorptionLine`.

Variants documented together: `vvoigtabs`, `zvvoigtabs`.

## Description

A voigt absorption line with line widths in km/s as a multiplicative model. The zvvoigtabs
variant includes redshift as a parameter.

$$M(E) = exp(-d*v(E))$$

where $v(E)$ is the voigt line shape (see `vvoigt` for details),
and the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | km/s | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Sigma | km/s | 100 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | Width | km/s | 100 | 0 | 10 | 0 | 20 | 0.05 |  |
| 4 | Strength | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |

## PyXspec

```python
from xspec import Model
m = Model("vvoigtabs*powerlaw")
# component: m.vvoigtabs  (params as attributes)
```
