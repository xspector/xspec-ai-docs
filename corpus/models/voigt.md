---
name: voigt
type: add  # additive
func: C_voigtLine
n_params: 4
family: [voigt, zvoigt]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVoigt.tex
---

# voigt

**additive model** (`add`), function `C_voigtLine`.

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
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("voigt")
# component: m.voigt  (params as attributes)
```
