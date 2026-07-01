---
name: setplot
aliases: [xsetplot]
also_documents: [setplotadd, setplotnoadd, setplotarea, setplotnoarea, setplotareascale, setplotnoareascale, setplotbackground, setplotnobackground, setplotchannel, setplotcommand, setplotcontimage, setplotnocontimage, setplotdelete, setplotdevice, setplotenergy, setploterrortype, setplotgroup, setplotid, setplotnoid, setplotlist, setplotrebin, setplotredshift, setplotsplashpage, setplotungroup, setplotwave, setplotxlog, setplotylog]
source: XSsetplot.tex
---

# setplot

**modify plotting parameters**

Set one of the various plot options.

**Syntax:** `setplot` <subcommand string>

where `<subcommand string>` is a keyword followed in some cases by 
arguments.  Current settings of all `setplot` items can be viewed 
with `show plot`.

- [add, noadd]

Switch on (add) and off (noadd) individual additive model components on data plots.

- [area, noarea]

After `setplot area` is entered, `plot data` and `plot ldata` 
will show the data divided by the response effective area for each particular 
channel.  `plot residuals` will necessarily also be affected by this.  
Usual plotting is restored by `setplot noarea`.  If data is associated 
with more than 1 response, the response effective area is calculated by 
simply summing the contributions from each response.

- [areascale, noareascale]

After `setplot areascale` is entered, `plot data` and `plot ldata` 
will show the data divided by the value of the AREASCAL keyword or
vector for each particular channel.  `plot residuals` will necessarily also be affected by this.  
Usual plotting is restored by `setplot noareascale`. This
option has no effect if `setplot area` is in use because the
AREASCAL values are already included in the area for these plots.

- [background, nobackground]

When running `plot data` or `plot ldata`, also show associated 
background spectra (if any).  

- [channel]

Change the x-axis on data and residual plots to channels.

- [command]

Add a PLT command to the command list.

`setplot command <PLT command>`

where `<PLT command>` is any valid PLT command. Every time you use 
`setplot command`, that command is added to the list that is passed to 
PLT when you use `plot` or `iplot`. The most common use of 
`setplot command` is to add a common label to all plots produced. 
You should be careful when using this command, because XSPEC does not check 
to see if you have entered a valid PLT command. These commands are appended 
to the list that XSPEC creates to generate the plot and so `setplot command` 
will override these values (this can either be a bug or a feature, depending 
on what you have done!). PLT uses expressions involving backslashes to
print special characters so care must be taken with these because the
Tcl interpreter also uses backslashes. Any backslash in a PLT label
must be replaced by two backslashes. This will work provided that an
abbreviation is not used for `setplot`. If an abbreviation is
used then any backslash must be replaced by four backslashes! This is
illustrated in the examples below. See also `setplot delete`
and `setplot list`. 

Example:

XSPEC12> setp co LA OT Crab  #Add the label "Crab" to future plots.
XSPEC12> setplot co LA OT 
gD
gx
u2
d  # delta chi-squared
XSPEC12> setpl co LA OT 

gD

gx

u2

d  # delta chi-squared

- [contimage,
  nocontimage]

Switch on (contimage) and off (nocontimage) the background image on
contour plots.

- [delete]

Delete a PLT command from the command list.

`setplot delete [all| <command #>-<command #>| <command #>]`

where `<command #>` is the number of a PLT command that had been 
entered previously using `setplot command`. This command is used to 
delete commands from the list passed to PLT when you use the XSPEC 
`plot` or `iplot` commands. 

- [device]

Set current plot device.

```
XSPEC12>setplot device	 <plot device>
XSPEC12>setplot device	<filename>
XSPEC12>setplot device	<filename>/{ps,cps,vps,vcps}
XSPEC12>setplot device	 none
```

If the second argument does not start with a '/' character, which indicates 
that the string represents a PGPLOT device, it is taken to be a filename for
 Postscript output, and the default postscript driver will be used. The 
 default postscript driver produces a monochrome plot in landscape orientation.
 
The filename argument can be followed by a '/' that specifies a particular 
postscript driver variant. Allowable  variants are: cps (color postscript), 
vps (monochrome portrait orientation), and vcps (color portrait orientation), 
as well as the default, ps.

A number of plot device types are supported in XSPEC. PGPLOT devices available
on Unix machines are :

/GIF & Graphics Interchange Format file, landscape orientation

