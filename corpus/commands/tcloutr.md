---
name: tcloutr
aliases: []
also_documents: []
source: XStcloutr.tex
---

# tcloutr

**tclout with return value**

**Syntax:** `tcloutr` <option> [<par1>] [<par2>] [<par3>]

`tcloutr` is identical to the `tclout` command except that it also
provides what is stored in $xspec_tclout  as a return value.  Therefore it can 
be used in tcl scripts like this:

```
set var1 [tcloutr energies 1]
```

`tcloutr` may produce quite a lot of unwanted screen output, which can 
be avoided by using `tclout`.
