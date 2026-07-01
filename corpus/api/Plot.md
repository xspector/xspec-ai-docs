---
class: PlotManager
singleton: Plot
module: plot.py
---

# Plot

Singleton instance `Plot` (class `PlotManager`).

**Xspec plotting class.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| add | — | get/set | Turn on/off the display of individual additive |
| area | — | get/set | Toggle displaying the data divided by the response |
| background | — | get/set | Toggle displaying the background spectrum (if any) |
| commands | — | get/set | Custom plot commands to be appended to Xspec-generated |
| device | str | get/set | The plotting device name [string]. |
| perHz | — | get/set | Toggle displaying Y-axis units per Hz when using |
| redshift | — | get/set | Apply a redshift to the X-axis energy or wavelength |
| splashPage | — | get/set | When set to False, the usual XSPEC version and build data |
| xAxis | str | get/set | X-Axis Units [string]. |
| xLog | — | get/set | Set the x-axis to logarithmic or linear for energy or |
| yLog | — | get/set | See xLog. |

## Methods

- `__init__(deviceStr)`
- `__call__(*panes)` — Display the plot.
- `addCommand(cmd)` — Add a plot command [string] to the end of the plot commands list.
- `contourLevels()` — Return a list of the values of the drawn levels in a contour plot.
- `delCommand(num)` — Remove a plot command by (1-based) number [int].
- `iplot(*panes)` — Display the plot and leave it in interactive plotting mode.
- `labels(plotWindow=1)` — Get the X, Y, and Title labels for the specified plot window.
- `noID()` — Turn off the plotting of line IDs.
- `setGroup(groupStr)` — Define a range of spectra to be in the same plot group.
- `setID(temperature=None, emissivity=None, redshift=None)` — Switch on plotting of line IDs.
- `setRebin(minSig=None, maxBins=None, groupNum=None, errType=None)` — Define characteristics used in rebinning the data (for plotting
- `show()` — Display current plot settings
- `x(plotGroup=1, plotWindow=1)` — Return a list of X-coordinate data values for a plot group and plot window
- `xErr(plotGroup=1, plotWindow=1)` — Return a list of X-coordinate errors for a plot group and plot window
- `y(plotGroup=1, plotWindow=1)` — Return a list of Y-coordinate data values for a plot group and plot window
- `yErr(plotGroup=1, plotWindow=1)` — Return a list of Y-coordinate errors for a plot group and plot window
- `z()` — Return a 2D list of the grid values for a 2D contour plot
- `model(plotGroup=1, plotWindow=1)` — Return a list of Y-coordinate model values for a plot group and plot window
- `backgroundVals(plotGroup=1, plotWindow=1)` — Return a list of background data values for a plot group and plot window
- `addComp(addCompNum=1, plotGroup=1, plotWindow=1)` — Return a list of Y-coordinates for a particular add component of a model
- `nAddComps(plotGroup=1, plotWindow=1)` — Return the number of add component plots for a given plot group.
