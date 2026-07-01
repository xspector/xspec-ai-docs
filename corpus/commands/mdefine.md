---
name: mdefine
aliases: [xmdefine]
also_documents: []
source: XSmdefine.tex
---

# mdefine

**define a simple model using an arithmetic expression**

**Syntax:** `mdefine` <name> [<expression> [: [<type>] [<emin> <emax>]]]

where `<name>` = the name of the model.  If `<name>` is a previously 
defined model with `mdefine`, the current definition will overwrite 
the old one, and the user is warned. If it is a built-in model, 
the user will be asked to use a different name.

`<expression>` = a string of arithmetic expressions. Simple rules for expressions:

- The energy term must be 'e' or 'E' in the expression.  Other words, 
which are not numerical constants nor internal functions, are assumed to be 
model parameters.

- If a convolution model varies with the location on the spectrum to be 
convolved, the special variable '.e' or '.E' may be used to refer to the 
convolution point.

- The expression may contain spaces for better readability. 

`<type>` = user may optionally specify the type of the model. The valid 
types are `add, mul, con`. Mixing models are not yet implemented.
Please note that the character ':' must be used to separate the 
options from the `<expression>`. If `<type>` is not given, the default  
is `add`. 

`<emin>` `<emax>` = user may also specify the  minimum and 
maximum energy values for the model. The default values are 1.e-20 and 1.e+20, respectively. 

Note that `mdefine` can also be used to display and delete previously 
defined models:  

- To display the name, type and expression of all previously defined models: 

```
XSPEC12>mdefine
```

- To display the name, type and expression of a previously defined model by the name, MNAME:

```
XSPEC12> mdefine MNAME
```

- To delete a previously defined model by the name, MNAME:

```
XSPEC12> mdefine MNAME :
```

**Operators:**

The following operators are recognized in an expression:

+ & = & plus operator

- & = & minus operator

$\ast$ & = & multiplying operator

/ & = & dividing operator

$\ast\ast$ & = & exponentiation operator

^ & = & exponentiation operator

**Functions:**

The following internal functions are supported where expr is a vector
(e.g. E):

4{c}{**unary functions**}

EXP   & (expr) & = & exponential

SIN   & (expr) & = & sine in radians
  
SIND  & (expr) & = & sine in degrees
 
COS   & (expr) & = & cosine in radians
  
COSD  & (expr) & = & cosine in degrees
 
TAN   & (expr) & = & tangent in radians
  
TAND  & (expr) & = & tangent in degree
 
SINH  & (expr) & = & hyperbolic sine in radians
  
SINHD & (expr) & = & hyperbolic sine in degrees
 
COSH  & (expr) & = & hyperbolic cosine in radians
  
COSHD & (expr) & = & hyperbolic cosine in degrees
 
TANH  & (expr) & = & hyperbolic tangent in radians
  
TANHD & (expr) & = & hyperbolic tangent in degrees
 
LOG   & (expr) & = & base 10 log
 
LN    & (expr) & = & natural log

SQRT  & (expr) & = & square root

ABS   & (expr) & = & absolute value

INT   & (expr) & = & integer part

ASIN  & (expr) & = & inverse sine in radians
  
ACOS  & (expr) & = & inverse cosine in radians
  
ATAN  & (expr) & = & inverse tangent in radians
  
ASINH & (expr) & = & inverse hyperbolic sine in radians
  
ACOSH & (expr) & = & inverse hyperbolic cosine in radians
  
ATANH & (expr) & = & inverse hyperbolic tangent in radians
  
ERF   & (expr) & = & error function

ERFC  & (expr) & = & complementary error function

GAMMA & (expr) & = & gamma function

LEGENDRE2 & (expr) & = & 2nd-order Legendre polynomial

LEGENDRE3 & (expr) & = & 3rd-order Legendre polynomial

LEGENDRE4 & (expr) & = & 4th-order Legendre polynomial

LEGENDRE5 & (expr) & = & 5th-order Legendre polynomial

SIGN  & (expr) & = & -1 if negative, +1 if positive 

HEAVISIDE & (expr) & = & 0 if negative, +1 if positive 

BOXCAR    & (expr) & = & +1 between 0 and 1, 0 otherwise 

MEAN  & (expr) & = & mean value of the vector expression

DIM   & (expr) & = & dimension of the vector expression
 
SMIN  & (expr) & = & minimum value of the vector expression

SMAX  & (expr) & = & maximum value of the vector expression

}
4{c}{**binary functions**}

ATAN2 & (expr1, expr2) & = & principal value of the arc tan of expr1/expr2 in radians

MAX   & (expr1, expr2) & = & maximum of the two expressions

MIN   & (expr1, expr2) & = & minimum of the two expressions

**XSPEC Model Functions:**

Any XSPEC model function (including models previously defined using
mdefine) can be used in an mdefine expression. The complete name of
the function must be used (no abbreviations) and the name should be
followed by parentheses enclosing the function parameter values
separated by commas. The energy is assumed and should not be included
within the parentheses. For additive models the normalization
parameter is not included within the parentheses but can obviously be
added as a parameter in the expression.

**Examples:**

//  define a model named "dplaw" with 3 parameters, p1, p2, f  
XSPEC12> mdef dplaw E**p1 + f*E**p2

// define a model named "junk" with 2 parameters (a, b)
XSPEC12> mdef junk a*e+b*log(e)/sin(e)  

// define a model named "junk2" with 1 parameter, a; the option 
//   following ":" says that it will be a multiplicative model. 
XSPEC12> mdef junk2  exp(-a*e) : mul   

// define a model named "junk3" with 1 parameter, B, options 
//   following ":" says that this will be a multiplicative model 
XSPEC12> mdef junk3  0.2+B*e : mul 

// try to define a blackbody model with name "bb", you get warning: 
XSPEC12> mdef bb E**2/T**4/(exp(E/T)-1) 

        ***Warning: bb is a pre-defined model
        Please use a different name for your model.

// this defines a Gaussian convolution model with sigma varying with 
//   square root of energy.
XSPEC12> mdef sg  exp(-E^2/(2*A*.E)) / sqrt(6.283*A*sqrt(.E))  :  con
                                        
// delete junk2 
XSPEC12> mdef junk2 :

// define a two-temperature model with common abundance and redshift
XSPEC12> mdef twotemp (1-f)*apec(T1,A,z) + f*apec(T2,A,z)

// define a pexrav model with parameter inclination instead of its cosine
XSPEC12> mdef mypex pexrav(g,f,refl,z,A,FeA,cos(Incl))

// define a model based on two other mdefine models
XSPEC12> mdef mymod junk3(p1)*junk(p2,p3)

// display all user-defined models
XSPEC12> mdef

Name ---- Type ---- Expression -----
dplaw     add       E**p1+f*E**p2
junk      add       a*E+b*LOG(E)/SIN(E)
junk3     mul       a+b*E
mymod     add       junk3(p1)*junk(p2,p3)
mypex     add       pexrav(g,f,refl,z,A,FeA,cos(Incl))
sg        con       EXP(-E^2/(2*A*.E))/SQRT(6.283*A*SQRT(.E))
twotemp   add       (1-f)*apec(T1,A,z)+f*apec(T2,A,z)
-----------------------------------------
