---
name: model
aliases: [xmodel]
also_documents: []
source: XSmodel.tex
---

# model

**define a theoretical model**

Define the form of the theoretical model to be fit to the data.

**Syntax:** `model` [<source num>:<name>] [<delimiter>] <component1>
 <delimiter> <component2> <delimiter>...<componentN>
  [<delimiter>]

**model** & `[?]`

**model** & `[<name>| unnamed] none`

**model** & `clear`

**model** & `<name>| unnamed active| inactive`

where `<delimiter>` is some combination of (, +, $\ast$, ), and 
`<componentJ>` is one of the model components known to XSPEC. 
The optional name must be preceded by a source number followed by a colon. 
To specifically refer to the default model use the string `unnamed`. 
Descriptions of these models may be accessed by typing `help model <componentJ>` 
at the prompt. 

The source argument and name, if present, assign that model to be used with 
one of the sources found to be in the spectrum during the data pipelining. 
These 2 parameters allow one to simultaneously analyze multiple models, 
each assigned to their own responses.  The model will be referred to the 
channel space using a response corresponding to that source number.  
To create a model for a source number higher than 1, a detector response 
must first exist for that number.  See the examples below and the `response` 
command for more information about using multiple sources.  This ability 
to assign multiple models both generalizes and replaces the XSPEC11 method 
of using '/b' to specify background models.

After the model is loaded, if there are data present the model is attached 
through the instrumental response to the spectra to be fitted, as in 
XSPEC11. Unlike XSPEC11, however, if there are no data loaded the model will 
be attached to a default diagonal dummy response. The parameters of that 
dummy response (energy range, number of flux points, linear/logarithmic 
intervals) can be set by the user in the Xspec.init file using the 
DUMMY setting. Thus any model can be plotted in energy or wavelength 
space as soon as it has been defined.

**Component Types**

The model components are of various types depending on what they represent 
and how they combine with other models additive, multiplicative, convolution, 
pile-up, and mixing models. Each component may have one or more parameters 
that can be varied during the fit (see the `newpar` command writeup).

**Additive** model components are those directly associated with sources, such 
as power laws, thermal models, emission lines, etc.  The net effect of two 
independent additive models is just the sum of their individual emissivities. 

**Multiplicative** model components do not directly produce photons, 
but instead modify (by an energy-dependent multiplicative parameter) the 
spectrum produced by one or more additive components. Examples of 
multiplicative models are photoelectric absorption models, edges, 
absorption lines, etc.

**Convolution** models components modify the spectrum as a whole, 
acting like operators rather than simply applying bin by bin multiplication 
factors. An example of a convolution model is a gaussian smoothing with energy 
dependent width. Thus, when using convolution models, the ordering of 
components is in general significant (see below under **syntax rules**).

The **pile-up** model (type `acn`) is applied *after* the 
model has been folded through the response: it acts on the count spectrum, 
on the response's ungrouped detector channels, so that the pulse heights of 
photons arriving in one frame add.  It operates on the sum of the components 
it multiplies, must be the first component of its term, and only one is 
allowed in a model (see `pileup`).

**Mixing** model components implement two-dimensional transformations 
of model spectra. The data are divided into regions by assigning them to 
2 or more datagroups, and the transformation ``mixes'' the flux among the 
regions. An example is the `projct` (projection) model, which 
assumes that the regions are 3-dimensional ellipsoidal shells in space, 
and projects the flux computed from the other components onto 
2-dimensional elliptical annuli.

A list of all the currently installed models is given in response to the command 

```
XSPEC> model ?

 The '?' is not actually required.

 This will leave the current model in use.  
```

Adding a component name shows that component's definition without loading
it, so it works with no data and no model, and the current model is left
untouched:

```
XSPEC> model ? gabs
Model component gabs: multiplicative (mul), built-in
   energy range 0 - 1e+20 keV
   gradient: analytic, with VJP (gv);  spectrum dependent: no
   model.dat tokens: grad=gv:... identity=Strength:0
 Par  Name       Unit     Default    Hard min   Soft min   Soft max   Hard max   Delta
   1  LineE      keV      1          0          0          1e+06      1e+06      0.05
   2  Sigma      keV      0.01       0          0          10         20         0.05
   3  Strength   keV      1          0          0          1e+06      1e+06      0.05
 Documentation: help model gabs
```

The header gives the component's type and where it comes from: built-in, a
local model (with the package that `lmod` loaded and the model
description file), a Python model, or an `mdefine` component (with its
expression). The second line says which analytic derivatives are registered
for it (none means XSPEC uses finite differences) and whether it depends on
the spectrum, and the third lists the keyed tokens of its model description
file entry, as written (see Appendix AppendixAddModels). The parameter
table gives each parameter's default, limits and delta from the model
description file; a negative delta (frozen by default) is marked
`frozen`, a switch parameter (`$`) shows its default setting,
and a scale parameter (`*`) its fixed value. An additive component's
normalization is not in the table. The name may be abbreviated as for
`model` (an `mdefine` name must be given in full); an
abbreviation that several components share lists them, and a name with
`*` or `?` lists every component it matches, with its type and
number of parameters:

```
XSPEC> model ? *gabs
  gabs           mul  3 parameters
  vgabs          mul  ...
```

`tclout modinfo` returns the same information as a Tcl list.

