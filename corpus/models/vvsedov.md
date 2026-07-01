---
name: vvsedov
type: add  # additive
func: C_vvsedov
n_params: 35
family: [sedov, vsedov, vvsedov, bsedov, bvsedov, bvvsedov]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelSedov.tex
---

# vvsedov

**additive model** (`add`), function `C_vvsedov`.

Variants documented together: `sedov`, `vsedov`, `vvsedov`, `bsedov`, `bvsedov`, `bvvsedov`.

## Description

Sedov model model with separate ion and electron
temperatures. This model is slow. par1 provides a measure of
the average energy per particle (ions+electrons) and is constant
throughout the postshock flow in plane shock models ([Borkowski et al.,
2001](https://ui.adsabs.harvard.edu/abs/2001ApJ...548..820B/abstract)). par2 should always be less than
par1. If par2 exceeds par1 then their
interpretations are switched (ie the larger of par1 and
par2 is always the mean temperature). Additional references
can be found under the help for the `equil` model. Several
versions are available. To switch between them use the `xset` **NEIAPECROOT** command. The versions available are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT_a | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 2 | kT_b | keV | 0.5 | 0.01 | 79.9 | 0.01 | 79.9 | 0.01 |  |
| 3 | H | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | Li | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | Be | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | B | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | F | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | P | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 18 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 19 | Cl | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 20 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 21 | K | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 22 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 23 | Sc | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 24 | Ti | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 25 | V | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 26 | Cr | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 27 | Mn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 28 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 29 | Co | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 30 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 31 | Cu | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 32 | Zn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 33 | Tau | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 34 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 35 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vvsedov")
# component: m.vvsedov  (params as attributes)
```
