---
name: phabs
type: mul  # multiplicative
func: xsphab
n_params: 1
family: [phabs, vphabs, zphabs, zvphabs]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelPhabs.tex
---

# phabs

**multiplicative model** (`mul`), function `xsphab`.

Variants documented together: `phabs`, `vphabs`, `zphabs`, `zvphabs`.

## Description

A photoelectric absorption using cross-sections set by the `xsect` 
command. The relative abundances are set by the `abund` command.

$$M(E)=\exp[-\eta_H\sigma(E)]$$

where $\sigma(E)$ is the photo-electric cross-section (NOT including 
Thomson scattering). Note that the default He cross-section changed in v11. 
The old version can be recovered using the command

```
XSPEC12>xsect obcm
```

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |

## PyXspec

```python
from xspec import Model
m = Model("phabs*powerlaw")
# component: m.phabs  (params as attributes)
```
