---
name: gain
aliases: [xgain]
also_documents: [gainoff, gainfit, gainnofit]
source: XSgain.tex
---

# gain

**modify a response file gain**

Modify a response file gain, in a particularly simple way.  ***CAUTION***  
This command is to be used with extreme care for investigation of the 
response properties.  To properly fit data, the response matrix should be 
recalculated explicitly (outside of XSPEC) using any modified gain 
information derived.

The `gain` command shifts the energies on which the response matrix 
is defined and shifts the effective area curve to match.  The effective 
area curve stored by XSPEC is either the ARF, if one was in use, or is 
calculated from the RSP file as the total area in each energy range.  This 
means that if there are sharp features in the response then these will only 
be handled correctly by the gain command if they are in the ARF or if no ARF 
is input.  The new energy is calculated by

E' = E/{`<slope>`} - `<intercept>`
 
 where `<intercept>` is in units of keV.

 p{} p{---6}}
**Syntax:** & **gain** & `[<sourceNum>:]<specNum> <slope> <intercept>`

 & **gain** & `fit [[<sourceNum>:]<specNum>]`

 & **gain** & `nofit {[[<sourceNum>:]<specNum>]| all}`

 & **gain** & `off`

The first variant of the gain command shown above will apply the gain shift 
specified by the `<slope>` and `<intercept>` parameters to the 
response belonging to spectrum `<specNum>`, and optionally specified 
`<sourceNum>` if the data is analyzed with multiple models.   The 
initial default `<specNum>` is 1; later, the default is the number of 
the spectrum last modified.  Initially, all responses are assumed to have 
nominal gains, determined implicitly by the data in the response files.  
This is equivalent to a `<slope>` of 1 and an `<intercept>` of zero.  
All responses can be reset back to this original state by entering `gain off`.  
Note that in this mode of usage, the slope and intercept values do NOT become 
variable fit parameters.  They are simply fixed values used to modify the response.

The `gain fit` mode is used when the user wishes to have the slope and 
intercept parameters determined by the results of a fit.  The `<specNum>` 
and optional `<sourceNum>` parameters specify to which response the fit 
gain values are to be applied.  These may be omitted only if a single spectrum 
is loaded, with a single model source.  Otherwise at least a spectrum number 
is required.  The user will then be prompted for slope and intercept parameter 
information in the same way as model parameters are normally entered.  These 
values are then immediately applied to the response, and will be adjusted 
the next time a fit is run.  

Gain fit parameters belong to the more general category of **response parameters** 
in XSPEC, and may be modified using an equivalent set of commands to those used 
for regular model parameters.  The command names are the same except prefixed 
by the letter **'r'**:

|p{}|}

XSPEC commands for editing/viewing model parameters & Equivalent commands for gain (or response) parameters)

newpar & rnewpar 

freeze & rfreeze 

thaw & rthaw 

untie & runtie 

error & rerror 

model & rmodel 

show par & show par, show rpar 

For example after assigning gain fit parameters to source 1 of spectrum 1 
(with `gain fit 1`):

```
XSPEC12> rfreeze 1
XSPEC12> rnewpar 2 .05
XSPEC12> show rpar

Response parameters defined:
========================================================================
Source No.: 1
Rpar Spectrum Rmodel   Rpar_name  Unit   Value

   1     1    gain     slope             1.00000      frozen
   2     1    gain     offset            5.00000E-02  +/-  0.0          
________________________________________________________________________
```

Rnewpar can also link gain parameters to one another and can adjust the hard 
and soft parameter limits, as newpar does for model parameters.  The default 
gain parameter hard limits are hardcoded in XSPEC, but these can be overridden 
by setting GSLOP_MIN, GSLOP_MAX, GOFFS_MIN, and GOFFS_MAX keywords in the 
matrix extension of your response file.
 
The gain operation itself belongs to the category of **response functions**, 
which in future versions of XSPEC may be defined with `rmodel` just as 
regular XSPEC model functions are defined with `model`.  Though `gain` 
is currently the only available response function, the following command will work:

```
// Apply gain to the response belonging to source 2 of spectrum 1
XSPEC12>rmodel 2:1 gain
```

which is equivalent to:

```
XSPEC12>gain fit 2:1
```

The `nofit` argument switches off the fitting and leaves the gain at 
the current values of the parameters.  Unless the argument `all` is 
given, it is applied to a single response specified by `<specNum>` and 
optional `<sourceNum>`.  As with `gain fit`, both arguments may be 
omitted if only a single spectrum with 1 source is loaded.  When `all` 
is specified, fitting is switched off for the gain parameters of all responses.  
`gain off` will switch off fitting for all gain parameters, and will 
reset all of them to their nominal value.  

Whenever a new response file is defined for a spectrum, the response will return 
to the `nofit` state with nominal value.  The `ignore` and 
`notice` commands however will not affect the current gain of the response.  
THE GAIN COMMAND IS NOT CURRENTLY IMPLEMENTED FOR DUMMY RESPONSES.  

**Examples:**

```
XSPEC12>gain 1 0.98
// The response belonging to spectrum 1 is adjusted with a 
// slope of 0.98. The 1 may be omitted if only 1 spectrum 
// (with 1 source) is loaded.  
XSPEC12>gain 1,,.03
// The offset also is moved now by 0.03 keV.
XSPEC12>gain 2:4 1.1 0.1
// The response belonging to source number 2, spectrum 4, is 
// adjusted with slope 1.1 and offset 0.1 keV.  
XSPEC12>gain off
// The above 2 responses, and any others that have been adjusted,
// are reset to slope 1.0, offset 0.0.
XSPEC12> gain fit 3
// Variable fit parameters are created for spectrum 3 response. 
// User will be prompted for starting fit parameter values of 
// slope and offset.
XSPEC12> fit
// Best fit gain values will now be determined for and applied 
// to spectrum 3 response.
XSPEC12> gain nofit 3
// Spectrum 3 response will retain its current gain values, 
// but values will not be adjusted during future fits.  
```

NOTE: Current gain information may be easily viewed with the `show response` 
command.  Gain fit parameters may also be viewed with the `show par`  
or `show rpar` commands.

**Historical Notes:**

The gain command has been slightly revised for XSPEC12.  Previously when a user 
entered a gain command, it was generally interpreted to apply to an entire **model**.  
This new implementation clearly defines an applied gain as belonging to a 
particular **response**.  It also offers less ambiguity for dealing with 
XSPEC12's multiple models scheme.  So for example if 2 spectra are loaded, each 
in its own data group, and the user enters a `gain fit` command,  under 
the old system they would be prompted for 2 sets of parameters since the model 
is applied to 2 data groups.  With the new system, the user specifies which 
particular response (belonging to either spectrum 1 or 2) they wish to apply 
the gain fit to, and are then prompted for just the 1 set of gain parameters 
for that response.  This is more clearly demonstrated with the examples above.    
The new command options `gain nofit` **all** and `gain off` are also described above.  

***** NOTE: Backwards incompatible syntax change *****

Beginning with XSPEC 12.5.1, `gain` parameters must be specified as
[<sourceNum>:]<specNum> and NOT <specNum>[:<sourceNum>].  This
reversal was made so that the gain command conforms to the [<sourceNum>:]<specNum>
usage in other XSPEC commands, such as `response` and `arf`.
