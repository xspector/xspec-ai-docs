---
name: help
aliases: [xhelp]
also_documents: [?, helpcommand, helpmodel]
source: XShelp.tex
---

# help

**display manual or help for a specific command/theoretical model component**

Obtain help on the XSPEC commands, their syntax, and examples of their use.

**Syntax:** `help` [<topic list>]

On the first invocation of the help command, an instance of a pdf file reader
(by default Adobe Acrobat Reader) is started (a short delay may ensue), or
the XSPEC manual is accessed online. Please see the subsection ``Customizing
XSPEC'' in the XSPEC Overview section for details on how to control this
behavior. The Acrobat reader must be in the user's path. If this default is
used, then subsequent calls to `help` will use this instance to display other
help pages. `help` without arguments displays the XSPEC manual, with a bookmark
index that allows random access to the help system, or in the online mode will
open to the XSPEC manual homepage.

The design allows for users to add help files for local models and scripts to the help system if they are placed in the help search path.

**Examples:**

```
XSPEC12> help
//show the entire manual.
XSPEC12> help fit
//Go to the help text for the fit command.
XSPEC12> help model pow
//Go to the help text for the powerlaw model. 
//(Entering just "XSPEC12> model" will produce a scrolled-text 
//list of all available model components.)
XSPEC12> help appendices
//show the manual appendices (which document the user interface,
//the Cash statistic, how to add models to XSPEC, a summary of 
//PLT commands, and associated FTOOLS and other programs for 
//manipulating data).
XSPEC12>help appendix local
//show the appendix describing how to add local models
```

Help also displays the following information as scrolling text:

```
XSPEC12> help ?
//Show a list of all available commands.
XSPEC12> help ??
//Show a brief summary and usage syntax of all available commands.
XSPEC12> <command> ?
// Show brief summary and syntax of <command>.
```
