---
class: Background
module: spectrum.py
---

# Background

**Background spectral data class.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| areaScale | — | get | The Background area scaling factor (GET only). |
| backScale | — | get | The Background back scaling factor (GET only). |
| exposure | float | get | The exposure time keyword value [float] (GET only). |
| fileName | str | get | The spectrum's file name [string] (GET only). |
| fromBackground | — | get | For a correction (Spectrum.correction): the background file |
| isPoisson | bool | get | Boolean flag, True if spectrum has Poisson errors (GET only). |
| values | tuple | get | Tuple of floats containing the background rates array in |
| variance | tuple | get | Tuple of floats containing the variance of each |

## Methods

- `__init__(backTuple, parent, isCorrection=False)` — Construct a Background object.
