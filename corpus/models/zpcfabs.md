---
name: zpcfabs
type: mul  # multiplicative
func: xszabp
n_params: 3
family: [pcfabs, zpcfabs]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelPcfabs.tex
---

# zpcfabs

**multiplicative model** (`mul`), function `xszabp`.

Variants documented together: `pcfabs`, `zpcfabs`.

## Description

A partial covering fraction absorption. The relative abundances are set by 
the `abund` command.

$$M(E) = f \exp[-\eta_H \sigma(E)] + (1-f)$$

where $\sigma(E)$ is the photo-electric cross-section (NOT including Thomson 
scattering) (see `phabs`) and:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | CvrFract | — | 0.5 | 0.05 | 0.95 | 0 | 1 | 0.01 |  |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zpcfabs*powerlaw")
# component: m.zpcfabs  (params as attributes)
```
