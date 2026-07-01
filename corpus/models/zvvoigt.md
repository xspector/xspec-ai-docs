---
name: zvvoigt
type: add  # additive
func: C_zvvoigtLine
n_params: 5
family: [vvoigt, zvvoigt]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVvoigt.tex
---

# zvvoigt

**additive model** (`add`), function `C_zvvoigtLine`.

Variants documented together: `vvoigt`, `zvvoigt`.

## Description

A Voigt line profile with both $\sigma$ and $\gamma$ in km/s. The
Voigt profile is the convolution of a Gaussian and a Lorentzian. It can be written as:

$$A(E) = K Re[w(z)] / (\sigma(E_l/c)\sqrt{(2\pi)})$$

where $w(z) = exp(-z^2) erfc(-iz)$ is the Faddeeva function, and
$z = (E-E_l + i\gamma(E_l/c)/2)/(\sqrt{2}\sigma(E_l/c))$

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 6.5 | 0 | 1000000 | 0 | 1000000 | 0.01 |  |
| 2 | Sigma | km/s | 100 | 0 | 10 | 0 | 20 | 0.005 |  |
| 3 | Gamma | km/s | 100 | 0 | 10 | 0 | 20 | 0.005 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zvvoigt")
# component: m.zvvoigt  (params as attributes)
```
