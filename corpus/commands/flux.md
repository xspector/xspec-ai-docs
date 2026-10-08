---
name: flux
aliases: [lumin, xflux, xlumin]
also_documents: []
source: XSflux.tex
---

# flux

**calculate fluxes**

Calculate the flux of the current model between certain limits.

**Syntax:** `flux` [<lowEnergy> [<hiEnergy>]] [err 
<number> <level>| noerr] [zero <param list>]

where `<lowEnergy>` and `<hiEnergy>` are the values over which 
the flux is calculated. Initial default values are 2 to 10 keV.

The flux is given in units of photons $cm^{-2} s^{-1}$ and ergs $cm^{-2} s^{-1}$. 
The energy range must be contained by the range covered by the current spectra 
(which determine the range over which the model is evaluated). Values outside 
this range will be reset automatically to the extremes. Note that the energy 
values are two separate arguments, and are NOT connected by a dash. (see 
parameter ranges in the `freeze` command).  

The flux will be calculated for all loaded spectra.  If no spectra are loaded 
(or none of the loaded spectra have a response), the model is evaluated over 
the energy range determined by its dummy response.  (In XSPEC12, models are 
automatically assigned default dummy responses when there is no data, so the 
dummyrsp command need not be given.) If more than 1 model has been loaded, 
whichever model the user has specified to be the active one for a given 
source is the one used for the flux calculation. 

The results of a `flux` command may be retrieved by the `tclout flux` 
`<n>` command where n is the particular spectrum of interest.  If the 
flux was calculated for the case of no loaded spectra, the results can be 
retrieved by `tclout flux` with the `<n>` argument omitted.  

The `err/noerr` switch sets whether errors will be estimated on the 
flux. The error algorithm is to draw parameter values from the distribution 
and calculate a flux. `<number>` of sets of parameter values will be 
drawn. The resulting fluxes are ordered and the central `<level>` 
percent selected to give the error range.  You can get the full array of 
simulated flux values by calling `tclout flux` with the `errsims` 
option (see `tclout` command).

When Monte Carlo Markov Chains are loaded (see `chain` command), they 
will provide the distribution of parameter values for the error estimate.  
Otherwise the parameter values distribution is assumed to be a 
multivariate Gaussian centered on the best-fit parameters with sigmas 
from the covariance matrix. This is only an approximation in the case that 
fit statistic space is not quadratic.

The `zero` clause, which must come last, holds the parameters in
`<param list>` at zero for the calculation: for the point value and,
with `err`, for every set of drawn parameter values (each set is
drawn for all the variable parameters, as without `zero`, and then
the listed ones are set to zero).  The parameters are restored afterwards.
Setting the column density of an absorption component to zero gives the
unabsorbed flux and its error; setting the normalizations of the other
additive components to zero gives the flux of one component.  The list
uses the parameter-range syntax of `freeze` (`1`,
`1-3`, `mymod:4`).  Linked parameters, and parameters whose
hard limits exclude zero, are refused.  The clause is not remembered by
the next `flux` command.

There is also a model component `cflux` which can be used to
estimate fluxes and errors for part of the model. For instance, defining 
the model as `wabs(pow + cflux(ga))` provides a fit parameter which gives 
the flux in the gaussian line.  `cflux` makes the flux a fit
parameter, so its error comes from the fit itself (`error`); the
`zero` clause needs no change to the model, and its error comes
from the same parameter draws as `err`.

**Examples:**
  
The current data have significant responses to data within 1.5 to 18 keV.

```
XSPEC> flux
//Calculate the current model flux over the default range.
XSPEC> flux 6.4 7.0
//Calculate the current flux over 6.4 to 7 keV
XSPEC> flux 1 10
//The flux is calculated from 1.5 keV (the lower limit of the 
//current response's sensitivity) to 10 keV.
XSPEC> model phabs(powerlaw)
XSPEC> fit
XSPEC> flux 2 10 err 1000 90 zero 1
//The unabsorbed 2-10 keV flux (the phabs column density, parameter
//1, held at zero) with its 90% range from 1000 parameter draws.
```
