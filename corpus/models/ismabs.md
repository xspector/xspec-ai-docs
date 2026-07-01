---
name: ismabs
type: mul  # multiplicative
func: F_ismabs
n_params: 31
family: [ismabs]
energy_range: [0.01, 1.e6]
source: manager/model.dat + XSmodelIsmabs.tex
---

# ismabs

**multiplicative model** (`mul`), function `F_ismabs`.

## Description

This is an X-ray photoabsorption model for the interstellar medium
that takes into account both neutral and ionized species from H, He,
N, O, Ne, Mg, Si, S, Ar, Ca, Fe, Ni and Zn. This model has been
developed by Efrain Gatuzz in collaboration with Javier Garcia, Tim
Kallman, Claudio Mendoza, and Tom Gorczyca. A complete description of
the science behind the model is described in [Gatuzz et al. (2015)](https://ui.adsabs.harvard.edu/abs/2015ApJ...800...29G/abstract).

Note that the He I column density is not included as a free parameter
in the model, due to an inherent degeneracy between the relative
columns of H, He I, He II. Instead, the He I column is assumed to be
one tenth that of the H column.

The sources of the cross-sections are as follows:

- Neutral states of Si, S, Ar and Ca from [Verner et al. (1995)](https://ui.adsabs.harvard.edu/abs/1995A%26AS..109..125V/abstract)

- Singly and doubly ionized states of Si, S, Ar and Ca from [Witthoeft et al. (2009)](https://ui.adsabs.harvard.edu/abs/2009ApJS..182..127W/abstract) and [Witthoeft et al. (2011)](https://ui.adsabs.harvard.edu/abs/2011ApJS..192....7W/abstract)

- Neutral, singly and doubly ionized states of N from [Garcia et al. (2009)](https://ui.adsabs.harvard.edu/abs/2009ApJS..185..477G/abstract)

- Neutral states of O from [Gorczyca et al. (2013)](https://ui.adsabs.harvard.edu/abs/2013ApJ...779...78G/abstract)

- Singly and doubly ionized states of O from [Garcia et al. (2005)](https://ui.adsabs.harvard.edu/abs/2005ApJS..158...68G/abstract), including corrections applied by [Gatuzz et al. (2013)](https://ui.adsabs.harvard.edu/abs/2013ApJ...768...60G/abstract)

- Neutral state of Ne from [Gorczyca et al. (2000)](https://ui.adsabs.harvard.edu/abs/2000PhRvA..61b4702G/abstract)

- Singly and doubly ionized states of Ne from [Gorczyca et al. (2005)](https://ui.adsabs.harvard.edu/abs/2005AIPC..774..223G/abstract)

- For the Fe-L edge region we use the measurement of metallic iron by [Kortright & Kim (2000)](https://ui.adsabs.harvard.edu/abs/2000PhRvB..6212216K/abstract)

- Neutral, singly and doubly ionized states of Mg from [Hasoglu et al. (2014)](https://ui.adsabs.harvard.edu/abs/2014ApJS..214....8H/abstract). 

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | H | 10^22 | 0.1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | He_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 3 | C_I | 10^16 | 33.1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 4 | C_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 5 | C_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 6 | N_I | 10^16 | 8.32 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 7 | N_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 8 | N_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 9 | O_I | 10^16 | 67.6 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 10 | O_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 11 | O_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 12 | Ne_I | 10^16 | 12 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 13 | Ne_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 14 | Ne_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 15 | Mg_I | 10^16 | 3.8 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 16 | Mg_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 17 | Mg_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 18 | Si_I | 10^16 | 3.35 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 19 | Si_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 20 | Si_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 21 | S_I | 10^16 | 2.14 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 22 | S_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 23 | S_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 24 | Ar_I | 10^16 | 0.25 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 25 | Ar_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 26 | Ar_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 27 | Ca_I | 10^16 | 0.22 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 28 | Ca_II | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 29 | Ca_III | 10^16 | 0 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |
| 30 | Fe | 10^16 | 3.16 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 31 | redshift | — | 0 | 0 | 10 | -1 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("ismabs*powerlaw")
# component: m.ismabs  (params as attributes)
```
