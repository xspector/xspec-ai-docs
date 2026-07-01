---
name: vapec
type: add  # additive
func: C_vapec
n_params: 16
family: [apec, vapec, vvapec, bapec, bvapec, bvvapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelApec.tex
---

# vapec

**additive model** (`add`), function `C_vapec`.

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
| 16 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vapec")
# component: m.vapec  (params as attributes)
```
