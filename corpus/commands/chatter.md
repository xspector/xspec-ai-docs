---
name: chatter
aliases: [xchatter]
also_documents: []
source: XSchatter.tex
---

# chatter

**set verboseness level**

Control the verbosity of XSPEC.

**Syntax:** `chatter` <chatter level>  <log chatter>

where `<chatter level>` and `<log chatter>` are integer values.The initial value
for each argument is 10. Higher values will encourage XSPEC to tell the user
more, lower values tell the user less, or make XSPEC ``quieter'' 
`<chatter level>` applies to the terminal output, while  `<log chatter>`
controls the verbosity in the log file. Currently, the maximum chattiness   
is 25.Values below five should be avoided, as they tend to make XSPEC far 
too obscure.Some commands may temporarily modify the chattiness, such as 
the `error` command. A chattiness of 25 will generate a lot of debug output.

**Examples:**

```
XSPEC12> chatter 10
// Set the terminal chattiness to 10, same as the initial value.
XSPEC12> chatter ,0 
//Set the chattiness for the log file to very low. 
//This setting essentially disables the log file output.
XSPEC12> chatter 5
//Make XSPEC very quiet.
XSPEC12> chatter 10 25
// Restore the terminal chattiness to the initial level, 
// while in the log file XSPEC will tell all
// (particularly when new data files are read in)
```
