---
name: mkcflow
type: add  # additive
func: C_xsmkcf
n_params: 6
family: [mkcflow, vmcflow]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelMkcflow.tex
---

# mkcflow

**additive model** (`add`), function `C_xsmkcf`.

Variants documented together: `mkcflow`, `vmcflow`.

## Description

For `mkcflow` see `coolflow`. 

For `vmcflow` see `vcoolflow`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | lowT | keV | 0.1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.001 |  |
| 2 | highT | keV | 4 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.001 |  |
| 3 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.01 |  |
| 4 | Redshift | — | 0.1 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("mkcflow")
# component: m.mkcflow  (params as attributes)
```
