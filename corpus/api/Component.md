---
class: Component
module: model.py
---

# Component

**Model component class**.

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| name | — | instance |  |
| parameterNames | — | instance |  |

## Methods

- `__init__(compName, parNames)` — Component constructor.
- `link(other)` — Link every parameter to the same-position parameter of `other`.
- `untie()` — Untie every parameter of this component, keeping the values.
