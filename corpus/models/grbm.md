---
name: grbm
type: add  # additive
func: xsgrbm
n_params: 4
family: [grbm]
energy_range: [1.e-20, 1.e+20]
source: manager/model.dat + XSmodelGrbm.tex
---

# grbm

**additive model** (`add`), function `xsgrbm`.

## Description

A model for gamma-ray burst continuum spectra developed by [Band
et al. (1993)](https://ui.adsabs.harvard.edu/abs/1993ApJ...413..281B/abstract).

{

$$A(E)= \begin{cases}
        K(E/100.)^{\alpha_1} \exp(-E/E_c)
          & \text{if } E < E_c(\alpha_1-\alpha_2) \\
        K[(\alpha_1-\alpha_2)E_c/100]^{\alpha_1-\alpha_2}(E/100)^{\alpha_2}
        \exp(\alpha_2-\alpha_1)
          & \text{if } E > E_c(\alpha_1 - \alpha_2)
\end{cases}$$

}

where $E$ is in units of keV and the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | alpha | — | -1 | -3 | 2 | -10 | 5 | 0.01 |  |
| 2 | beta | — | -2 | -5 | 2 | -10 | 10 | 0.01 |  |
| 3 | tem | keV | 300 | 50 | 1000 | 10 | 10000 | 10 |  |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("grbm")
# component: m.grbm  (params as attributes)
```
