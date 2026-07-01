---
name: zwndabs
type: mul  # multiplicative
func: xszwnb
n_params: 3
family: [wndabs, zwndabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelWndabs.tex
---

# zwndabs

**multiplicative model** (`mul`), function `xszwnb`.

Variants documented together: `wndabs`, `zwndabs`.

## Description

Photo-electric absorption from approximation to a warm absorber using 
[Balucinska-Church & McCammon (1992)](https://ui.adsabs.harvard.edu/abs/1992ApJ...400..699B/abstract) cross-sections. Relative 
abundances are set by the `abund` command.

$$M(E) = \begin{array}{ll}
        1 & E > E_w \rowsp
        \exp[-\eta_H\sigma(E)] & E \leq E_w
       \end{array}$$

where $\sigma(E)$ is the photo-electric cross-section (NOT including
Thomson scattering) and

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 10 | 0 | 20 | 0.05 |  |
| 2 | WindowE | keV | 1 | 0.05 | 20 | 0.03 | 20 | 0.05 |  |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zwndabs*powerlaw")
# component: m.zwndabs  (params as attributes)
```
