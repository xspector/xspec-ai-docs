---
name: delcomp
aliases: [xdelcomp]
also_documents: []
source: XSdelcomp.tex
---

# delcomp

**delete a model component**

Delete one or more components from the current model. 

**Syntax:** `delcomp` [<modelName>:]<comp num range>

where `<comp num range>` is a range of positions in the 
model specification of the components to be deleted.

**Examples:**
  
Suppose that the current model specification is

```
wa(po+ga+ga)
```

Then

```
XSPEC> delcomp 3-4
//Changes the model to wa(po)
XSPEC> delcomp 1
//Changes the model to po
```
