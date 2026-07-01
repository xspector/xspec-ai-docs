---
name: vbremss
type: add  # additive
func: xsbrmv
n_params: 3
family: [bremss, vbremss, zbremss]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelBremss.tex
---

# vbremss

**additive model** (`add`), function `xsbrmv`.

Variants documented together: `bremss`, `vbremss`, `zbremss`.

## Description

A thermal bremsstrahlung spectrum based on the [Kellogg, Baldwin & Koch
(1975, ApJ 199,
  299)](https://ui.adsabs.harvard.edu/abs/1975ApJ...199..299K/abstract)
polynomial fits to the [Karzas & Latter (1961, ApJS 6, 167)](https://ui.adsabs.harvard.edu/abs/1961ApJS....6..167K/abstract)
numerical values. A routine from Kurucz (private communication) is
used at the low temperature end. The He abundance is assumed to be 8.5
% of H by number.

The `zbremss` variant includes a choice of redshift and
`vbremss` allows the H to He abundance ratio to be varied.

For `bremss`:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 3 | 0.01 | 100 | 0.0001 | 200 | 0.01 |  |
| 2 | HeovrH | — | 1 | 0 | 100 | 0 | 100 | 0.01 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vbremss")
# component: m.vbremss  (params as attributes)
```
