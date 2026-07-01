---
name: btapec
type: add  # additive
func: C_btapec
n_params: 6
family: [btapec, bvtapec, bvvtapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelBtapec.tex
---

# btapec

**additive model** (`add`), function `C_btapec`.

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
| 1 | kT | keV | 1 | 0.008 | 64 | 0.008 | 64 | 0.01 |  |
| 2 | kTi | keV | 1 | 0.008 | 64 | 0.008 | 64 | 0.01 |  |
| 3 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.001 | frozen by default |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("btapec")
# component: m.btapec  (params as attributes)
```
