---
name: zvphabs
type: mul  # multiplicative
func: xszvph
n_params: 19
family: [phabs, vphabs, zphabs, zvphabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPhabs.tex
---

# zvphabs

**multiplicative model** (`mul`), function `xszvph`.

Variants documented together: `phabs`, `vphabs`, `zphabs`, `zvphabs`.

## Description

A photoelectric absorption using cross-sections set by the `xsect` 
command. The relative abundances are set by the `abund` command.

$$M(E)=\exp[-\eta_H\sigma(E)]$$

where $\sigma(E)$ is the photo-electric cross-section (NOT including 
Thomson scattering). Note that the default He cross-section changed in v11. 
The old version can be recovered using the command

```
XSPEC>xsect obcm
```

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 3 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | Cl | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Cr | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | Co | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 18 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 19 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zvphabs*powerlaw")
# component: m.zvphabs  (params as attributes)
```
