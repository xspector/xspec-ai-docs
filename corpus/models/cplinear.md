---
name: cplinear
type: add  # additive
func: C_cplinear
n_params: 21
family: [cplinear]
energy_range: [0., 10.]
source: manager/model.dat + XSmodelCplinear.tex
---

# cplinear

**additive model** (`add`), function `C_cplinear`.

## Description

This is a simple non-physical model for low-count background spectra,
used by fitting scripts in the ACIS Extract (AE) package. Using this
model outside the context of the AE package should be done with
extreme caution since it requires a choice on vertex energies and
number of segments. AE places the first and last vertices at the
lowest and highest energy of the background counts. Intermediate
vertices are placed at energies where a background count exists such
that each segment covers a similar number of background counts. Any
results using this model should cite [Broos et al. (2010)](https://ui.adsabs.harvard.edu/abs/2010ApJ...714.1582B/abstract).

Note that if all the rate parameters in use are thawed then the norm
parameter is degenerate and must be frozen. Freezing one of the rate
parameters will not work because if that vertex is driven to zero in
the fit then the norm will be zero and the other rate parameters
infinite.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | energy00 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 2 | energy01 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 3 | energy02 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 4 | energy03 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 5 | energy04 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 6 | energy05 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 7 | energy06 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 8 | energy07 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 9 | energy08 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 10 | energy09 | keV | -1 |  |  |  |  |  | scale (not fitted) |
| 11 | log_rate00 | — | 0 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 12 | log_rate01 | — | 1 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 13 | log_rate02 | — | 0 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 14 | log_rate03 | — | 1 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 15 | log_rate04 | — | 0 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 16 | log_rate05 | — | 1 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 17 | log_rate06 | — | 0 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 18 | log_rate07 | — | 1 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 19 | log_rate08 | — | 0 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 20 | log_rate09 | — | 1 | -19 | 19 | -20 | 20 | 0.1 | frozen by default |
| 21 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("cplinear")
# component: m.cplinear  (params as attributes)
```
