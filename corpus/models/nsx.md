---
name: nsx
type: add  # additive
func: C_nsx
n_params: 6
family: [nsx]
energy_range: [0.05, 10.0]
source: manager/model.dat + XSmodelNsx.tex
---

# nsx

**additive model** (`add`), function `C_nsx`.

## Description

The `nsx` model interpolates from a grid of neutron star (NS) atmosphere
spectra to produce a final spectrum that depends on the parameters
listed below. Atmosphere spectra are obtained using opacity tables
computed by The Opacity Project and are for non-magnetic atmospheres
(note that `nsx` is fully compatible with the magnetic atmosphere
spectral tables of `nsmaxg`, and both `nsx` and `nsmaxg` spectral tables can
easily be made compatible with other XSPEC NS fitting
models). Atmosphere models are constructed by solving the radiative
transfer equation, and the atmosphere is assumed to be in radiative
and hydrostatic equilibrium. Atmosphere models depend on the surface
effective temperature $T_{eff}$ and surface gravity $g = (1+z_g)GM/R^2$, where
$1 + z_g = \sqrt{1-2GM/R}$ is the gravitational redshift and $M$ and $R$ are the
NS mass and radius, respectively. The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | logTeff | K | 6 | 5.5 | 6.7 | 5.5 | 6.7 | 0.01 |  |
| 2 | M_ns | Msun | 1.4 | 0.5 | 3 | 0.5 | 3 | 0.1 |  |
| 3 | R_ns | km | 10 | 5 | 30 | 5 | 30 | 0.1 |  |
| 4 | dist | kpc | 1 | 0.01 | 100 | 0.01 | 100 | 0.1 |  |
| 5 | specfile | — | 6 |  |  |  |  |  | switch (not fitted) |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nsx")
# component: m.nsx  (params as attributes)
```
