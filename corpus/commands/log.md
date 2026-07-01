---
name: log
aliases: [xlog]
also_documents: []
source: XSlog.tex
---

# log

**log the session output**

Open a log file.

**Syntax:** `log` [STAMP] <log file>

where `<log file>` is the name of the file to be opened (default
extension is .log). If the name of the file is preceded by $>$
then the log is appended to this file. If no arguments are on the
line, then the default file name is xspec.log.  If `<log
  file>` matches the string `none`, then the current log file is
closed.  If the string `STAMP` is given as an argument then the
log filename will include a data and time stamp. If `<log file>`
has no suffix then the stamp is appended to the name and a
.log suffix added. To change the chattiness level for the log
file (ie. the amount of information written to the log file) use the
`chatter` command. The default chatter level for the log file is
10.

**Examples:**

```
XSPEC12> log
//Turn on the log file (default xspec.log).
XSPEC12> log none 
//Close the log file.
XSPEC12> log >mylog
//Append to the log file (mylog.log)
XSPEC12> chatter ,, 12
//Set the log file chattiness to 12.
```
