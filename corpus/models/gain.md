---
name: gain
type: rsp  # rsp
func: C_gain
n_params: 2
family: []
energy_range: [0., 1.e20]
source: manager/model.dat + (no tex)
---

# gain

**rsp model** (`rsp`), function `C_gain`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | slope | — | 1 | 0.5 | 1.5 | 0.01 | 5 | 0.01 |  |
| 2 | offset | keV | 0 | -1 | 1 | -1 | 1 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("gain")
# component: m.gain  (params as attributes)
```
