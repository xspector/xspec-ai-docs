---
name: compTT
type: add  # additive
func: xstitg
n_params: 6
family: [compTT]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelComptt.tex
---

# compTT

**additive model** (`add`), function `xstitg`.

## Description

This is an analytic model describing Comptonization of soft photons in
a hot plasma, developed by Titarchuk (see [Titarchuk 1994, ApJ 434, 313](https://ui.adsabs.harvard.edu/abs/1994ApJ...434..570T/abstract)). This
replaces the Sunyaev-Titarchuk Comptonization model (`compST`)
in the sense that
the theory is extended to include relativistic effects. Also, the
approximations used in the model work well for both the optically thin
and thick regimes. The Comptonized spectrum is determined completely
by the plasma temperature and the so-called $\beta$ parameter which is
independent of geometry. The optical depth is then determined as a
function of $\beta$ for a given geometry. Thus par5 switches
between spherical and disk geometries so that $\beta$ is not a direct
input here. This parameter MUST be frozen. If par5 $\geq 0$,
$\beta$ is obtained from the optical depth using analytic
approximation (e.g. [Titarchuk 1994](https://ui.adsabs.harvard.edu/abs/1994ApJ...434..570T/abstract)). If par5 < 0 and $0.1 <
\tau < 10$, $\beta$ is obtained by interpolation from a set of
accurately calculated pairs of $\beta$ and $\tau$ from [Sunyaev &
Titarchuk (1985, A&A 143, 374)](https://ui.adsabs.harvard.edu/abs/1980A&A....86..121S/abstract).

In this incarnation of the model, the soft photon input spectrum is a
Wien law [$x^2e^{-x}$ photons] because this lends itself to a
particularly simple analytical form of the model. For present X-ray
detectors this should be adequate. Note that in energy flux space the
peak of the Wien law occurs at 3kT as opposed to 2.8kT for a
blackbody.  The plasma temperature may range from 2--500 keV, but the
model is not valid for simultaneously low temperatures and low optical
depth, or for high temperatures and high optical depth. The user is
strongly urged to read the following references (esp. HT95 Fig 7)
before and after using this model in order to fully understand and
appreciate the physical assumptions made: [Titarchuk (1994, ApJ
434,
313)](https://ui.adsabs.harvard.edu/abs/1994ApJ...434..570T/abstract);
[Hua & Titarchuk (1995, ApJ 449, 188)](https://ui.adsabs.harvard.edu/abs/1995ApJ...449..188H/abstract);
[Titarchuk & Lyubarskij (1995, ApJ 450, 876)](https://ui.adsabs.harvard.edu/abs/1995ApJ...450..876T/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 2 | T0 | keV | 0.1 | 0.01 | 100 | 0.001 | 100 | 0.01 |  |
| 3 | kT | keV | 50 | 2 | 500 | 2 | 500 | 0.1 |  |
| 4 | taup | — | 1 | 0.01 | 100 | 0.01 | 200 | 0.1 |  |
| 5 | approx | — | 1 | 0 | 5 | 0 | 200 | 0.1 | frozen by default |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("compTT")
# component: m.comptt  (params as attributes)
```
