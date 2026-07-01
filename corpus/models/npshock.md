---
name: npshock
type: add  # additive
func: C_npshock
n_params: 7
family: [npshock, vnpshock, vvnpshock, bnpshock, bvnpshock, bvvnpshock]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelNpshock.tex
---

# npshock

**additive model** (`add`), function `C_npshock`.

Variants documented together: `npshock`, `vnpshock`, `vvnpshock`, `bnpshock`, `bvnpshock`, `bvvnpshock`.

## Description

Plane-parallel shock plasma model with separate ion and electron
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
| 3 | Abundanc | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 4 | Tau_l | s/cm^3 | 0 | 0 | 50000000000000 | 0 | 50000000000000 | 100000000 | frozen by default |
| 5 | Tau_u | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 6 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 7 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("npshock")
# component: m.npshock  (params as attributes)
```
