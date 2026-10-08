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

The package is loaded directly, the same mechanism PyXspec's
`AllModels.lmod` uses: the library is opened and the entry point
``<name>`_xscoreInit` is called.  A package built by an
`initpackage` from an XSPEC release before 13.0 has no such entry point
and is refused with a message asking for it to be rebuilt.

Before that entry point is called, `lmod` checks which version of the
local-model contract the package was built against (the version
`initpackage` records in it; see ``The local-model contract'' in
Appendix AppendixAddModels).  A package built for a different major
version, or for a newer minor version than this XSPEC implements, is refused
with a message asking for it to be rebuilt with `initpackage`.  A
package built before the contract was versioned carries no version; it is
loaded, with a warning asking for a rebuild.

A package whose library still calls Fortran routines that are now in the
modules `xsfortran` and `xsfortfuncwrappers` in the
pre-12.15.1 way is refused before it is loaded, with the same report `initpackage` gives
and the `xsmigrate_local_model` command that fixes it (see
``Migrating Fortran local models from 12.14 and earlier'' in
Appendix AppendixAddModels); loaded, it would stop XSPEC at its first
evaluation.  The check needs `nm` and is skipped without it.

A built package directory may be moved or copied: the package reads the
model.dat file beside its library, falling back to the path it was
built with.

This command is now also supported on Cygwin.
