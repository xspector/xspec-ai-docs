---
name: cflow
type: add  # additive
func: C_xscflw
n_params: 6
family: [cflow]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCflow.tex
---

# cflow

**additive model** (`add`), function `C_xscflw`.

## Description

A cooling flow model after Mushotzky & Szymkowiak (Cooling Flows in 
Clusters and Galaxies, ed. Fabian, 1988). An index of zero for the 
power-law emissivity function corresponds to emission measure weighted by 
the inverse of the bolometric luminosity at that temperature. The abundance 
ratios are set by the `abund` command. Redshift is converted to 
distance using the cosmology set by the `cosmo` command.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | slope | — | 0 | -5 | 5 | -5 | 5 | 0.01 |  |
| 2 | lowT | keV | 0.1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.001 |  |
| 3 | highT | keV | 4 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.001 |  |
| 4 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.01 |  |
| 5 | redshift | — | 0.1 | 1e-10 | 10 | 1e-10 | 10 | 0.01 | frozen by default |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("cflow")
# component: m.cflow  (params as attributes)
```
