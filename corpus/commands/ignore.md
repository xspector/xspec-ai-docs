---
name: ignore
aliases: [xignore]
also_documents: []
source: XSignore.tex
---

# ignore

**ignore detector channels**

Ignore data channels. (See also `notice`.)

 p{} p{---6}}
**Syntax:** & **ignore** & `<range1> [<range2>] ... [<rangeN>]`

                 & **ignore** & `bad`

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

If integers are given for the channel ranges then channels will be used while 
if reals are given then energies (or wavelengths if `setplot wave` has 
been specified). Energy and wavelength units are determined by the `setplot energy` 
and `setplot wave` settings.  If only the last channel is indicated, then a 
default value of one (1) is used for the initial channel. Channels remain 
ignored until they are explicitly noticed with the `notice` command, 
or if a spectrum is replaced.  

**Examples:**
  
Assume that 4 spectra have been read in, the first 2 with 100 channels 
and the last 2 with 50 channels.

```
XSPEC12> ignore **:1-10
//The first 10 channels of all 4 spectra are ignored
XSPEC12> ignore 80-**
//An attempt will be made to ignore channels  in all four data 
// sets (as that was the last spectrum range specified). As a result,
// only channels 80-100 will be ignored for spectra 1 and 2.
// No change will occur for spectra 3 and 4, as they have no 
// channels greater than 50.
XSPEC12> ign 4:1-20 3:30-40 45-** 
//Channels 11-20 for spectrum 4 are ignored (1-10 were ignored already)
// while channels 30-40 and 45-50 of spectrum 3 are ignored.
XSPEC12> ignore 1:1-5
//No channels are ignored, as these were ignored at the beginning.
XSPEC12> ignore 2:1.-5.
//Ignore all channels between 1 and 5 keV in the second dataset
```
