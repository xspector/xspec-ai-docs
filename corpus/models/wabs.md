---
name: wabs
type: mul  # multiplicative
func: xsabsw
n_params: 1
family: [wabs, zwabs]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelWabs.tex
---

# wabs

**multiplicative model** (`mul`), function `xsabsw`.

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

## PyXspec

```python
from xspec import Model
m = Model("wabs*powerlaw")
# component: m.wabs  (params as attributes)
```
