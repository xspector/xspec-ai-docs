---
name: notice
aliases: [xnotice]
also_documents: []
source: XSnotice.tex
---

# notice

**notice data channels**

(See also `ignore`.)

 p{} p{---6}}
**Syntax:** & **notice** & `[<unit>] <range1> [<range2>] ... [<rangeN>]`

                 & **notice** & `all`

where `<rangeI>` ::= `<spectrum range>`:`<channel range>` |   `<channel range>`.

If no `<spectrum range>`  is given, then the previous range is used 
(the initial default range is file one (1) only). The form of `<spectrum range>` 
is

`<spectrum range>` ::= `<initial spectrum>`-`<last spectrum>`
|   `<spectrum>`

where `<init spectrum>`, `<last spectrum>`, and `<spectrum>` 
are spectrum numbers, in the order that they were input with the `data` 
command. The form of `<channel range>` is

`<channel range>` ::= `<initial channel>`-`<last channel>`
|   `<channel>`

If `<channel range>` are integers then channels will be used or if reals 
then energies (or wavelengths if `setplot wave` has been specified). 
Energy and wavelength units are determined by the `setplot energy` and 
`setplot wave` settings, unless the command begins with a `<unit>`, which works as
for `ignore`: for that command only, and integers are then in that unit
too.  If only the last channel is indicated, then a default 
value of 1 is used for the initial channel. Channels remain noticed until they 
are explicitly ignored with the `ignore` command. When a spectrum is 
replaced by another spectrum, all input channels automatically are noticed.

```
XSPEC> notice all 
```

resets all the channels to 'noticed'.

**Examples:**

Assume that 4 spectra have been read in, the first 2 having 100 channels and 
the last 2 having 50 channels. Assume also that channels 1-10 of all four 
spectra are ignored and that channels 80-100 of spectra 1 and 2 are ignored.

In XSPEC12, `notice` does not force the detector response to be reread 
(see `response` description).  

```
XSPEC> notice **:1-10 
//The first 10 channels of all 4 spectra are noticed.
XSPEC> notice 80-** 
//an attempt will be made to notice channels  in all 4 spectra 
// (as that was the last spectrum range specified) but the
// result is that only channels 80-100 will be noticed for  
// spectra 1 and 2, with no change for spectra 3 and 4 as 
// they have no channels greater than 50.
XSPEC> notice 1:1-5
//No additional channels are noticed, as these channels were
//already noticed by the earlier notice **:1-10 command.
XSPEC> notice keV 0.5-7.0
//Notice 0.5-7 keV in the last spectrum range, whatever setplot says
```
