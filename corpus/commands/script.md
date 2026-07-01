---
name: script
aliases: [xscript]
also_documents: []
source: XSscript.tex
---

# script

**write commands to a script file**

Open a script file.

**Syntax:** `script` <script file>

where `<script file>` is the name of the file to be opened 
(default extension is .xcm).  If no arguments are on the line, 
then the default file name is xspec.xcm.  If `<script file>` 
matches the string `none`, then the current script file is closed. 
The script file saves all commands that are input. This command is useful 
for users who use the same set of commands repeatedly. Once a script file is 
written and saved, the user then can re-run the same set of commands on other data by:

```
XSPEC12> source <script file>
```

**Examples:**

```
XSPEC12> script
// Turn on the script file (default xspec.xcm)
XSPEC12> script none
// Close the script file.
XSPEC12> script myscript 
// Open the script file (myscript.xcm)
```
