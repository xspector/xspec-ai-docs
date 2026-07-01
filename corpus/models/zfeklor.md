---
name: zfeklor
type: add  # additive
func: C_zFeKfromSevenLorentzians
n_params: 2
family: [feklor, zfeklor, bfeklor, zbfeklor]
energy_range: [0.01, 1.e6]
source: manager/model.dat + XSmodelFeklor.tex
---

# zfeklor

**additive model** (`add`), function `C_zFeKfromSevenLorentzians`.

Variants documented together: `feklor`, `zfeklor`, `bfeklor`, `zbfeklor`.

## Description

A seven Lorentzian approximation to the line profile of Fe K$\alpha$
from neutral material. The energies, widths, and
relative amplitudes for the Lorentzians are taken from
[Holzer et al (1997)](https://ui.adsabs.harvard.edu/abs/1997PhRvA..56.4554H/abstract) and
are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 2 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zfeklor")
# component: m.zfeklor  (params as attributes)
```
