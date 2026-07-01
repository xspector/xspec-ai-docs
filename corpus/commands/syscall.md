---
name: syscall
aliases: []
also_documents: []
source: XSsyscall.tex
---

# syscall

**execute a shell command**

Execute command in a shell.

**Syntax:** `syscall` [<shell command>]

This command executes its arguments by passing them to the users current shell
for execution. Thus file name globbing (i.e. wildcard expansion) are performed 
on the command before execution. This is in contrast to the **exec** 
command, which executes commands directly, without first passing them on to a shell.

If no arguments are given, then the command will start an interactive subshell.
