---
name: cie
type: add  # additive
func: C_cie
n_params: 5
family: [cie, vcie, vvcie, bcie, bvcie, bvvcie]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCie.tex
---

# cie

**additive model** (`add`), function `C_cie`.

Variants documented together: `cie`, `vcie`, `vvcie`, `bcie`, `bvcie`, `bvvcie`.

## Description

An emission spectrum from a plasma in collisional-ionizization
equilibrium. The switch parameter can be used to change the source of
the atomic physics data. Most of the values for this switch are
included for historical reasons. Only the AtomDB and SPEX options
should be used for modern data. More information can be found about
the AtomDB atomic database at http://atomdb.org/ and about SPEX
at https://spex-xray.github.io/spex-help/index.html. The default
AtomDB version number can be changed by modifying the
ATOMDB_VERSION string in your `Xspec.init` file. At the
moment the only SPEX version available is 3.07.

The behaviour of the cie model and all other models which use the
underlying code can be changed using a number of options with the `xset` command.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.008 | 64 | 0.008 | 64 | 0.01 |  |
| 2 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.001 | frozen by default |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("cie")
# component: m.cie  (params as attributes)
```
