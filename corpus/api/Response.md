---
class: Response
module: response.py
---

# Response

Detector response class.

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| rmodels | — | get |  |
| arf | — | get/set |  |
| firstOrder | — | get/set |  |
| firstOrderInfo | — | get |  |
| chanEnergies | — | get |  |
| energies | — | get |  |
| rmf | — | get |  |
| sourceNumber | — | get |  |
| gain | — | instance |  |

## Methods

- `__init__(parent, respTuple)` — Construct a Response object.
- `setPars(*seqPars)` — Set multiple response parameters with a single function call.
- `addRModel(name, *values)` — Attach a response model to this response, or reset one already attached.
- `removeRModel(name=None)` — Remove one response model from this response, or all of them.
- `show()` — Display response information including (optional) response parameters.
