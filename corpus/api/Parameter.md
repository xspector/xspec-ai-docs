---
class: Parameter
module: parameter.py
---

# Parameter

**Model or response parameter class.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| error | tuple | get | A tuple containing the results of the most recent fit *error* |
| index | — | get | Position of the parameter within the Model object. |
| name | — | get/set | Name of Parameter (GET only). |
| prior | tuple | get/set | A tuple containing the settings for the prior used when |
| sigma | — | get | The Parameter fit sigma (-1.0 when not applicable) (GET only). |
| values | list | get/set | List of value floats [val,delta,min,bot,top,max]. |
| frozen | bool | get/set | Bool, if True then parameter is frozen. |
| unit | — | get | An optional string for the parameter's units (GET only). |
| link | — | get/set | Parameter link expression string (empty if not linked). |

## Methods

- `__init__(parName, parStrategy)` — Parameter constructor.
- `untie()` — Remove parameter link (if any)
