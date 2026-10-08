---
name: newpar
aliases: [rnewpar, xnewpar, xrnewpar]
also_documents: [rnewpar]
source: XSnewpar.tex
---

# newpar (and rnewpar, dnewpar)

**change parameter values**

Adjust one or more of the model parameters.

 p{} p{---6}}
**Syntax:** & **newpar** & `[<modelName>:]<index range> [<param spec list>]`

**Syntax:** & **newpar** & `[<modelName>:]<index> = <coupling expression>`

**Syntax:** & **newpar** & `[<modelName>:]<index> upper|lower = <limit expression>`

**Syntax:** & **newpar** & `[<modelName>:]<index> upper|lower none`

**Syntax:** & **newpar** & `comp [<modelName>:]<c> [group <g>] = comp [<modelName>:]<c'> [group <g'>]`

**Syntax:** & **newpar** & `0`

where:

`<param spec list>` ::= `<param value>` `<delta>` `<param range spec>` 

`<param range spec>` ::= `<hard min>` `<soft min>` `<soft max>` `<hard max>`

For **response parameters** (created with the `gain` or `rmodel` command):

 p{} p{---6}}
**Syntax:** & **rnewpar** & `[<sourceNum>:]<idx range> [<param spec list>]`

**Syntax:** & **rnewpar** & `[<sourceNum>:]<index> = <coupling expression>`

For **data parameters** (see the `dmodel` command), `dnewpar`
takes a data parameter number; a data parameter can be linked only to
other data parameters (`dnewpar 2 = d1`).

The model parameters are accessed through their model parameter indices. 
For example, the first parameter of the first model component generally 
is model parameter 1, etc. The first command line argument, <index range>, 
gives the indices' parameters to be modified by the `newpar` command. 
The default value is the range from the previous invocation of `newpar`. 
The remaining arguments can be used to update the parameter specification. 
If the parameter specification is omitted from the command line, then the 
user is explicitly prompted for it. The first two arguments of the parameter 
specification are:

 p{0.61}}
`<param value>` & The trial value of the parameter used initially in the fit

`<delta>` & The step size used in the numerical determination of the 
derivatives used during the fitting process.  When delta is set to zero, 
the parameter is not adjustable during the fit.  This value may be overriden 
for all parameters by the `xset delta` command option, which will apply 
a proportional rather than a fixed delta.

The four arguments of the range specification determine the range of
acceptable values for the parameter. The soft limits should include the
range of expected parameter behavior. The parameter is never allowed to
have a value at or outside the hard limits.  The default
Levenberg-Marquardt (`leven`) method treats the whole range
between the hard limits uniformly, so a fit started between the soft and
hard limits converges the same way as one started inside them.  The
Minuit methods (`migrad`, `simplex`) enforce the hard
limits through Minuit's own internal transformation; see the
`method` command for how the limits are passed to Minuit.

A slash (/) will set all the six parameter specification values (value, 
delta, range specification) to the previous value (default for a new 
model, current value if the parameter has previously been set or fit).

