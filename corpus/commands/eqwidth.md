---
name: eqwidth
aliases: [xeqwidth]
also_documents: []
source: XSeqwidth.tex
---

# eqwidth

**determine equivalent width**

Determine the equivalent width of a model component.

**Syntax:** `eqwidth` [[range <frac range>] [<model name>:]<model component number>] 
[err <number> <level>| noerr]

The command calculates the integrated photon flux produced by an additive 
model component (combined with its multiplicative and/or convolution 
pre-factors) (FLUX), the location of the peak of the photon spectrum (E), 
and the flux (photons per keV) at that energy of the continuum (CONTIN). 
The equivalent width is then defined as {EW = FLUX / CONTIN} in units of 
keV.  New for XSPEC12:  the continuum is defined to be the contribution 
from all other components of the model.  

There are certain models with a lot of structure where, were they the 
continuum, it might be inappropriate to estimate the continuum flux at a 
single energy. The continuum model is integrated (from $E(1-<frac range>)$ 
to $E(1+<frac range>)$. The initial value of `<frac range>` is 0.05 
and it can changed using the `range` keyword.

The `err/noerr` switch sets whether errors will be estimated on 
the equivalent width. The error algorithm is to draw parameter values from 
the distribution and calculate an equivalent width.  `<number>` of sets 
of parameter values will be drawn. The resulting equivalent widths are 
ordered and the central `<level>` percent selected to give the error
range.  You can get the full array of simulated equivalent width values 
by calling `tclout eqwidth` with the `errsims` option 
(see `tclout` command).

When Monte Carlo Markov Chains are loaded (see `chain` command), they 
will provide the distribution of parameter values for the error estimate.  
Otherwise the parameter values distribution is assumed to be a 
multivariate Gaussian centered on the best-fit parameters with sigmas from 
the covariance matrix. This is only an approximation in the case that 
fit statistic space is not quadratic. 

**Examples:**
  
The current model is assumed to be $M_1(A_1+A_2+A_3+A_4+M_2(A_5))$, where the 
$M_x$ models are multiplicative and the $A_x$ models are additive.

```
XSPEC12> eqwidth 3
// Calculate the total flux of component M1A2 (the third 
// component of the model with its multiplicative pre-factor)
// and find its peak energy (E). The continuum flux is
// found by the integral flux of M1(A1+A3+A4+M2(A5)), using the 
// range of 0.95E to 1.05E to estimate the flux.
XSPEC12> eqwidth range .1 3
// As before, but now the continuum is estimated from 
// its behavior over the range 0.9E to 1.1E.
XSPEC12> eqwidth range 0 3
// Now the continuum at the single energy range (E) 
// will be used.
XSPEC12> eqwidth range .05 2
// Now the component M1A1 is used as the feature, and 
// M1(A2+A3+A4+M2(A5)) are used for the continuum.  The range 
// has been reset to the original value.
XSPEC12> eqwidth 1
// Illegal, as M1 is not an additive component.
```
