---
name: zvoigt
type: add  # additive
func: C_zvoigtLine
n_params: 5
family: [voigt, zvoigt]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVoigt.tex
---

# zvoigt

**additive model** (`add`), function `C_zvoigtLine`.

Variants documented together: `voigt`, `zvoigt`.

## Description

A Voigt line profile. The Voigt profile is the convolution of a Gaussian and
a Lorentzian. It can be written as:

$$A(E) = K Re[w(z)] / (\sigma\sqrt{(2\pi)})$$

where $w(z) = exp(-z^2) erfc(-iz)$ is the Faddeeva function, and
$z = (E-E_l + i\gamma/2)/(\sqrt{2}\sigma)$

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 6.5 | 0 | 1000000 | 0 | 1000000 | 0.01 |  |
| 2 | Sigma | keV | 0.01 | 0 | 10 | 0 | 20 | 0.005 |  |
| 3 | Gamma | keV | 0.01 | 0 | 10 | 0 | 20 | 0.005 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zvoigt")
# component: m.zvoigt  (params as attributes)
```
