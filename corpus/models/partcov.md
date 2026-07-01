---
name: partcov
type: con  # convolution
func: C_PartialCovering
n_params: 1
family: [partcov]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPartcov.tex
---

# partcov

**convolution model** (`con`), function `C_PartialCovering`.

## Description

A convolution model to convert some absorption model into a partial covering 
absorption. If the absorption model is M(E) then this is converted to 
(1-CvrFract) + Cvrfact * M(E). Note that when specifying the model it is 
important to put parentheses in the right place. Let this model be P(E) 
which we want to apply to an absorption model M(E) then use the result 
to multiply an additive model A(E). The combined model should be specified 
as (P*M)*A, not P*M*A or P*(M*A).

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | CvrFract | — | 0.5 | 0.05 | 0.95 | 0 | 1 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("partcov*powerlaw")
# component: m.partcov  (params as attributes)
```
