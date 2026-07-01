---
name: identify
aliases: [xidentify]
also_documents: []
source: XSidentify.tex
---

# identify

**identify spectral lines**

List possible lines in the specified energy range.

**Syntax:** `identify` <energy> <delta_energy> <redshift> <line_list>

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
This can be done with the ftgetmodeldata tool. See 
[https://heasarc.gsfc.nasa.gov/docs/software/xspec/modeldata.html](https://heasarc.gsfc.nasa.gov/docs/software/xspec/modeldata.html) 
for more details on model data files.

    
- `bearden`: use `bearden` for the `modelname` parameter in ftgetmodeldata.

- `mekal`: the line file will be downloaded along with the required mekal model data files when `modelname` is any of the mekal family of models.

- `apec`: the line file will be downloaded along with the required apec model data files when `modelname` is any of the apec family of models.

- `spex`: the line file will be downloaded along with the required spex model data files when `modelname` is any of the spex family of models.
