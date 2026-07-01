---
name: rsvapec
type: add  # additive
func: C_rsvapec
n_params: 18
family: [rsapec, rsvapec, rsvvapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRsapec.tex
---

# rsvapec

**additive model** (`add`), function `C_rsvapec`.

Variants documented together: `rsapec`, `rsvapec`, `rsvvapec`.

## Description

An emission spectrum from collisionally-ionized diffuse gas calculated
from the AtomDB atomic database (http://atomdb.org/) modified by
resonance scattering out of the beam following
[Chakraborty et al. (2023)](https://ui.adsabs.harvard.edu/abs/2023ApJ...959..126C/abstract).
This assumes an isothermal plasma and that there is no significant
scattering into the beam. The free parameter for the resonance
scattering is the column in units of 10$^{22}$ cm$^{-2}$. This model
also includes a velocity broadening parameter and includes thermal
broadening of all lines. The calculated line shape includes the
different resonance scattering correction between the core and the
wings. For large columns this can produce a double-peaked structure.

See the `apec` model for information about the additional options
available.

For the `rsapec` model the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 6.5 | 0.0808 | 68.447 | 0.0808 | 68.447 | 0.01 |  |
| 2 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 3 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 16 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 17 | RScolumn | 10^22 | 0 | 0 | 10000 | 0 | 10000 | 1 | frozen by default |
| 18 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("rsvapec")
# component: m.rsvapec  (params as attributes)
```
