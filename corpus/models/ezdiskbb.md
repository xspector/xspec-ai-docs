---
name: ezdiskbb
type: add  # additive
func: ezdiskbb
n_params: 2
family: [ezdiskbb]
energy_range: [0.01, 100.0]
source: manager/model.dat + XSmodelEzdiskbb.tex
---

# ezdiskbb

**additive model** (`add`), function `ezdiskbb`.

## Description

A multi-temperature blackbody model for a thin, steady-state,
Newtonian accretion disk, assuming zero torque at the inner boundary
for the disk at radius $R_{in}$. The temperature of the disk as a function
of radius is assumed to be $T(r) = T_* r^{-3/4} (1-r^{-1/2})^{1/4}$,
where $r = R/R_{in}$ and $T_* = f(3GM\dot{M}/8\pi
R_{in}^3\sigma)^{1/4}$. The maximum temperature in the disk is given 
by $T_{max} = 0.488 T_*$.

This model is an alternative to `diskbb`, which assumes a non-zero
torque at the inner edge and a temperature profile $T(r) = T_*
r^{-3/4}$, and it should be used to fit spectra of disks when the
zero-torque inner boundary condition is appropriate. For details see
[Zimmerman et al. (2005)](https://ui.adsabs.harvard.edu/abs/2005ApJ...618..832Z/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | T_max | keV | 1 | 0.01 | 100 | 0.01 | 100 | 0.01 |  |
| 2 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("ezdiskbb")
# component: m.ezdiskbb  (params as attributes)
```
