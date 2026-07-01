---
name: rsrnei
type: add  # additive
func: C_rsrnei
n_params: 8
family: [rsrnei, rsvrnei, rsvvrnei]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRsrnei.tex
---

# rsrnei

**additive model** (`add`), function `C_rsrnei`.

Variants documented together: `rsrnei`, `rsvrnei`, `rsvvrnei`.

## Description

A version of the `rnei` model modified by resonance scattering
out of the beam following [Chakraborty et
  al. (2023)](https://ui.adsabs.harvard.edu/abs/2023ApJ...959..126C/abstract). This assumes the entire
observed beam is described by this model and there is no significant
scattering into the beam. The free parameter for the resonance
scattering is the column in units of 10$^{22}$ cm$^{-2}$. This model
also includes a velocity broadening parameter and includes thermal
broadening of all lines. The calculated line shape includes the
different resonance scattering correction between the core and the
wings. For large columns this can produce a double-peaked structure.

See the `rnei` model for information about the additional options
available.

For the `rsrnei` model the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 0.5 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 2 | kT_init | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 3 | Abundanc | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 4 | Tau | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 7 | RScolumn | 10^22 | 0 | 0 | 10000 | 0 | 10000 | 1 | frozen by default |
| 8 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("rsrnei")
# component: m.rsrnei  (params as attributes)
```
