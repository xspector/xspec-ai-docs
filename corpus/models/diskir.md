---
name: diskir
type: add  # additive
func: diskir
n_params: 9
family: [diskir]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelDiskir.tex
---

# diskir

**additive model** (`add`), function `diskir`.

## Description

The inner disk can be irradiated by the Compton tail. This can
substantially change the inner disk temperature structure from that
expected from an unilluminated disk in the limit where the ratio of
luminosity in the tail to that in the disk, $L_c/L_d >> 1$. This is
generally the case in the low/hard state of accreting black holes, and
neglecting this effect leads to an underestimate of the inner disk
radius ([Gierlinski, Done & Page 2008](https://ui.adsabs.harvard.edu/abs/2008MNRAS.388..753G/abstract)).

The irradiated inner disk and Compton tail can illuminate the rest of
the disk, and a fraction $f_{out}$ of the bolometric flux is thermalized
to the local blackbody temperature at each radius. This reprocessed
flux generally dominates the optical and UV bandpass of LMXBs
([Gierlinski, Done & Page 2009](https://ui.adsabs.harvard.edu/abs/2009MNRAS.392.1106G/abstract)).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT_disk | keV | 1 | 0.01 | 5 | 0.01 | 5 | 0.01 |  |
| 2 | Gamma | — | 1.7 | 1.001 | 5 | 1.001 | 10 | 0.01 |  |
| 3 | kT_e | keV | 100 | 5 | 1000 | 1 | 1000 | 0.1 |  |
| 4 | LcovrLd | — | 0.1 | 0 | 10 | 0 | 10 | 0.01 |  |
| 5 | fin | — | 0.1 | 0 | 1 | 0 | 1 | 1e-06 | frozen by default |
| 6 | rirr | — | 1.2 | 1.0001 | 10 | 1.0001 | 10 | 0.01 |  |
| 7 | fout | — | 0.0001 | 0 | 0.1 | 0 | 0.1 | 1e-06 |  |
| 8 | logrout | — | 5 | 3 | 7 | 3 | 7 | 0.01 |  |
| 9 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("diskir")
# component: m.diskir  (params as attributes)
```
