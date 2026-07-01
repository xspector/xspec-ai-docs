---
name: save
aliases: [xsave]
also_documents: []
source: XSsave.tex
---

# save

**save the current session commands**

Save aspects of the current state to a command file.

**Syntax:** `save` <option>  <filename>

If no `<filename>` is given, then the file savexspec.xcm is created. 
If you don't give the extension to the file name the default is .xcm.
The values of `<option>` allowed are `model`, `files`,
and `all`. The `model` option writes out commands to recreate 
the current model and parameter values; the `files` option writes out 
commands to read-in the current spectra, and the `all` option does 
both of the above. The default option is `model`. To recover the 
saved context use the command:

```
XSPEC12>@filename
```

**Examples:**

```
XSPEC12> save model fname 
// Write out model commands to the file fname.xcm
XSPEC12> save
// Same as above, but save into file savexspec.xcm.
XSPEC12> save files fname
// Write out data file commands.
```
