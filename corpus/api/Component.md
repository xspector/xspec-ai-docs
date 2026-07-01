---
class: Component
module: model.py
---

# Component

**Model component class**.

## Attributes

Attributes are **dynamic**: one per parameter, named by the parameter (e.g. `m.powerlaw.PhoIndex`), each a `Parameter`. See `corpus/recipes/00_object_model.md`.

## Methods

- `__init__(compName, parNames)` — Component constructor.
