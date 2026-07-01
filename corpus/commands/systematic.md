---
name: systematic
aliases: [xsystematic]
also_documents: []
source: XSsystematic.tex
---

# systematic

**add a model-dependent systematic term to the variance**

**Syntax:** `systematic`    [<modelName>] <model systematic error>

Set a systematic error term on the model to be added in quadrature to 
that on the data when evaluating chi-squared. The default value is zero.

If no `<modelName>` argument is given, then the `<model systematic error>`
value becomes the default value for all current models and any models defined
in the future.  But if a `<modelName>` is specified, the value will only apply 
to that model and it will override the default systematic error setting.

The `<modelName>` argument can be specified only if a model with that
name already exists. To set a value specifically for the default model 
(which has no name), `<modelName>` should be `unnamed`.
