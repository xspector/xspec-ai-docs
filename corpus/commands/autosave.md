---
name: autosave
aliases: [xautosave]
also_documents: []
source: XSautosave.tex
---

# autosave

**set frequency of saving commands**

Set or disable autosave, which saves the XSPEC environment to a file
periodically.

**Syntax:** `autosave` <option>

where `<option>` is either `off` or a non-zero positive integer N.
If the option is `off`, then auto-saving is disabled. If the option is N,
the XSPEC environment is saved every N commands. 
The saving of the environment is equivalent to the command

```
XSPEC>save all xautosav.xcm .,
```

i.e. both the file and model information is saved to the file xautosav.xcm, 
placed in the directory  /.xspec/cache.  Thus in case of an unexpected crash,
the state of XSPEC before the crash can be restored by running @xautosav.xcm.
The default value for the auto-save option is 1.
