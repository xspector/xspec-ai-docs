---
name: vmcflow
type: add  # additive
func: C_xsvmcf
n_params: 19
family: [mkcflow, vmcflow]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelMkcflow.tex
---

# vmcflow

**additive model** (`add`), function `C_xsvmcf`.

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
| 3 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | Redshift | — | 0.1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 18 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 19 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vmcflow")
# component: m.vmcflow  (params as attributes)
```
