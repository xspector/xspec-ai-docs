---
name: cgain
type: rsp  # rsp
func: C_cgain
n_params: 2
family: []
energy_range: [0., 1.e20]
source: manager/model.dat + (no tex)
---

# cgain

**rsp model** (`rsp`), function `C_cgain`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | slope | — | 1 | 0.5 | 1.5 | 0.01 | 5 | 0.01 |  |
| 2 | offset | chan | 0 | -100 | 100 | -10000 | 10000 | 0.1 |  |

## PyXspec

```python
from xspec import Model
m = Model("cgain")
# component: m.cgain  (params as attributes)
```