The sequence  /* leaves all parameters unchanged (in the case of a new model, 
to be set to the default).

`newpar` **0** prints the current parameter settings.

**Parameter Links**

Coupling of parameters allows parameters in a model to always have the same 
value or to be related by an expression. The expression is a function of 
the other parameters (XSPEC will reject attempts to link parameters to 
themselves!). Scale parameters (i.e. never variable during a fit), and s
witch parameters (i.e. that change the mode in which a component 
is calculated) can only be linked to other scale and switch parameters, 
respectively. Details of parameter types are explained in more detail 
in Appendix AppendixAddModels. 

The syntax for linking parameters is

`XSPEC> newpar <par> = f(<par>)`

where `f` is a function in the (other) parameters. Parameters can 
be specified either by the character 'p' followed by the parameter number (
preferred) or by the parameter number. Integers appearing in `f` that are 
within the range of existing parameter numbers will be interpreted as 
parameters: to avoid confusion, if a real number is intended it should 
include a decimal point. Integers larger than the last parameter number will 
be interpreted as integers. Parameters of named models must be prefixed 
by `<modelName:>`.
 
The following operators and functions can be used in `f`:

3{c}{**operators**}

+ & = & plus operator

- & = & minus operator

$\ast$ & = & multiplying operator

/ & = & dividing operator

$\ast\ast$ & = & exponentiation operator

^ & = & exponentiation operator

4{c}{**unary functions**}

EXP & (expr) &	= &	exponential

SIN &	(expr)	& = & 	sine in radians
  
SIND &	(expr)  & = &	sine in degrees
 
COS &	(expr)	& = &	cosine in radians
  
COSD &	(expr)	& = &	cosine in degrees
 
TAN &	(expr)	& = &	tangent in radians
  
TAND &	(expr)	& = &	tangent in degrees
 
SINH &	(expr)	& = & 	hyperbolic sine in radians
  
SINHD &	(expr)  & = &	hyperbolic sine in degrees
 
COSH &	(expr)	& = &	hyperbolic cosine in radians
  
COSHD &	(expr)	& = &	hyperbolic cosine in degrees
 
TANH &	(expr)	& = &	hyperbolic tangent in radians
  
TANHD &	(expr)	& = &	hyperbolic tangent in degrees
 
LOG &	(expr)	& = &	base 10 log
 
LN &	(expr)	& = &	natural log

SQRT &	(expr)	& = &	square root

ABS &	(expr)	& = & 	absolute value

INT &	(expr)	& = &	integer part

ASIN &	(expr)	& = &	inverse sine in radians
  
ACOS &	(expr)	& = &	inverse cosine in radians
  
ATAN &	(expr)	& = &	inverse tangent in radians
  
ASINH &	(expr)	& = &	inverse hyperbolic sine in radians
  
ACOSH &	(expr)	& = &	inverse hyperbolic cosine in radians
  
ATANH &	(expr)	& = &	inverse hyperbolic tangent in radians
  
ERF  &	(expr)	& = &	error function

ERFC &	(expr)	& = &	complementary error function

GAMMA &	(expr)	& = &	gamma function

SIGN &	(expr)	& = &	-1 if negative, +1 if positive 

HEAVISIDE & (expr) & = & 0 if negative, +1 if positive 

BOXCAR & (expr) & = &   +1 between 0 and 1, 0 otherwise 

}
4{c}{**binary functions**}

ATAN2 &	(expr1, expr2)	& = &	principal value of the arc tan of expr1/expr2 in radians 

MAX &	(expr1, expr2)	& = &	maximum of the two expressions

MIN &	(expr1, expr2)	& = &	minimum of the two expressions

An expression may also read a parameter's *limits*:
`p<n>.lower` and `p<n>.upper` are its effective hard
limits (including any dependent limit, below), and
`p<n>.softlower` and `p<n>.softupper` its soft limits,
with a model prefix as for values (`mod2:p3.upper`).  So
`newpar 3 = p2.upper` keeps parameter 3 at parameter 2's upper limit,
and follows it when that limit is edited.

**Dependent Limits**

A parameter's hard upper or lower limit can be an expression of other
parameters, written in the same language as a link:

`XSPEC> newpar 4 upper = p1`

`XSPEC> newpar 8 upper = 1 - p5`

`XSPEC> newpar 6 lower = p3 + 0.4`

The first keeps line 2's energy at or below line 1's (so two lines cannot
swap places), the second keeps two fractions summing to at most 1, and the
third keeps two lines at least 0.4 keV apart.  The bound is a hard limit: the
effective hard limit is the tighter of the expression and the numeric limit at
each point, and the soft limit is clamped to it.  `newpar <n>
upper none` (or `lower none`) removes it, leaving the numeric limit.
`show` `parameters` prints a dependent limit at the end of its
parameter's line (`<= p1`, `>= p3 + 0.4`), and `save`
writes the `newpar` line after the parameters.

A point outside a dependent limit is invalid, and every engine treats it so.
`leven` makes a parameter whose step would carry it past its bound
follow the bound for that step, which lets a fit slide along a bound that moves
with the parameters it reads; a trial still outside is rejected like an
uphill step.  `migrad` refuses to fit while any dependent limit is in
force (its bound transformation is fixed when the fit starts), and suggests
`leven`.  `chain` (Metropolis--Hastings and Goodman--Weare) and
`hmc` reject such a proposal, and `nest` gives it zero
likelihood --- so the prior is the box of numeric limits truncated by the
constraint, and the evidence it reports is relative to the untruncated box.
`error` and `steppar` keep their inner fits inside the bounds;
`error` reports a parameter pegged at its dependent limit, and a
`steppar` grid point outside one whatever the free parameters do is
skipped, marked `skipped`, and given the grid's largest statistic.

The refusals: a bound the parameter's current value breaks (move the value
first --- nothing is clamped silently); a dependent limit on a linked or
periodic parameter, or on a response parameter; and an expression that would
close a cycle through values and limits (`p1.lower = p2.lower` with
`p2.lower = p1.lower`, or `p1.upper = p1 + 1`), which is
named.  A value that would put any parameter outside a dependent limit is
refused and the old value kept.  Linking a parameter that has a dependent
limit removes the limit, with a note, and deleting a component a limit reads
reverts that limit to numeric, also with a note.  Dependent limits belong to
the parameter they are set on: they are not copied to its data-group copies.

**Component Links**

`newpar comp <c> group <g> = comp <c'> group <g'>`
links every parameter of component <c> in data group <g> to the
same-position parameter of component <c'> in group <g'>.  A group
left out is the model's first; a source component with no model prefix is in
the target's model.  The two must have the same parameter names in the same
order --- otherwise nothing is linked and both lists are shown --- and a
component cannot be linked to itself or to one that already depends on it.
The links are ordinary parameter links, exactly as if typed one by one, so
`show`, `save` (which writes them one by one), `untie` and
the fit see nothing new.  `untie` `comp` undoes them.

If there are multiple data groups present, then the parameters of models 
associated with datagroups greater than 1 (``secondary models'') are 
coupled by default to their ``primary'' counterparts. For example, if 
there are 5 parameters in the model and 3 datagroups present, then the 
model command will prompt for 15 parameters. If the user types

```
XSPEC> model <expression>
XSPEC>/*
```

Then parameters 1-5 will be set to their values specified in the 
initialization (model.dat) file. Parameters 6-15 will be linked 
to their counterparts, i.e. as if the user had typed

```
XSPEC> newpar 6 = p1
XSPEC> newpar 7 = p2
...
XSPEC> newpar 11 = p1
```

And so on.

**Examples:**

The total number of model parameters for the example is four.

```
XSPEC> newpar 2 0.1
// The value of the second parameter is set to 0.1.
XSPEC> newpar 3-4
// The program will prompt for a specification for the 3rd
//   parameter (comp gives the name of the corresponding model 
//   component)
comp:param3>0.001, 0
// which has its value set to 0.001 and its delta set to zero, fixing 
//   it in later fits.The program now prompts for a specification for 
//   the 4th parameter
comp:param4>21
// which is set to 21.As there is no 5th parameter, the program 
//   displays a summary and returns to command level.
XSPEC> newpar ,,.001
// The value of the delta of the 3rd parameter (which is the default 
//   index as it was the first parameter modified in the previous 
//   newpar invocation) is set to 0.001, allowing it to be adjusted 
//   during any fits.
```

The total number of parameters for this example is eight.

```
XSPEC> newpar 4 = 1
// The value of parameter 4 is set to the value of parameter 1. 
//   This has the consequence of model parameter 4 being frozen at the
//   value of parameter 1 during subsequent fitting procedures.
//   If model parameter 1 is a free parameter, then both parameters
//   1 and 4 change their values simultaneously in the fit procedure.
XSPEC> newpar 4 = p3/5 + 6.7 
// The value of parameter 4 is set to the value of
//   (parameter 3/ parameter 5) plus 6.7
XSPEC> newpar 6 = p3 * 0.1 - 9.5
// The value of parameter 6 is set to 0.1 times the 
//   value of parameter 3 minus 9.5
XSPEC> newpar 5 = 2 + 5. 
// The value of parameter 5 is set to the value
//   of parameter 2 plus 5.
XSPEC> newpar 8 = p1 / 4.6
// parameter 8 is set to parameter 1 divided by 4.6
XSPEC> newpar 8 = abs(p1^3) / 2.0
// parameter 8 is set to the absolute value of the cube of 
//   parameter 1 divided by 2.0
XSPEC> newpar 5 = cos(p1) + sin(p3)
// parameter 5 is set to the cosine of parameter 1 plus the sine 
//   of parameter 3
XSPEC> newpar 3 = log(mymodel:p1)
// parameter 3 is set to the log (base 10) of parameter 1 in the
//   mymodel model
XSPEC> untie 6 
// Makes parameter 6 independent of parameter 3 and a free
//  parameter.
XSPEC> newpar 6 upper = p3
// Parameter 6 may not exceed parameter 3, which moves in the fit.
XSPEC> newpar 6 upper none
// Back to parameter 6's numeric upper limit.
XSPEC> newpar comp 3 group 2 = comp 1 group 1
// Every parameter of component 3 in data group 2 is linked to its
//   counterpart in component 1, data group 1.
```
