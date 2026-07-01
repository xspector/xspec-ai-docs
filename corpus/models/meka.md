---
name: meka
type: add  # additive
func: C_meka
n_params: 5
family: [meka, vmeka]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelMeka.tex
---

# meka

**additive model** (`add`), function `C_meka`.

Variants documented together: `meka`, `vmeka`.

## Description

An emission spectrum from hot diffuse gas based on the model
calculations of Mewe and Gronenschild (as amended by Kaastra). The
model includes line emissions from several elements. Abundances are
the number of nuclei per Hydrogen nucleus relative to the Solar
abundances set by the `abund` command.

For the `meka` model the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.001 | 100 | 0.001 | 100 | 0.01 |  |
| 2 | nH | cm-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 3 | Abundanc | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("meka")
# component: m.meka  (params as attributes)
```
