---
name: agnslim
type: add  # additive
func: agnslim
n_params: 15
family: [agnslim]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelAgnslim.tex
---

# agnslim

**additive model** (`add`), function `agnslim`.

## Description

A broadband spectral model for a super-Eddington black hole accretion
disc developed by 
[Kubota & Done (2019; KD19)](https://ui.adsabs.harvard.edu/abs/2019MNRAS.489..524K/abstract). 
This is based on the slim disc emissivity (
[Abramowicz et al., 1988](https://ui.adsabs.harvard.edu/abs/1988ApJ...332..646A/abstract); 
[Watarai et al., 2000](https://ui.adsabs.harvard.edu/abs/2000PASJ...52..133W/abstract); 
[Sadowski, 2011](https://ui.adsabs.harvard.edu/abs/2011arXiv1108.0396S/abstract)), 
where radial advection keeps
the surface luminosity at the local Eddington limit, resulting in
$L(r) \propto r^{-2}$ rather than the $r^{-3}$ expected from the
Novikov-Thorne (standard, sub-Eddington) disc emissivity. This is the
only major change from the sub-Eddington `agnsed` model
([Kubota & Done 2018; KD18](https://ui.adsabs.harvard.edu/abs/2018MNRAS.480.1247K/abstract),
an updated version of `optxagnf` ([Done et
al. (2012)](https://ui.adsabs.harvard.edu/abs/2012MNRAS.420.1848D/abstract)). The flow is radially
stratified, with an outer standard disc (from $R_{out}$ to $R_{warm}$), an
inner hot Comptonising region ($R_{in}$ to $R_{hot}$) and an intermediate warm
Comptonising region to produce the soft X-ray excess ($R_{warm}$ to
$R_{hot}$). A minor difference from `agnsed` is that the disc 
is assumed to extend untruncated down to the inner radius of the flow, 
$R_{in}$. This can be below the innermost stable circular orbit as
pressure forces are important. By default, the code calculates its own 
expected value of $R_{in}$ given the mass accretion rate. However, we
also allow this to be a free parameter e.g. for use for the extreme super
Eddington mass accretion rates probably truncate at some radius from
strong wind mass loss. Another minor difference from `agnsed` is that
we do not calculate the reprocessed emission as the geometry of the
inner disc is very uncertain but it probably shields the outer flow.

The model calculates some useful quantities, such as the radius at
which the flux first goes above the local Eddington limit, and the
inner radius of the flow. These are not normally displayed but can be
seen by inputting the command chatter 20, and getting the model to
recalculate the fit e.g. by changing the normalisation to 1.0001. Set
this back to the default of chatter 10 to suppress all this
information if further fits are required.

Parameters for agnslim:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | mass | solar | 10000000 | 1 | 10000000000 | 1 | 10000000000 | 0.1 | frozen by default |
| 2 | dist | Mpc | 100 | 0.01 | 1000000000 | 0.01 | 1000000000 | 0.01 | frozen by default |
| 3 | logmdot | — | 1 | -10 | 3 | -10 | 3 | 0.01 |  |
| 4 | astar | — | 0 | 0 | 0.998 | 0 | 0.998 | 1 | frozen by default |
| 5 | cosi | — | 0.5 | 0.05 | 1 | 0.05 | 1 | 1 | frozen by default |
| 6 | kTe_hot | keV(-pl) | 100 | 10 | 300 | 10 | 300 | 1 | frozen by default |
| 7 | kTe_warm | keV(-sc) | 0.2 | 0.1 | 0.5 | 0.1 | 0.5 | 0.01 |  |
| 8 | Gamma_hot | — | 2.4 | 1.3 | 3 | 1.3 | 3 | 0.01 |  |
| 9 | Gamma_warm | (-disk) | 3 | 2 | 5 | 2 | 10 | 0.01 |  |
| 10 | R_hot | Rg | 10 | 2 | 500 | 2 | 500 | 0.01 |  |
| 11 | R_warm | Rg | 20 | 2 | 500 | 2 | 500 | 0.1 |  |
| 12 | logrout | (-selfg) | -1 | -3 | 7 | -3 | 7 | 0.01 | frozen by default |
| 13 | rin | — | -1 | -1 | 100 | -1 | 100 | 1 | frozen by default |
| 14 | redshift | — | 0 | 0 | 5 | 0 | 5 | 1 | frozen by default |
| 15 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("agnslim")
# component: m.agnslim  (params as attributes)
```
