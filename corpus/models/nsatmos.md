---
name: nsatmos
type: add  # additive
func: nsatmos
n_params: 5
family: [nsatmos]
energy_range: [.05, 10.]
source: manager/model.dat + XSmodelNsatmos.tex
---

# nsatmos

**additive model** (`add`), function `nsatmos`.

## Description

This model interpolates from a grid of NS atmosphere calculations
provided by George Rybicki and Ramesh Narayan to output a NS
atmosphere spectrum. The model grids cover a wide range of surface
gravity and effective temperature, and incorporate thermal electron
conduction and self-irradiation by photons from the compact
object. This code assumes negligible (less than $10^9$ G) magnetic
fields and a pure hydrogen atmosphere. A detailed description of the
model is given in [Heinke et al. (2006)](https://ui.adsabs.harvard.edu/abs/2006ApJ...644.1090H/abstract) (see also
[McClintock et al. 2004](https://ui.adsabs.harvard.edu/abs/2004ApJ...615..402M/abstract)).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LogT_eff | K | 6 | 5 | 6.5 | 5 | 6.5 | 0.01 |  |
| 2 | M_ns | Msun | 1.4 | 0.5 | 3 | 0.5 | 3 | 0.1 |  |
| 3 | R_ns | km | 10 | 5 | 30 | 5 | 30 | 0.1 |  |
| 4 | dist | kpc | 10 | 0.1 | 100 | 0.1 | 100 | 0.1 |  |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nsatmos")
# component: m.nsatmos  (params as attributes)
```
