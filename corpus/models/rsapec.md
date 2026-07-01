---
name: rsapec
type: add  # additive
func: C_rsapec
n_params: 6
family: [rsapec, rsvapec, rsvvapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRsapec.tex
---

# rsapec

**additive model** (`add`), function `C_rsapec`.

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
| 1 | kT | keV | 1 | 0.008 | 64 | 0.008 | 64 | 0.01 |  |
| 2 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.001 | frozen by default |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 5 | RScolumn | 10^22 | 0 | 0 | 10000 | 0 | 10000 | 1 | frozen by default |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("rsapec")
# component: m.rsapec  (params as attributes)
```
