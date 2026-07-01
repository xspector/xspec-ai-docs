---
name: editmod
aliases: [xeditmod]
also_documents: []
source: XSeditmod.tex
---

# editmod

**edit a model component**

Add, delete, or replace one component in the current model.

**Syntax:** `editmod` [<delimiter>] <component1> 
<delimiter> <component2> <delimiter> ... <componentN>
 [ <delimiter>]

where `<delimiter>` is some combination of (,+,*,and), and `<componentJ>`
is one of the models known to XSPEC.

The arguments for this command should specify a new model, with the same 
syntax as the previous model, except for one component which may be either added, 
deleted, or changed to a different component type. XSPEC then compares the entered 
model with the current model, determines which component is to be modified 
(prompting the user if necessary to resolve ambiguities) and then modifies the 
model, prompting the user for any new parameter values which may be needed.

**Examples:**

```
XSPEC12> mo wabs(po)
XSPEC12> ed wabs(po+ga)
//This command will add the component gauss to model
// in the specified place and prompt the user for its initial
// parameters.
XSPEC12> mo wabs(po+zg)
XSPEC12> ed po+zg
//This command will delete the component wabs from the 
//model, leaving the other components and their current 
//parameter values unchanged
XSPEC12> mo wabs(po+po)
XSPEC12> ed wabs(po)
//Here an ambiguity exists as to which component to delete.
//In this case XSPEC will print out  the current model, 
//showing the component number for each component, and then 
//prompt the user for which component he wants deleted.
XSPEC12> mo wabs(po+ga)
XSPEC12> ed wabs(po+zg)
//The component gauss will be replaced by the component zgauss, 
//and the user will be prompted for parameter values for the new
// component
```