/VGIF & Graphics Interchange Format file, portrait orientation

/NULL & Null device, no output

/PPM & Portable Pixel Map file, landscape orientation

/VPPM & Portable Pixel Map file, portrait orientation

/PS & PostScript file, landscape orientation

/VPS & PostScript file, portrait orientation

/CPS & Colour PostScript file, landscape orientation

/VCPS & Colour PostScript file, portrait orientation

/TEK4010 & Tektronix 4010 terminal

/GF & GraphOn Tek terminal emulator

/RETRO & Retrographics VT640 Tek emulator

/GTERM & Color gterm terminal emulator

/XTERM & XTERM Tek terminal emulator

/ZSTEM & ZSTEM Tek terminal emulator

/V603 & Visual 603 terminal

/KRM3 & Kermit 3 IBM-PC terminal emulator

/TK4100 & Tektronix 4100 terminals

/VT125DEC & VT125 and other REGIS terminals

/XDISP & pgdisp or figdisp server

/XWINDOW & X window window@node:display.screen/xw

/XSERVE & An /XWINDOW window that persists for re-use

Examples:

```
XSPEC12> setplot device /xt 
   // sets the device to the xterm.
XSPEC12> setplot device none 
   // closes the plot file.
```

- [energy]

Change the X-axis on plots to energies, and optionally change the units.

`setplot energy [<units>]`

where `<units>` is an optional string for modifying X-axis energy units.  
Valid choices currently are:  `keV, MeV, GeV`, and `Hz`, which are case-insensitive 
and can be abbreviated.  Energy units initially default to `keV`.  
The selection made here also determines the units in the
`ignore` and `notice` energy range specifiers.  

Where applicable, Y-axis units will be modified to match the X-axis selection.  
The exception is for the choice of Hz when emodel/eufspec is in Jy and 
eemodel/eeufspec in ergs/cm^2/s.

- [errortype]

Define how to calculate the error bars on plots. Note that this is
only for plots, it makes no difference to fitting.

`setplot errortype <error type> <plot group>`

The `<error type>` argument specifies how to calculate the error bars
on the plot bins. The default is `quad` which uses the original
errors on the data and sums in quadrature if channels are combined.
`sqrt` uses $\sqrt{N}$ where N is the number of counts in the
bin, `poiss-1` uses $1+\sqrt{N+0.75}$, 
`poiss-2` uses $\sqrt{N-0.25}$, and `poiss-3` is the 
arithmetic mean of `poiss-1` and `poiss-2`. If background 
is present its error is calculated by the same method then added in 
quadrature to the source error. 

- [group]

Define a range of spectra to be in the same group for plotting purposes only.

`setplot group <spectrum range>...`

where `<spectrum range>` is a range of contiguous spectra to be treated 
as a single spectrum for plotting purposes. The spectra still are fit 
individually. If multiple ranges are given, each range becomes a single 
group. Initially, all spectra read in are treated as single spectra.  
(See also `ungroup`.)

Examples:

Assume that there are five spectra currently read in, all of them ungrouped 
initially.

XSPEC12> setplot group 1-4
   //The first four spectra are treated as one group, with the fifth 
   //  spectra on its own. Thus all plots will appear to have two spectra.
XSPEC12> setplot group 1 2 3 4 
   //The spectra are reset to each be in their own group.
XSPEC12> setplot group 2-3 4-5 
   //Now there are three plot groups, being spectrum 1, by itself, and 
   //  spectra 2-3 and 4-5 as groups.
XSPEC12> setplot group 1-**
   //All the spectra are placed in a single plot group.

- [id, noid]

Switch on (id) and off (noid) plotting of line IDs.

`setplot id <temperature> <emissivity limit> <redshift> <lowEng> <highEng>`

The IDs are taken from the APEC line list for the temperature given by
the first argument. The plot only shows those lines with emissivities
above the limit set and the lines are redshifted by the amount
specified. Only lines between the low and high energy values will be
shown. If both the low and high energy values are zero then energy
range used is that plotted. When plotting with a wavelength x-axis the
low and high values given are assumed to be in wavelength units. The
APEC version is the current default unless `xset apecroot` has
been used to reset the APEC files then `setplot id` uses a
filename based on the value of `apecroot` as described in the
documentation for the `apec` model.

- [list]

List all the PLT commands in the command list.

`setplot list`

See `setplot delete` for an example of use.

