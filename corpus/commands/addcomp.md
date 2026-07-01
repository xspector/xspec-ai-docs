---
name: addcomp
aliases: [xaddcomp]
also_documents: []
source: XSaddcomp.tex
---

# addcomp

**add component to a model**

Add a component to the model.

**Syntax:** `addcomp` [<modeName>:]<n>  <comp>

where `<n>` is the component number before which the new 
component is to be inserted, and `<comp>` is the name of the new 
component. Components are numbered in sequence in order of appearance in the 
expression entered. The new component is regarded as an operator on the 
component added if it is not additive.

The optional `<modelName>` qualifier allows the user to address a named model.

The user is prompted for parameter values for the component. If there are 
m components in the current model, then acceptable values for the 
component number added are 1 to m+1. 

XSPEC detects the type of the model (additive, multiplicative etc), checks the 
correctness of the syntax of the output model, and adds the component if the 
resulting models obeys the syntax rules documented in the `model` command.

Thus,

```
XSPEC12> mo  wa(po)
```

Followed by

```
XSPEC12> addcomp 2 bb
```

Yields the model achieved by

```
XSPEC12> mo  wa(bb + po)
```

See also `delcomp` (delete component by number).

Other examples will serve to clarify `addcomp`'s behavior.  Suppose
that the current model specification is

```
ga+po
```

which using the `show` command would yield the description

```
model  = gaussian[1] + powerlaw[2]
```

The comments give the model expression following the entry of `addcomp`
and `delcomp` commands:

XSPEC12> addcomp 2 wab 
// gaussian[1] + wabs[2](powerlaw[3])
XSPEC12> addcomp 4 pha 
// (gaussian[1] + wabs[2](powerlaw[3]))phabs[4]
XSPEC12> delcomp 1	
// (wabs[1](powerlaw[2]))phabs[3]}
XSPEC12> addcomp 2 zg 
// (wabs[1](zgauss[2] + powerlaw[3]))phabs[4]
XSPEC12> delcomp 3 
// (wabs[1](zgauss[2]))phabs[3]

XSPEC12> mo wa(po)
XSPEC12> addcomp 1 ga
// gauss[1] + wabs[2]*powerlaw[3]
XSPEC12> delcomp 1
XSPEC12> addcomp 1 pha
// phabs[1]*wabs[2]*powerlaw[3]

XSPEC12>mo wabs(po)
XSPEC12> addcomp 3 bb
// wabs[1]*powerlaw[2] + bbody[3]
XSPEC12> delcomp 1
XSPEC12> addcomp 3 pha
// wabs[1]*powerlaw[2]*pha[3]
XSPEC12> addcomp 3 po
// ERROR: po (additive) is interpreted as being added to the 
// multiplicative model pha[3], which is a context error.

For multiply nested models?
XSPEC12> mo wa(po + pha(bb + ga))
XSPEC12> addcomp 6 po
// wabs[1](powerlaw[2] + phabs[3](bbody[4] + ga[5]) + powerlaw[6])
XSPEC12> addcomp 5 peg
// wabs[1](powerlaw[2] + phabs[3](bbody[4] + pegpwlw[5] ga[6]) + powerlaw[7])
XSPEC12> addcomp 7 wa
// wabs[1](powerlaw[2] + phabs[3](bbody[4] + pegpwlw[5] ga[6]) + wabs[7]*powerlaw[8])
