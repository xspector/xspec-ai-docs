---
name: rsvrnei
type: add  # additive
func: C_rsvrnei
n_params: 20
family: [rsrnei, rsvrnei, rsvvrnei]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRsrnei.tex
---

# rsvrnei

**additive model** (`add`), function `C_rsvrnei`.

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
| 3 | H | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 4 | He | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 5 | C | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 6 | N | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 7 | O | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 8 | Ne | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 9 | Mg | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 10 | Si | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 11 | S | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 12 | Ar | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 13 | Ca | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 14 | Fe | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 15 | Ni | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 16 | Tau | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 17 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 18 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 19 | RScolumn | 10^22 | 0 | 0 | 10000 | 0 | 10000 | 1 | frozen by default |
| 20 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("rsvrnei")
# component: m.rsvrnei  (params as attributes)
```
