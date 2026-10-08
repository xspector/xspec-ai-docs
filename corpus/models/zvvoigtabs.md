---
name: zvvoigtabs
type: mul  # multiplicative
func: C_zvvoigtAbsorptionLine
n_params: 5
family: [vvoigtabs, zvvoigtabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVvoigtabs.tex
---

# zvvoigtabs

**multiplicative model** (`mul`), function `C_zvvoigtAbsorptionLine`.

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
| 1 | LineE | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Sigma | km/s | 100 | 0 | 300000 | 0 | 300000 | 0.05 |  |
| 3 | Width | km/s | 100 | 0 | 300000 | 0 | 300000 | 0.05 |  |
| 4 | Strength | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zvvoigtabs*powerlaw")
# component: m.zvvoigtabs  (params as attributes)
```
