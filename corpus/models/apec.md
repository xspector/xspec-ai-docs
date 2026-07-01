---
name: apec
type: add  # additive
func: C_apec
n_params: 4
family: [apec, vapec, vvapec, bapec, bvapec, bvvapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelApec.tex
---

# apec

**additive model** (`add`), function `C_apec`.

Variants documented together: `apec`, `vapec`, `vvapec`, `bapec`, `bvapec`, `bvvapec`.

## Description

An emission spectrum from collisionally-ionized diffuse gas calculated
from the AtomDB atomic database. More information can be found at
http://atomdb.org/ which should be consulted by anyone running this
model. This default version number can be changed by modifying the
ATOMDB_VERSION string in your `Xspec.init` file.

The behaviour of the apec model and all other models which use the
apec code can be changed using a number of options with the `xset` command.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.008 | 64 | 0.008 | 64 | 0.01 |  |
| 2 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.001 | frozen by default |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("apec")
# component: m.apec  (params as attributes)
```
