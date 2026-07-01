---
name: bvtapec
type: add  # additive
func: C_bvtapec
n_params: 18
family: [btapec, bvtapec, bvvtapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelBtapec.tex
---

# bvtapec

**additive model** (`add`), function `C_bvtapec`.

Variants documented together: `btapec`, `bvtapec`, `bvvtapec`.

## Description

A velocity- and thermally-broadened emission spectrum from
collisionally-ionized diffuse gas calculated from the AtomDB atomic
database. More information can be found at http://atomdb.org/
which should be consulted by anyone running this model. This version
of the model allows different temperatures for the continuum and
lines. This default version number can be changed by modifiying the
ATOMDB_VERSION string in your `Xspec.init` file.

See the documentation on the `apec` model for a list of the
`xset` options which can be used to change the behaviour of the
apec code.

For the `btapec` model the parameters are:

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
| 17 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 18 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bvtapec")
# component: m.bvtapec  (params as attributes)
```
