---
name: bvvcie
type: add  # additive
func: C_bvvcie
n_params: 35
family: [cie, vcie, vvcie, bcie, bvcie, bvvcie]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCie.tex
---

# bvvcie

**additive model** (`add`), function `C_bvvcie`.

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
| 1 | kT | keV | 6.5 | 0.0808 | 68.447 | 0.0808 | 68.447 | 0.01 |  |
| 2 | H | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 3 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | Li | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | Be | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | B | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | F | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | P | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 18 | Cl | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 19 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 20 | K | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 21 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 22 | Sc | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 23 | Ti | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 24 | V | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 25 | Cr | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 26 | Mn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 27 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 28 | Co | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 29 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 30 | Cu | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 31 | Zn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 32 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 33 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 34 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 35 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bvvcie")
# component: m.bvvcie  (params as attributes)
```
