---
name: spexpcut
type: mul  # multiplicative
func: C_superExpCutoff
n_params: 2
family: [spexpcut]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelSpexpcut.tex
---

# spexpcut

**multiplicative model** (`mul`), function `C_superExpCutoff`.

## Description

A high-energy super-exponential roll-off.

$$M(E) = \exp\left(-(E/E_c)^\alpha\right)$$

useful for fitting gamma-ray spectra of pulsars (see eg [Nel & de Jager 1995](https://ui.adsabs.harvard.edu/abs/1995Ap%26SS.230..299N/abstract)), 
where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Ecut | keV | 10 | 0 | 1000000 | 0 | 1000000 | 0.1 |  |
| 2 | alpha | — | 1 | -5 | 5 | -5 | 5 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("spexpcut*powerlaw")
# component: m.spexpcut  (params as attributes)
```
