---
name: pexrav
type: add  # additive
func: C_xspexrav
n_params: 8
family: [pexrav]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelPexrav.tex
---

# pexrav

**additive model** (`add`), function `C_xspexrav`.

## Description

Exponentially cut off power law spectrum reflected from neutral
material ([Magdziarz & Zdziarski 1995](https://ui.adsabs.harvard.edu/abs/1995MNRAS.273..837M/abstract)). The output
spectrum is the sum of the cut-off power law and the reflection
component. The reflection component alone can be obtained for
$rel_{refl} < 0$. Then the actual reflection normalization is
$|rel_{refl}|$. Note that you need to then change the limits of
$rel_{refl}$ to exclude zero (as then the direct component
appears). If $E_c$ = 0 there is no cutoff in the power law. The metal
and iron abundance are variable with respect to those defined by the
command `abund`. The opacities are those set by the command
`xsect`. As expected in AGNs, H and He are assumed to be fully
ionized

The core of this model is a Greens' function integration with one
numerical integral performed for each model energy. The numerical
integration is done using an adaptive method which continues until a
given estimated fractional precision is reached. The precision can be
changed by setting PEXRAV_PRECISION eg `xset` **PEXRAV_PRECISION
  0.05**. The default precision is 0.01 (ie 1%).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndex | — | 2 | -9 | 9 | -10 | 10 | 0.01 |  |
| 2 | foldE | keV | 100 | 1 | 1000000 | 1 | 1000000 | 10 |  |
| 3 | rel_refl | — | 0 | 0 | 1000000 | 0 | 1000000 | 0.01 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | abund | — | 1 | 0 | 1000000 | 0 | 1000000 | 0.01 | frozen by default |
| 6 | Fe_abund | — | 1 | 0 | 1000000 | 0 | 1000000 | 0.01 | frozen by default |
| 7 | cosIncl | — | 0.45 | 0.05 | 0.95 | 0.05 | 0.95 | 0.01 | frozen by default |
| 8 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("pexrav")
# component: m.pexrav  (params as attributes)
```
