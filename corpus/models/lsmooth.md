---
name: lsmooth
type: con  # convolution
func: C_lsmooth
n_params: 2
family: [lsmooth]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelLsmooth.tex
---

# lsmooth

**convolution model** (`con`), function `C_lsmooth`.

## Description

Lorentzian smoothing with a variable width, which varies as the par2 power of the energy. 
The width at 6 keV is set with par1.

$$\begin{array}{ll}
dC(E) = & \frac{\Sigma(E)}{2\pi[(E-X)^2+(\Sigma(E)/2)^2]}A(X)d(X)\rowsp
\Sigma(E) = & \sigma(E/6)^\alpha
\end{array}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Sig_6keV | keV | 1 | 0 | 10 | 0 | 20 | 0.05 |  |
| 2 | Index | — | 0 | -1 | 1 | -1 | 1 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("lsmooth*powerlaw")
# component: m.lsmooth  (params as attributes)
```
