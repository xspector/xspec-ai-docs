---
name: bkgnorm
type: dat  # dat
func: C_bkgnorm
n_params: 1
family: [bkgnorm]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelBkgnorm.tex
---

# bkgnorm

**dat model** (`dat`), function `C_bkgnorm`.

## Description

A data model (attached with `dmodel`) whose parameter $b$ multiplies
the spectrum's background scaling factor, $\alpha \to b\alpha$, where
$\alpha$ is the ratio of the source and background exposures, areas and
BACKSCALs.  The background therefore enters the statistic as $b\alpha B$:
for $\chi^2$ it is subtracted as $b\alpha B$ and its variance scaled by
$(b\alpha)^2$; for W (`cstat` with a background) and `pgstat`
the background profiled at each bin is estimated with the scale $b\alpha$.
Use it when the background normalization is uncertain, for example a
background taken from a region whose area or particle level is known only
approximately.

```
XSPEC>dmodel 1 bkgnorm & 1.0
XSPEC>dthaw 1
XSPEC>bayes d1 lognormal 1 0.05
XSPEC>bayes on
```

$b$ is frozen at 1 by default.  Freed with nothing to constrain it, $b$ and
the source normalization are close to degenerate when the background
spectrum resembles the source spectrum; give it a prior
(`bayes` `d`$n$), such as the lognormal above for a 5 per cent
uncertainty in the scaling.  `bkgnorm` is refused on a spectrum
without a background, including one whose background is fitted with
`backmodel`; if the background is removed after it is attached, it is
inactive and $b$ is not a fit parameter.  Simulations draw the background
contribution as $b\alpha B$, and `fakeit` writes the nominal
BACKSCAL.  The fit derivatives with respect to $b$ come from the statistic
itself, by a central difference in $b$ that needs no model evaluation.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Bnorm | — | 1 | 0.01 | 10 | 0.01 | 100 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("bkgnorm")
# component: m.bkgnorm  (params as attributes)
```
