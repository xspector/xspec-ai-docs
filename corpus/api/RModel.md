---
class: RModel
module: response.py
---

# RModel

**Response Model class.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| isOn | — | get | On/Off indicator for RModel object. |
| name | — | get | The response model's name. |
| parameterNames | — | instance |  |

## Methods

- `__init__(resp, parNames, rmodName)` — RModel constructor.
- `off()` — Remove this response model and its parameters (turn it OFF).
