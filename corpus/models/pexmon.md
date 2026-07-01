---
name: pexmon
type: add  # additive
func: pexmon
n_params: 8
family: [pexmon]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelPexmon.tex
---

# pexmon

**additive model** (`add`), function `pexmon`.

## Description

This model from [Nandra et al. (2007)](https://ui.adsabs.harvard.edu/abs/2007MNRAS.382..194N/abstract) combines `pexrav`
with self-consistently generated Fe K$\alpha$, Fe K$\beta$, Ni
K$\alpha$ and the Fe K$\alpha$ Compton shoulder. Line strengths are based on Monte Carlo calculations
by [George & Fabian (1991)](https://ui.adsabs.harvard.edu/abs/1991MNRAS.249..352G/abstract) which are parametrized for
$1.1 < \gamma < 2.5$ by :

$$EW = 9.66 EW_0(\gamma^{-2.8} - 0.56)$$

with inclination dependence for $i < 85$ degrees :

$$EW = EW_0 (2.20 \cos i - 1.749 (\cos i)^2 + 0.541(\cos i)^3)$$

and abundance dependence :

$$\log EW = \log EW_0 (0.0641 \log A_{Fe} - 0.172 (\log A_{Fe})^2)$$

The Fe K$\beta$ and Ni K$\alpha$ line fluxes are 11.3% and 5%
respectively of that for Fe K$\alpha$. The Fe K$\alpha$ Compton shoulder is
approximated as a gaussian with E = 6.315 keV and $\sigma = 0.035$ keV. The
inclination dependence is taken from [Matt (2002)](https://ui.adsabs.harvard.edu/abs/2002MNRAS.337..147M/abstract) such
that :

$$EW_{shoulder} = EW_{Fe K\alpha}(0.1 + 0.1 \cos i)$$

The model parameters are :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndex | — | 2 | 1.1 | 2.5 | 1.1 | 2.5 | 0.01 |  |
| 2 | foldE | keV | 1000 | 1 | 1000000 | 1 | 1000000 | 1 | frozen by default |
| 3 | rel_refl | — | -1 | -1000000 | 1000000 | -1000000 | 1000000 | 1 | frozen by default |
| 4 | redshift | — | 0 | 0 | 4 | 0 | 4 | 0.01 | frozen by default |
| 5 | abund | — | 1 | 0 | 1000000 | 0 | 1000000 | 0.01 | frozen by default |
| 6 | Fe_abund | — | 1 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 7 | Incl | deg | 60 | 0 | 85 | 0 | 85 | 1 |  |
| 8 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("pexmon")
# component: m.pexmon  (params as attributes)
```
