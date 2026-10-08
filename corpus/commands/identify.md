---
name: identify
aliases: [xidentify]
also_documents: []
source: XSidentify.tex
---

# identify

**identify spectral lines**

List possible lines in the specified energy range, from a line list or from
the current model.

**Syntax:** `identify` <energy> <delta_energy> <redshift> <line_list>

**Syntax:** `identify fit` <energy> <delta_energy> [top <n>] [group <g>] [model <name>]

The first form searches a line list, as described below. The second,
`identify fit`, lists the lines the current model actually emits, and
is described at the end of this entry.

The energy range searched is `<energy>` $\pm \Delta$`<energy>`
(keV) in the rest frame of the source.  If working in wavelength mode, as 
set by the setplot command, then the `<energy>` and `<delta energy>` 
parameters should be entered as wavelengths (in Angstroms).  

`<line list>` specifies the list of lines to be searched.  The options are:

    
- `bearden`, which searches the Bearden compilation of fluorescence lines 
        (Bearden, J.A., 1967, Rev.Mod.Phys. 39, 78)

- `mekal`, which uses the lines from the mekal model (q.v.)

- `apec`, which uses the APEC 
        [http://www.atomdb.org/](http://www.atomdb.org/) 
        line list. The apec option takes an additional two arguments: the temperature of 
        the plasma (keV) and a minimum emissivity of lines to be shown. If the command 
        `xset` has been used to set APECROOT, then `identify` uses the APECROOT 
        value to define the new atomic physics data files. See the help on the `apec` model 
        for details.

- `spex`, which uses the SPEX 
        [https://spex-xray.github.io/spex-help/](https://spex-xray.github.io/spex-help/) 
        line list. The spex option takes an additional two arguments: the temperature of 
        the plasma (keV) and a minimum emissivity of lines to be shown. If the command 
        `xset` has been used to set SPEXROOT, then `identify` uses the SPEXROOT 
        value to define the new atomic physics data files. See the help on the `apec` model 
        for details.

The line list files must be downloaded to the local machine before use.
This can be done with the ftgetmodeldata tool.  For more details on model
data files see

https://heasarc.gsfc.nasa.gov/docs/software/xspec/modeldata.html.

    
- `bearden`: use `bearden` for the `modelname` parameter in ftgetmodeldata.

- `mekal`: the line file will be downloaded along with the required mekal model data files when `modelname` is any of the mekal family of models.

- `apec`: the line file will be downloaded along with the required apec model data files when `modelname` is any of the apec family of models.

- `spex`: the line file will be downloaded along with the required spex model data files when `modelname` is any of the spex family of models.

*identify fit**

`identify fit` lists the lines that the AtomDB components of the
current model emit at the current parameter values: `apec` and its
variants, the multi-temperature models (`cevmkl`, `wdem`,
), the NEI models (`nei`, `gnei`, `pshock`,
) and the resonance-scattering models. Each additive component is
evaluated once more, on its own grid over the window, with line recording
switched on for that evaluation only, so the list always matches the current
parameters and fitting is not slowed.
`setplot id model` (see `setplot`) labels a plot with the same
lines.

`<energy>` $\pm$ `<delta energy>` is the window in the observed
frame, in keV, or in Angstrom when `setplot` `wave` is in effect.
There is no redshift argument: each component's own redshift is applied. One
row is printed per line: the component number and name, the ion (e.g. Fe
XXV), the upper and lower AtomDB level numbers (the identifiers
`xset` `APECREMOVELINES` takes), the rest and observed energy (or
wavelength), the photon flux (photons cm$^{-2}$ s$^{-1}$) and the line's
percentage of the AtomDB components' photon flux in the window. Rows are
sorted by flux, and the strongest `<n>` are printed (`top`,
default 20). A closing line gives the window's total, line and continuum
fluxes. `group` chooses the data group whose parameter values are
used (default 1), and `model` a named model (default the unnamed one).

Lines removed with `APECREMOVELINES` are not emitted and are not
listed; the weak lines AtomDB folds into its pseudo-continuum count as
continuum. The fluxes are those the plasma components themselves emit:
absorption, and any other multiplicative or convolution component applied
outside them, is not applied. The command is refused when the model has no
AtomDB component. For example, for `model tbabs*apec`:

```
XSPEC12> identify fit 6.66 0.06 top 4
```

lists the Fe XXV w, z, y and x lines and their shares of the 6.60--6.72 keV
flux (for a redshift of zero). In PyXspec, `AllModels.identifyLines(energy, delta, top, group,
model)` prints the same report and returns the lines, and
`Model.emittedLines(loKeV, hiKeV)` returns them without printing.
