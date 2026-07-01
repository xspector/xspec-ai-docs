---
name: lumin
aliases: [flux, xflux, xlumin]
also_documents: []
source: XSlumin.tex
---

# lumin

**calculate luminosities**

Calculate the luminosity of the current model for a given redshift and 
source frame energy range.

**Syntax:** `lumin` [<lowEnergy>] [<hiEnergy>] [<redshift>] [err 
<number> <level>| noerr]

where `<lowEnergy>` and `<hiEnergy>` are the source frame energies 
over which the luminosity is calculated and `<redshift>` is the 
source redshift. Initial default values are 2 to 10 keV for 0 redshift. 
The luminosity is given in units of ergs/s. The energy range redshifted 
to the observed range must be contained by the range covered by the 
current spectra (which determine the range over which the model is evaluated). 
Values outside this range will be automatically reset to the extremes. 
Note that the energy values are two separate arguments and are NOT connected 
by a dash (see parameter ranges in the freeze command description). 

The `lumin` will be calculated for all loaded spectra.  If no spectra are 
loaded (or none of the loaded spectra have a response), the model is 
evaluated over the energy range determined by its dummy response.  
(In XSPEC12, models are automatically assigned default dummy responses when 
there is no data, so the `dummyrsp` command need not be given.) If more 
than 1 model has been loaded, whichever model the user has specified to 
be the active one for a given source is the one used for the `lumin` 
calculation. 

The results of a `lumin` command may be retrieved by the
`tclout lumin` `<n>` command where `<n>` is the
particular spectrum of interest.  If `lumin` was calculated for
the case of no loaded spectra, the results can be retrieved by
`tclout lumin` with the `<n>` argument omitted.

The `err/noerr` switch sets whether errors will be estimated on the 
luminosity. The error algorithm is to draw parameter values from the 
distribution and calculate a luminosity. `<number>` of sets of 
parameter values will be drawn. The resulting luminosities are ordered 
and the central `<level>` percent selected to give the error range.  
You can get the full array of simulated lumin values by calling `tclout lumin` 
with the `errsims` option (see `tclout` command).

The parameter values distribution is assumed to be a multivariate Gaussian 
centered on the best-fit parameters with sigmas from the covariance matrix. 
This is only an approximation in the case that fit statistic space is not 
quadratic. 

There is also a model component `clumin` which can be used to 
estimate luminosities and errors for part of the model. For instance, defining 
the model as `wabs(pow + clumin(ga))` provides a fit parameter which gives 
the luminosity in the gaussian line.

**Examples:**

The current data have significant response to data within 1 to 18 keV.

```
XSPEC> lumin,,,0.5 
//Calculate the current model luminosity over the default range 
//for z=0.5
XSPEC> lumin 6.4 7.0
//Calculate the current luminosity over 6.4 to 7 keV.
```
