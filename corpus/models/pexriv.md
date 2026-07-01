---
name: pexriv
type: add  # additive
func: C_xspexriv
n_params: 10
family: [pexriv]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelPexriv.tex
---

# pexriv

**additive model** (`add`), function `C_xspexriv`.

## Description

Exponentially cut off power law spectrum reflected from ionized
material ([Magdziarz & Zdziarski 1995](https://ui.adsabs.harvard.edu/abs/1995MNRAS.273..837M/abstract)). Ionization
and opacities of the reflecting medium is computed as in the `absori`
model. The output spectrum is the sum of the cut-off power law and the
reflection component. The reflection component alone can be obtained
for $rel_{refl} < 0$. Then the actual reflection normalization is
$|rel_{refl}|$. Note that you need to then change the limits of
$rel_{refl}$ to exclude zero (as then the direct component
appears). If $E_c$ = 0 there is no cutoff in the power law. The metal
and iron abundance are variable with respect to those defined by the
command `abund`.

The core of this model is a Greens' function integration with one
numerical integral performed for each model energy. The numerical
integration is done using an adaptive method which continues until a
given estimated fractional precision is reached. The precision can be
changed by setting PEXRIV_PRECISION eg `xset` **PEXRIV_PRECISION
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
| 8 | T_disk | K | 30000 | 10000 | 1000000 | 10000 | 1000000 | 1000 | frozen by default |
| 9 | xi | erg cm/s | 1 | 0 | 1000 | 0 | 5000 | 0.1 |  |
| 10 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("pexriv")
# component: m.pexriv  (params as attributes)
```