The new command variants have the following uses:

- [model  {[<name>{]} none}] 

removes the model of name `<name>` if given. Without the `<name>` 
argument, the command removes the unnamed ``default'' model, which 
is of course the XSPEC11 behavior.

- [model clear] 

removes all models

- [model <name>| unnamed active| inactive] 

makes the model named `<name>` active (fit to data) or inactive. 
Inactive models are tied to a dummy (unit diagonal) response. Making a model 
assigned to a given source active makes any previous model assigned to that source 
inactive. Note that to make the default unnamed model active or inactive 
refer to it by the string unnamed.

See the commands `delcomp`, `addcomp` and `editmod` for details 
on how to modify the current model without having to enter a completely new model.

Response models --- transformations of a detector response, such as a gain
shift --- are attached to a response with the separate `rmodel`
command.

**Syntax Rules**

Model components are combined in the obvious algebraic way, with + separating additive 
models, $\ast$ separating multiplicative models, and parentheses to show which 
additive models the multiplicative models act on. The $\ast$ need not be included 
next to parentheses, where it is redundant. Also, if only one additive model is 
being modified by one or more multiplicative models, the required brackets may 
be replaced by a $\ast$. In this case the additive model must be the last component 
in the grouping. Thus

M1*(A1+A2) + M2*M3(A3) + M4*A4 + A5

is a valid model, where the M's signify multiplicative models and the A's 
additive models. 

The old style syntax for entering models (versions 9.02 and earlier) is not supported 
in version 12 and will return a syntax error.

XSPEC12's recursive lexical analyzer and expression parser allows, in principle, 
infinite nesting depth. It has been tested to 3 levels of parentheses, although it 
should be said that this new behavior is a by-product of the design rather than 
fulfilling an important need. Thus, expressions such as

M1*(A1 + A2*(A3 + M2*M3*(A4 + A5))) + C1*(A6 + M4*(A7 + M5*A8))

are supported.

The model expression is analyzed on entry and syntax errors, or undefined 
models, will return control to the prompt with an error message. XSPEC12's 
model definition algorithm treats expressions delimited by '+' signs that 
are not within parentheses as separate ``Component Groups''. The Component 
Group comprises a list of components of the different types, and these are 
in turn calculated and then combined to produce an internal ``Sum Component''. 
These Sum Components from each such component group are then added to 
produce the output model (note that if there is an overall component - for 
example, a convolution or mixing component - then all of the model will 
be contained inside one Component Group).

The syntax rules that are checked for are as follows:

- A '*' must be preceded and followed by words or a brace (redundant 
braces are removed).

- A standalone component must be additive. A standalone component is 
defined as a single component model or a single component at the beginning 
(end) of the expression followed (preceded) by a '+', or in the middle of 
the expression delimited by 2 '+' signs.

- A convolution or mixing component must not appear at the end, or 
followed by a closing brace.

When using convolution or mixing components, the order in which they are 
applied is in  general significant.For example, the two models

C1*M1(A1+A2) and M1* C1 (A1+A2)

are not necessarily equivalent (here the C's represent convolution models).
The way XSPEC handles the ordering of components is by first computing 
the spectrum for the additive components of a given additive group 
(A1+A2 in the above example). It then applies all multiplicative or 
convolution components in the additive group from right to left in the 
order they appear in the model formula. 

N.B. Beginning with v12.5.0, convolutions no longer have to precede the 
source.  Parentheses may also be used to specify convolution precedence, 
so the following two examples are not equivalent:

C1*M1(A1+A2) and (C1*M1) (A1+A2)

**Examples:**
  
Note that po (= `powerlaw`) and ga (= `gauss`) 
are additive models, and that `wabs` and `phabs` 
(different photoelectric absorption screens) are multiplicative models.

XSPEC> model po 
// The single component po (powerlaw) is the model.
XSPEC> model po+ga
XSPEC> model (po+ga)wabs
XSPEC> model phabs(po+ga)
XSPEC> model wa(phabs(po)+ga)
XSPEC> model wa po phabs ga //error: old syntax
XSPEC> model wa*phabs*po
XSPEC> model (po+po)phabs 
//Note that though the first and second components are the same 
// form, their parameters are varied separately.
XSPEC> model phabs*wa(po)

A complex (and almost certainly unphysical) example is the following:

XSPEC>model wa(po+pha(peg+edge(disk+bbod)))const + pla(pos+hr*step) + not*gau

Applying multiple models:
Assume 3 spectra are loaded, each with a single response (source 1 by default).
XSPEC> model wa(po)
	// The unnamed model wa(po) will apply to all 3 spectra, accordingly 
	// multiplied by each spectrum's response.
XSPEC> response 2:2 new_resp.pha 2:3 another_new_resp.pha
	// Additional responses assigned to source number 2 for spectra 2 and 3.
XSPEC> model 2:second_mod ga
	// The model "second_mod" will now apply to source 2, and is therefore
	// multiplied by new_resp.pha and another_new_resp.pha for spectra 2 
	// and 3 respectively.
XSPEC> model second_mod inactive
	// "second_mod" will no longer apply to spectra 2 and 3, though they
	// retain responses for source 2.  
	OR
XSPEC> response 2:2 none
XSPEC> response 2:3 none
	// No responses exist for source number 2, second_mod is
	// rendered inactive.
