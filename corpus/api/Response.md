---
class: Response
module: response.py
---

# Response

Detector response class.

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| arf | — | get/set |  |
| chanEnergies | — | get |  |
| energies | — | get |  |
| rmf | — | get |  |
| sourceNumber | — | get |  |
| gain | — | instance |  |

## Methods

- `__init__(parent, respTuple)` — Construct a Response object.
- `setPars(*seqPars)` — Set multiple response parameters with a single function call.
- `show()` — Display response information including (optional) response parameters.
