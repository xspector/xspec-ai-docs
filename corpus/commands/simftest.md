---
name: simftest
aliases: [xsimftest]
also_documents: []
source: XSsimftest.tex
---

# simftest

**likelihood-ratio test for a model component, calibrated by simulation**

Estimate how significant a component of the current model is, by the
likelihood ratio calibrated by simulation (see `lrt`).

**Syntax:** `simftest` <model_comp> <niter> [<filename>]

`<model_comp>` is the number of a component of the default model, as
`delcomp` counts them.  The alternative is the current model; the null
is the same model with that component switched off and its parameters
frozen.  An additive component is switched off by setting its
normalisation to zero; a multiplicative component by setting the
parameters its model definition names in `identity=` to the values
there (for `gabs`, `Strength` = 0; for an absorber,
`nH` = 0) --- see Appendix AppendixAddModels.  A multiplicative
component with no `identity=` setting, a convolution or mixing
component, and a component with no free parameter are refused; use
`lrt` with an explicit null for those.  `<filename>` and the
report are as for `lrt`.

**Examples:**

```
XSPEC> model powerlaw + gaussian
XSPEC> fit
XSPEC> simftest 2 1000
// Is the gaussian needed?  Null: its norm at 0.
XSPEC> model gabs*powerlaw
XSPEC> fit
XSPEC> simftest 1 1000 gabs.txt
// The absorption line: null Strength = 0.
```
