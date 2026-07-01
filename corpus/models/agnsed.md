---
name: agnsed
type: add  # additive
func: agnsed
n_params: 16
family: [agnsed, qsosed]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelAgnsed.tex
---

# agnsed

**additive model** (`add`), function `agnsed`.

Variants documented together: `agnsed`, `qsosed`.

## Description

A model for the spectral energy distribution (SED) of an AGN developed
by [Kubota & Done (2018; KD18)](https://ui.adsabs.harvard.edu/abs/2018MNRAS.480.1247K/abstract).
Following [Done et al. (2012)](https://ui.adsabs.harvard.edu/abs/2012MNRAS.420.1848D/abstract),
the SED model has three characteristic regions: the outer standard
disc region; the warm Comptonising region; and the inner hot
Comptonising region.

For the warm Comptonising region, this model adopts the passive disc
scenario tested by [Petrucci et al. (2018)](
https://ui.adsabs.harvard.edu/abs/2018A&A...611A..59P/abstract). Here,
the flow is assumed to be completely radially stratified, emitting as
a standard disc blackbody from Rout to Rwarm, as warm Comptonisation
from Rwarm to Rhot and then makes a transition to the hard X-ray
emitting hot Comptonisation component from Rhot to RISCO. The warm
Comptonisation component is optically thick, so is associated with
material in the disc. Nonetheless, the energy does not thermalise to
even a modified blackbody, perhaps indicating that significant
dissipation takes place within the vertical structure of the disc,
rather than being predominantly released in the midplane.

At a radius below Rhot, the energy is emitted in the hot
Comptonisation component. This has much lower optical depth, so it is
not the disc itself. In the model, the albedo is fixed at a = 0.3, and
the seed photon temperature for the hot Comptonisation component is
calculated internally. In contrast to optxagnf, this model does not
take the color temperature correction into account.

There are two versions of the model, agnsed and qsosed. agnsed is the
full model, while qsosed is a simplified version of agnsed made by
fixing some parameters at their typical values and by including
reprocessing.  For qsosed the agnsed parameters are fixed at kTe_hot =
100 keV, kTe_warm = 0.2 keV, Gamma_warm = 2.5, R_warm = 2R_hot, rout = rsg
and Htmax = 100. Also, Gamma_hot is calculated via eq.(6) in KD18 and R_hot
is calculated to satisfy Ldiss_hot = 0.02LEdd.

Parameters for agnsed:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | mass | solar | 10000000 | 1 | 10000000000 | 1 | 10000000000 | 0.1 | frozen by default |
| 2 | dist | Mpc | 100 | 0.01 | 1000000000 | 0.01 | 1000000000 | 0.01 | frozen by default |
| 3 | logmdot | — | -1 | -10 | 2 | -10 | 2 | 0.01 |  |
| 4 | astar | — | 0 | -1 | 0.998 | -1 | 0.998 | 1 | frozen by default |
| 5 | cosi | — | 0.5 | 0.05 | 1 | 0.05 | 1 | 1 | frozen by default |
| 6 | kTe_hot | keV(_pl) | 100 | 10 | 300 | 10 | 300 | 1 | frozen by default |
| 7 | kTe_warm | keV(_sc) | 0.2 | 0.1 | 0.5 | 0.1 | 0.5 | 0.01 |  |
| 8 | Gamma_hot | (_calc) | 1.7 | 1.3 | 3 | 1.3 | 3 | 0.01 |  |
| 9 | Gamma_warm | (_disk) | 2.7 | 2 | 5 | 2 | 10 | 0.01 |  |
| 10 | R_hot | Rg | 10 | 6 | 500 | 6 | 500 | 0.01 |  |
| 11 | R_warm | Rg | 20 | 6 | 500 | 6 | 500 | 0.1 |  |
| 12 | logrout | (_selfg) | -1 | -3 | 7 | -3 | 7 | 0.01 | frozen by default |
| 13 | Htmax | Rg | 10 | 6 | 10 | 6 | 10 | 1 | frozen by default |
| 14 | reprocess | 0off/1on | 1 | 0 | 1 | 0 | 1 | 1 | frozen by default |
| 15 | redshift | — | 0 | 0 | 1 | 0 | 1 | 1 | frozen by default |
| 16 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("agnsed")
# component: m.agnsed  (params as attributes)
```
