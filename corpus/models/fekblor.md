---
name: fekblor
type: add  # additive
func: C_FeKbetafromFourLorentzians
n_params: 1
family: [fekblor, zfekblor, bfekblor, zbfekblor]
energy_range: [0.01, 1.e6]
source: manager/model.dat + XSmodelFekblor.tex
---

# fekblor

**additive model** (`add`), function `C_FeKbetafromFourLorentzians`.

Variants documented together: `fekblor`, `zfekblor`, `bfekblor`, `zbfekblor`.

## Description

A four Lorentzian approximation to the line profile of Fe K$\beta$
from neutral material. The energies, widths, and
relative amplitudes for the Lorentzians are taken from
[Holzer et al (1997)](https://ui.adsabs.harvard.edu/abs/1997PhRvA..56.4554H/abstract) and
are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("fekblor")
# component: m.fekblor  (params as attributes)
```
