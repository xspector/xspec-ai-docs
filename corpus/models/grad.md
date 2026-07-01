---
name: grad
type: add  # additive
func: grad
n_params: 7
family: [grad]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelGrad.tex
---

# grad

**additive model** (`add`), function `grad`.

## Description

General Relativistic Accretion Disk model around a Schwarzschild black
hole. Inner radius is fixed to be 3 Schwarzschild radii, thus the
energy conversion efficiency is 0.057. See [Hanawa (1989)](https://ui.adsabs.harvard.edu/abs/1989ApJ...341..948H/abstract) and [Ebisawa, Mitsuda & Hanawa (1991)](https://ui.adsabs.harvard.edu/abs/1991ApJ...367..213E/abstract).
Several bugs were found in the old GRAD model which was included in
xspec 11.0.1ae and before.  Due to these bugs, it turned out that the
mass obtained by fitting the old GRAD model to the observation was 1.4
times over-estimated.  These bugs were fixed, and a new parameter
(par6) was added to make the distinction between the old and
new codes clear.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | D | kpc | 10 | 0 | 10000 | 0 | 10000 | 1 | frozen by default |
| 2 | i | deg | 0 | 0 | 90 | 0 | 90 | 1 | frozen by default |
| 3 | Mass | solar | 1 | 0 | 100 | 0 | 100 | 0.01 |  |
| 4 | Mdot | 1e18 | 1 | 0 | 100 | 0 | 100 | 0.01 |  |
| 5 | TclovTef | — | 1.7 | 1 | 10 | 1 | 10 | 1 | frozen by default |
| 6 | refflag | — | 1 | -1 | 1 | -1 | 1 | 1 | frozen by default |
| 7 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("grad")
# component: m.grad  (params as attributes)
```
