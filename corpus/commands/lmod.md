---
name: lmod
aliases: [xlmod]
also_documents: []
source: XSlmod.tex
---

# lmod

**load a package of local models**

The `lmod` command loads a user model package. Further details are 
given in Appendix AppendixAddModels. 

**Syntax:** `lmod` <name> [<directory>]

As with `initpackage`, the `<name>` argument is the name of the 
model package being loaded, and the `<directory>` is its location, 
defaulting to the setting of LOCAL_MODEL_DIRECTORY given in the user's 
Xspec.init file. 

`lmod` performs the following tasks:

- loads the library corresponding to the package named `<name>`

- reads the model description file supplied by the `initpackage` command for the library

- adds the new model components to the list of models recognized by the `model` command

Note that `lmod` requires that the user has write-access to 
`<directory>` (please see Appendix AppendixAddModels for details).

This command is now also supported on Cygwin.
