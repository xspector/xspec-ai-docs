---
name: absori
type: mul  # multiplicative
func: C_xsabsori
n_params: 6
family: [absori]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelAbsori.tex
---

# absori

**multiplicative model** (`mul`), function `C_xsabsori`.

## Description

An ionized absorber based on that of [Done et al. (1992,
ApJ 395, 275)](https://ui.adsabs.harvard.edu/abs/1992ApJ...395..275D/abstract)
and developed by [Magdziarz & Zdziarski (1995, MNRAS 273,
  837)](https://ui.adsabs.harvard.edu/abs/1995MNRAS.273..837M/abstract). See
also [Zdziarski et al. (1995, ApJ 438,
  L63)](https://ui.adsabs.harvard.edu/abs/1995ApJ...438L..63Z/abstract). Photoionization
rates are from [Reilman & Manson (1979, ApJS 40, 815)](https://ui.adsabs.harvard.edu/abs/1979ApJS...40..815R/abstract), who
employ the Hartree-Slater approximation (accurate to about 5%), and
recombination rates are from [Shull & van Steenberg (1982, ApJS
  48, 95)](https://ui.adsabs.harvard.edu/abs/1982ApJS...48...95S/abstract). The cross sections are extrapolated with $E^{-3}$ above 5
keV. The abundances are set up by the command abund. Send questions or
comments to **[aaz@camk.edu.pl](mailto:aaz@camk.edu.pl)**

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndex | — | 2 | 0 | 4 | 0 | 4 | 0.05 | frozen by default |
| 2 | nH | 10^22 | 1 | 0 | 100 | 0 | 100 | 0.01 |  |
| 3 | Temp_abs | K | 30000 | 10000 | 1000000 | 10000 | 1000000 | 1000 | frozen by default |
| 4 | xi | — | 1 | 0 | 1000 | 0 | 5000 | 0.1 |  |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | Fe_abund | — | 1 | 0 | 1000000 | 0 | 1000000 | 0.02 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("absori*powerlaw")
# component: m.absori  (params as attributes)
```
