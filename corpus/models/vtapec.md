---
name: vtapec
type: add  # additive
func: C_vtapec
n_params: 17
family: [tapec, vtapec, vvtapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelTapec.tex
---

# vtapec

**additive model** (`add`), function `C_vtapec`.

Variants documented together: `tapec`, `vtapec`, `vvtapec`.

## Description

An emission spectrum from collisionally-ionized diffuse gas calculated
from the AtomDB atomic database. More information can be found at
http://atomdb.org/ which should be consulted by anyone running this
model. This version of the model allows different temperatures for the
continuum and lines. This default version number can be changed by modifying the
ATOMDB_VERSION string in your `Xspec.init` file.

See the documentation on the `apec` model for a list of the
`xset` options which can be used to change the behaviour of the
apec code.

For the `tapec` model the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 6.5 | 0.0808 | 68.447 | 0.0808 | 68.447 | 0.01 |  |
| 2 | kTi | keV | 6.5 | 0.0808 | 68.447 | 0.0808 | 68.447 | 0.01 |  |
| 3 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 17 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vtapec")
# component: m.vtapec  (params as attributes)
```
