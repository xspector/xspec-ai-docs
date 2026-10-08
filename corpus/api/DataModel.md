---
class: DataModel
module: spectrum.py
---

# DataModel

**A data model attached to a spectrum** (the *dmodel* command).

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| name | — | get | The data model's name (get only). |
| spectrum | — | get | Index of the spectrum it is attached to (get only). |
| parameters | — | get | Its Parameter objects, row order (get only). |
| parameterNames | — | instance |  |

## Methods

- `__init__(spectrum, name, parNames, offset)` — Intended for creation by a Spectrum object only.
- `__call__(index)`