- [rebin]

Define characteristics used in rebinning the data (for plotting purposes ONLY).

`setplot rebin <min significance> <max # bins> <plot group> <error type>`

In plotting the data from a spectrum (or group of spectra, see `setplot group`), 
adjacent bins are combined until they have a significant detection at least 
as large as  `<min significance>` (in $\sigma$).However, no more than 
`<max # bins>` may be so combined. Initial values are 0. and 1, 
respectively. This argument effects only the presentation of the data in 
plots. It does not change the fitting, in particular the number of degrees 
of freedom. The values given are applied to all the plotted data in the 
plot group specified as the final argument. To change the rebinning 
simultaneously for all the plot groups give a negative value of the plot group.

The `<error type>` argument specifies how to calculate the error bars
on the new bins. The default is `quad` which sums in quadrature the 
errors on the original bins. `sqrt` uses $\sqrt{N}$ where N is the 
number of counts in the new bin, `poiss-1` uses $1+\sqrt{N+0.75}$, 
`poiss-2` uses $\sqrt{N-0.25}$, and `poiss-3` is the 
arithmetic mean of `poiss-1` and `poiss-2`. If background 
is present its error is calculated by the same method then added in 
quadrature to the source error. 

Examples:

XSPEC12> setplot rebin 3 5 1
   //Bins in plot group 1 are plotted that have at least 3 sigma,
   // or are grouped in sets of 5 bins.
XSPEC12> setplot rebin 5 5
   //The significance is increased to 5 sigma.
XSPEC12> setplot rebin,,10,-1
   //All plotted bins can be grouped into up to 10 bins in reaching the 
   // 5 sigma significance criterion.
XSPEC12> setplot rebin ,,,sqrt
   //Uses sqrt(N) to calculate error bars.

- [redshift]

Apply a redshift to the X-axis energy and wavelength values.

`setplot redshift <z>`

This will multiply X-axis energies by a factor of (1+z) to allow for 
viewing in the source frame.  Y-axis values will be equally affected in 
plots which are normalized by energy or wavelength.  Note that this is 
not connected in any way to redshift parameters in the model (or the 
`setplot id` redshift parameter) and should only be used for 
illustrative purposes.

- [splashpage (on| off)]

When set to off, the usual XSPEC version and build date information will 
not be printed to the screen when the first plot window is initially opened.  
This is intended primarily for the HERA installation of XSPEC.

- [ungroup]

Remove previous grouping set up by `setplot group`, resetting all spectra 
to be in a distinct plot group.

- [wave]

Change the x-axis on plots to wavelength, and optionally change the units.

`setplot wave [<units>]`
`setplot wave perhz [off]`

where `<units>` is an optional string for modifying X-axis wavelength 
units.  Valid choices currently are:  `angstom, cm, micron`, and `nm`, 
which are case-insensitive and can be abbreviated.  Wavelength units 
initially default to `angstrom`.

Where applicable, Y-axis units will be modified to match the X-axis 
selection.  However this behavior can be changed by the command 
`setplot wave perhz`, which will cause Y-axis units to be in 1/Hz.  
This feature is turned off by `setplot wave perhz off`, and its 
initial setting is determined by the WAVE_PLOT_UNITS setting in the 
user's $\sim$/.xspec/Xspec.init file.  Also note that when `perhz` 
is selected, emodel/eufspec and eemodel/eeufspec will have the same 
Y-axis units as for `setplot energy hz`.

This command makes `ignore` and `notice` operate in terms of 
wavelength rather than energies.  The units setting here also determines 
the units in the `ignore` and `notice` range specifiers.

- [xlog (on| off)]

Set the x-axis to logarithmic or linear respectively for energy or wavelength 
plots. `xlog` has no effect on plots in channel space (recall 
that the default for energy plots is logarithmic: `xlog` allows the 
user to override this setting).  `xlog` and `ylog` will not 
work for model-related plots (eg. model, ufspec, and their variants) as 
their axes are always set to log scale.

- [ylog (on| off)]

Set the y-axis to logarithmic or linear respectively for energy or 
wavelength plots. For plot instructions that are explicitly logarithmic 
(`plot ldata`, `plot lcounts`) the state of the `ylog` 
setting is ignored.  `xlog` and `ylog` will not work for 
model-related plots (eg. model, ufspec, and their variants) as their axes 
are always set to log scale.
