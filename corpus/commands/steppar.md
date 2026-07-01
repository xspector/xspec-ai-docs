---
name: steppar
aliases: [xsteppar]
also_documents: []
source: XSsteppar.tex
---

# steppar

**generate the statistic ``surface'' for 1 or more parameters**

Perform a fit while stepping the value of a parameter through a given range. 
Useful for determining confidence ranges in situations where greater control 
is needed than given with the `error` command.

**Syntax:** `steppar` [current| best] <step spec> [<step spec>...]

where `<step spec>` ::= `[log| nolog] [<modelName>:]<param index> 
<low value>  <high value>  <# steps>`

or `<step spec>` ::= `[log| nolog] [<modelName>:]<param index> 
delta <step size>  <# steps>`

In the first case the parameter is stepped from `<low value>` to `<high value>` 
in  `<# steps>` plus one trials. In the second case the parameter is stepped 
from `<best fit value>`-`<step size>`*`<# steps>` to `<best fit value>>`
+`<step size>`*`<# steps>`, ie a total of 2`<# steps>`+1 trials. 
The stepping is either linear or 
log. Initially, the stepping is linear but it can be changed by the optional 
string `log` before the parameter index. `nolog` will force the stepping to be 
returned to the linear form.  If more than one parameter is entered, then 
`<# steps>` must be entered for each one except the last.  Note that every 
variable parameter whose `<param index>` is NOT entered in the command will 
still be allowed to vary freely during each steppar iteration. 

To perform a `steppar` run on `gain` (or response) parameters, 
the optional `[<modelName>:]` specifier is replaced by an optional 
`[<sourceNumber>:]` specifier, and the letter 'r' needs to be 
attached as a prefix to the `<parameter index>`.  For example:

```
steppar 2:r3 1.5 2. 10
```

will step the third response parameter belonging to source number 2.

The number of steps is set initially to 10. At each value, the parameter is 
frozen, a fit performed, and the resulting value of chi-squared given. 
If `best` is given as an argument then the non-stepped parameters are 
reset to the best-fit values at each grid point.  Alternatively, if 
`current` is given as an argument then the non-stepped parameters 
are started at their values after the last grid point (the default).

If multiple `<step spec>` are given for different parameters, then a 
raster scan of the parameter ranges is performed.  At the end of the set, 
the parameters and chi-squared are restored to the values they had initially.

If the model is in a best-fit state when a `steppar` run is started 
and a new best fit is found during the run, the user will be prompted at the 
end of the run to determine if they wish to accept the new best-fit values 
for their parameters.  This prompting can be disabled by the setting of 
the `query` flag.

Depending on the machine, a `steppar` run may be sped up significantly 
by assigning it to multiple processes.  See the `parallel` command with 
the `steppar` option for more details.

**Examples:**
  
Assume that the current model has four parameters:

```
XSPEC12> steppar 3 1.5 2.5
//Step parameter 3 from 1.5 to 2.5 in steps of .1.
XSPEC12> steppar log
//Repeat the above, only use multiplicative steps of 1.0524.
XSPEC12> step nolog 2 -.2 .2 20
//Step parameter 2 linearly from -.2 to .2 in steps of 0.02.
XSPEC12> step 2 delta 0.02 5
      //Step parameter 2 linearly from the best-fit value-0.1 to 
      //the best-fit value+0.1 in a total of 11 steps.
```
