---
name: initpackage
aliases: [xinitpackage]
also_documents: []
source: XSinitpackage.tex
---

# initpackage

**initialize a package of local models**

The `initpackage` command initializes a package of local models from 
their source code and from a model component description file in model.dat 
format which defines the component's name, type, function call, and its 
parameter names and initial settings. Further details of the file format, 
function and parameter specifications are given in Appendix AppendixAddModels.

**Syntax:** `initpackage` <name> <description file> [<directory>] [-udmget | -udmget64]

The `<name>` argument names the package. For internal reasons package 
names must be lowercase: the `initpackage` command will force lower 
case and warn the user if the argument contains uppercase letters.  Also 
there should be no numerals in the package name.

The `<description file>` argument specifies the model component 
description file. The third argument `<directory>` is optional and 
specifies the location of the source code. If it is not given, the value 
of the setting LOCAL_MODEL_DIRECTORY given in the user's Xspec.init
file will be used. Finally, the `<description file>`, if not specified 
as an absolute pathname, will be read from the same directory as the 
source code.

Another optional argument is `-udmget`, for local model libraries 
containing Fortran code which makes use of XSPEC's now-obsolete udmget 
function for dynamic memory allocation.  None of the functions in XSPEC's 
built-in models library use udmget anymore, and the necessary xsudmget.cxx 
file no longer resides there.  If a user still requires this code for 
their own local models, they should add `-udmget` at the end of 
the comamnd line.  `initpackage` will then copy the files 
xsudmget.cxx and xspec.h into the user's local model directory.

`initpackage` performs the following tasks:

- reads the model description file 

- writes code that will load the new component calculation functions

- writes a makefile that will drive the compilation and installation of the new code

- invokes the compiler and builds the library.

The generated code records the version of the local-model contract the
package is built against, which `lmod` checks (see ``The local-model
contract'' in Appendix AppendixAddModels).  The generated makefile links
XSPEC's Python support library only for a package that contains Python
(`Py_`) models, so a package of compiled models also loads into a
program without Python.  A complete example package, with analytic gradients
and a check of them, is installed in $HEADAS/lib/xspec-lmod-template.

After building the library `initpackage` checks that it does not call
any of the Fortran routines XSPEC 12.15.1 moved into the modules
`xsfortran` and `xsfortfuncwrappers` the pre-12.15.1 way, which
would stop XSPEC the first time the model was evaluated.  If it does, the
command fails, naming each routine, its module, the source file that calls it,
and the `xsmigrate_local_model` command that migrates the sources (see
``Migrating Fortran local models from 12.14 and earlier'' in
Appendix AppendixAddModels).

A separate command, `lmod`, actually loads the library. This two step 
process makes it easier to determine where the user is during the 
process if compilation failures arise. Further, if the model is complete 
and working correctly, only the `lmod` command need be invoked.

`initpackage` can also be run as a stand-alone program outside 
of XSPEC.  When used like this however, after `initpackage` has 
finished the user must manually run hmake to build their library.  
XSPEC performs this part automatically using a script file.

This command is now also supported on Cygwin.  The former Cygwin-only 
static_initpackage command has been removed.
