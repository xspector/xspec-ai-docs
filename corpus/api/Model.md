---
class: Model
module: model.py
---

# Model

**Xspec model class.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| flux | — | get |  |
| lumin | — | get |  |
| startParIndex | — | get |  |

## Methods

- `__init__(exprString, modName='', sourceNum=1, setPars=None)` — Model constructor.
- `__call__(parIdx)` — Get a Parameter object from the Model.
- `energies(spectrumIndex)` — Get the Model object's energies array for a given spectrum.
- `folded(spectrumIndex)` — Get the Model object's folded flux array for a given spectrum.
- `setPars(*parVals)` — Change the value of multiple parameters in a single function call.
- `show()` — Display information for a single Model object.
- `showList()` — Show the list of all available XSPEC model components.
- `untie()` — Remove links for all parameters in Model object
- `values(spectrumIndex)` — Get the Model object's values array for a given spectrum.
