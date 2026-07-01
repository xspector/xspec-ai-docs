---
name: nteea
type: add  # additive
func: C_xsnteea
n_params: 16
family: [nteea]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelNteea.tex
---

# nteea

**additive model** (`add`), function `C_xsnteea`.

## Description

A nonthermal pair plasma model based on that of [Lightman & Zdziarski
(1987)](https://ui.adsabs.harvard.edu/abs/1987ApJ...319..643L/abstract) from Magdziarz and Zdziarski. It includes
angle-dependent reflection from [Magdziarz & Zdziarski (1995)](https://ui.adsabs.harvard.edu/abs/1995MNRAS.273..837M/abstract).  In versions 1.1 and above the Compton reflection is done
through an internal call to the `reflect` model. The Greens' function
integration required for the Compton reflection calculation is
performed to an accuracy of 0.01 (i.e. 1%). This can be changed using
e.g. `xset` **NTEEA_PRECISION 0.05**.The abundances are set up by the
command `abund`. Send questions or comments to [aaz@camk.edu.pl](mailto:aaz@camk.edu.pl)

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | l_nth | — | 100 | 0 | 10000 | 0 | 10000 | 10 |  |
| 2 | l_bb | — | 100 | 0 | 10000 | 0 | 10000 | 10 |  |
| 3 | f_refl | — | 0 | 0 | 4 | 0 | 4 | 0.1 |  |
| 4 | kT_bb | — | 10 | 1 | 100 | 1 | 100 | 1 | frozen by default |
| 5 | g_max | — | 1000 | 5 | 10000 | 5 | 10000 | 10 | frozen by default |
| 6 | l_th | — | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 7 | tau_p | — | 0 | 0 | 10 | 0 | 10 | 0.2 | frozen by default |
| 8 | G_inj | — | 0 | 0 | 5 | 0 | 5 | 0.1 | frozen by default |
| 9 | g_min | — | 1.3 | 1 | 1000 | 1 | 1000 | 1 | frozen by default |
| 10 | g_0 | — | 1.3 | 1 | 5 | 1 | 5 | 0.5 | frozen by default |
| 11 | radius | — | 10000000000000 | 100000 | 1e+16 | 100000 | 1e+16 | 100000 | frozen by default |
| 12 | pair_esc | — | 0 | 0 | 1 | 0 | 1 | 0.1 | frozen by default |
| 13 | cosIncl | — | 0.45 | 0.05 | 0.95 | 0.05 | 0.95 | 0.01 |  |
| 14 | Fe_abund | — | 1 | 0.1 | 10 | 0.1 | 10 | 0.01 | frozen by default |
| 15 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 16 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nteea")
# component: m.nteea  (params as attributes)
```
