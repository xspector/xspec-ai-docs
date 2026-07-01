---
name: zvoigtabs
type: mul  # multiplicative
func: C_zvoigtAbsorptionLine
n_params: 5
family: [voigtabs, zvoigtabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVoigtabs.tex
---

# zvoigtabs

**multiplicative model** (`mul`), function `C_zvoigtAbsorptionLine`.

Variants documented together: `voigtabs`, `zvoigtabs`.

## Description

A voigt absorption line as a multiplicative model. The zvoigtabs
variant includes redshift as a parameter.

$$M(E) = exp(-d*v(E))$$

where $v(E)$ is the voigt line shape:

$$v(E) = Re[w(z)] / (\sigma\sqrt{(2\pi)})$$

where $w(z) = exp(-z^2) erfc(-iz)$ is the Faddeeva function, and
$z = (E-E_l + i\gamma/2)/(\sqrt{2}\sigma)$

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | km/s | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Sigma | keV | 0.01 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | Width | keV | 0.01 | 0 | 10 | 0 | 20 | 0.05 |  |
| 4 | Strength | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zvoigtabs*powerlaw")
# component: m.zvoigtabs  (params as attributes)
```
