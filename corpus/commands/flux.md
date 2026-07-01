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
<number> <level>| noerr]

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

There is also a model component `cflux` which can be used to 
estimate fluxes and errors for part of the model. For instance, defining 
the model as `wabs(pow + cflux(ga))` provides a fit parameter which gives 
the flux in the gaussian line.

**Examples:**
  
The current data have significant responses to data within 1.5 to 18 keV.

```
XSPEC12> flux
//Calculate the current model flux over the default range.
XSPEC12> flux 6.4 7.0
//Calculate the current flux over 6.4 to 7 keV
XSPEC12> flux 1 10
//The flux is calculated from 1.5 keV (the lower limit of the 
//current response's sensitivity) to 10 keV.
```
