---
name: refsch
type: add  # additive
func: xsrefsch
n_params: 14
family: [refsch]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelRefsch.tex
---

# refsch

**additive model** (`add`), function `xsrefsch`.

## Description

Exponentially cut-off power-law spectrum reflected from an ionized
relativistic accretion disk. In this model, spectrum of `pexriv` is
convolved with a relativistic disk line profile `diskline`. See
[Magdziarz & Zdziarski (1995)](https://ui.adsabs.harvard.edu/abs/1995MNRAS.273..837M/abstract) for details of Compton
reflection. See [Fabian et al. (1989)](https://ui.adsabs.harvard.edu/abs/1989MNRAS.238..729F/abstract) for details of the
disk line profile.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndex | — | 2 | -9 | 9 | -10 | 10 | 0.01 |  |
| 2 | foldE | keV | 100 | 1 | 1000000 | 1 | 1000000 | 10 |  |
| 3 | rel_refl | — | 0 | 0 | 2 | 0 | 2 | 0.01 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | abund | — | 1 | 0.5 | 10 | 0.5 | 10 | 0.01 | frozen by default |
| 6 | Fe_abund | — | 1 | 0.1 | 10 | 0.1 | 10 | 0.01 | frozen by default |
| 7 | Incl | deg | 30 | 19 | 87 | 19 | 87 | 0.05 | frozen by default |
| 8 | T_disk | K | 30000 | 10000 | 1000000 | 10000 | 1000000 | 1000 | frozen by default |
| 9 | xi | ergcm/s | 1 | 0 | 1000 | 0 | 5000 | 0.1 |  |
| 10 | Betor10 | — | -2 | -10 | 20 | -10 | 20 | 0.01 | frozen by default |
| 11 | Rin | R_g | 10 | 6 | 1000 | 6 | 10000 | 0.1 | frozen by default |
| 12 | Rout | R_g | 1000 | 0 | 1000000 | 0 | 10000000 | 1 | frozen by default |
| 13 | accuracy | — | 30 | 30 | 100000 | 30 | 100000 | 1 | frozen by default |
| 14 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("refsch")
# component: m.refsch  (params as attributes)
```
