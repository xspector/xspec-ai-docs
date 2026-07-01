---
name: newpar
aliases: [rnewpar, xnewpar, xrnewpar]
also_documents: [rnewpar]
source: XSnewpar.tex
---

# newpar (and rnewpar)

**change parameter values**

Adjust one or more of the model parameters.

 p{} p{---6}}
**Syntax:** & **newpar** & `[<modelName>:]<index range> [<param spec list>]`

**Syntax:** & **newpar** & `[<modelName>:]<index> = <coupling expression>`

**Syntax:** & **newpar** & `0`

where:

`<param spec list>` ::= `<param value>` `<delta>` `<param range spec>` 

`<param range spec>` ::= `<hard min>` `<soft min>` `<soft max>` `<hard max>`

For **response parameters** (created with the `gain` or `rmodel` command):

 p{} p{---6}}
**Syntax:** & **rnewpar** & `[<sourceNum>:]<idx range> [<param spec list>]`

**Syntax:** & **rnewpar** & `[<sourceNum>:]<index> = <coupling expression>`

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
range of expected parameter behavior. Between the hard and soft limits, 
the parameter is made stiffer to adjustment by the minimization routine 
invoked by the `fit` command. The parameter is never allowed to 
have a value at or outside the hard limits. 

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

`XSPEC12> newpar <par> = f(<par>)`

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

If there are multiple data groups present, then the parameters of models 
associated with datagroups greater than 1 (``secondary models'') are 
coupled by default to their ``primary'' counterparts. For example, if 
there are 5 parameters in the model and 3 datagroups present, then the 
model command will prompt for 15 parameters. If the user types

```
XSPEC12> model <expression>
XSPEC12>/*
```

Then parameters 1-5 will be set to their values specified in the 
initialization (model.dat) file. Parameters 6-15 will be linked 
to their counterparts, i.e. as if the user had typed

```
XSPEC12> newpar 6 = p1
XSPEC12> newpar 7 = p2
...
XSPEC12> newpar 11 = p1
```

And so on.

**Examples:**

The total number of model parameters for the example is four.

```
XSPEC12> newpar 2 0.1
// The value of the second parameter is set to 0.1.
XSPEC12> newpar 3-4
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
XSPEC12> newpar ,,.001
// The value of the delta of the 3rd parameter (which is the default 
//   index as it was the first parameter modified in the previous 
//   newpar invocation) is set to 0.001, allowing it to be adjusted 
//   during any fits.
```

The total number of parameters for this example is eight.

```
XSPEC12> newpar 4 = 1
// The value of parameter 4 is set to the value of parameter 1. 
//   This has the consequence of model parameter 4 being frozen at the
//   value of parameter 1 during subsequent fitting procedures.
//   If model parameter 1 is a free parameter, then both parameters
//   1 and 4 change their values simultaneously in the fit procedure.
XSPEC12> newpar 4 = p3/5 + 6.7 
// The value of parameter 4 is set to the value of
//   (parameter 3/ parameter 5) plus 6.7
XSPEC12> newpar 6 = p3 * 0.1 - 9.5
// The value of parameter 6 is set to 0.1 times the 
//   value of parameter 3 minus 9.5
XSPEC12> newpar 5 = 2 + 5. 
// The value of parameter 5 is set to the value
//   of parameter 2 plus 5.
XSPEC12> newpar 8 = p1 / 4.6
// parameter 8 is set to parameter 1 divided by 4.6
XSPEC12> newpar 8 = abs(p1^3) / 2.0
// parameter 8 is set to the absolute value of the cube of 
//   parameter 1 divided by 2.0
XSPEC12> newpar 5 = cos(p1) + sin(p3)
// parameter 5 is set to the cosine of parameter 1 plus the sine 
//   of parameter 3
XSPEC12> newpar 3 = log(mymodel:p1)
// parameter 3 is set to the log (base 10) of parameter 1 in the
//   mymodel model
XSPEC12> untie 6 
// Makes parameter 6 independent of parameter 3 and a free
//  parameter.
```
