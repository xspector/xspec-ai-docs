---
name: zwabs
type: mul  # multiplicative
func: xszabs
n_params: 2
family: [wabs, zwabs]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelWabs.tex
---

# zwabs

**multiplicative model** (`mul`), function `xszabs`.

Variants documented together: `wabs`, `zwabs`.

## Description

A photo-electric absorption using Wisconsin ([Morrison &
  McCammon 1983](https://ui.adsabs.harvard.edu/abs/1983ApJ...270..119M/abstract)) cross-sections.

$$M(E) = \exp[-\eta_H\sigma(E)]$$

where $\sigma(E)$ is the photo-electric cross-section (NOT including Thomson 
scattering). Note that this model uses the Anders & Ebihara relative 
abundances ([1982](https://ui.adsabs.harvard.edu/abs/1982GeCoA..46.2363A/abstract)) regardless of the `abund` command.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zwabs*powerlaw")
# component: m.zwabs  (params as attributes)
```
