---
name: cpd
aliases: [xcpd]
also_documents: [cpdnone]
source: XScpd.tex
---

# cpd

**set current plotting device**

 p{} p{---6}}
**Syntax:** & **cpd** & `<plot device>`

& **cpd** & `<filename>`

& **cpd** & `<filename>/{ps,cps,vps,vcps}`

& **cpd** & `none`

Set current plot device. The same can be achieved with the `setplot device` 
command, which takes the same options. In XSPEC12 as in previous versions, 
the plot device options are those allowed by the PGPLOT library.

When plotting to the screen, the most commonly used devices are `/xs` 
(`/xserve`) and `/xw` (`/xwindow`).  If you select 
`/xs`, the plot window is persistent: it remains visible and in 
the selected position even after the XSPEC session is finished.  With 
`/xw` the plot window closes at the end of the XSPEC session.  
Also note that on some platforms, when using `/xs` in multiple 
desktops, you might not see the window appear in a second desktop if 
it is still open in the first.

If the second argument does not start with a '/' character, which indicates 
that the string represents a PGPLOT device, it is taken to be a filename 
for Postscript output, and the default postscript driver will be used. 
The default postscript driver produces a monochrome plot in landscape 
orientation.

The filename argument can be followed by a '/' that specifies a particular 
postscript driver variant. Allowable  variants are: `cps` (color 
postscript), `vps` (monochrome portrait orientation), and `vcps` 
(color portrait orientation), as well as the default, `ps`.

**PGPLOT devices**

A number of plot device types are supported in XSPEC. PGPLOT devices 
available on Unix machines are:

/GIF & Graphics Interchange Format file, landscape orientation

/VGIF & Graphics Interchange Format file, portrait orientation

/NULL & Null device, no output

/PPM & Portable Pixel Map file, landscape orientation

/VPPM & Portable Pixel Map file, portrait orientation

/PS & PostScript file, landscape orientation

/VPS & PostScript file, portrait orientation

/CPS & Colour PostScript file, landscape orientation

/VCPS & Colour PostScript file, portrait orientation

/TEK4010 & Tektronix 4010 terminal

/GF & GraphOn Tek terminal emulator

/RETRO & Retrographics VT640 Tek emulator

/GTERM & Color gterm terminal emulator

/XTERM & XTERM Tek terminal emulator

/ZSTEM & ZSTEM Tek terminal emulator

/V603 & Visual 603 terminal

/KRM3 & Kermit 3 IBM-PC terminal emulator

/TK4100 & Tektronix 4100 terminals

/VT125DEC & VT125 and other REGIS terminals

/XDISP & pgdisp or figdisp server

/XWINDOW & X window window@node:display.screen/xw

/XSERVE & An /XWINDOW window that persists for re-use 

`cpd none` closes the device.  For Postscript output, it 
flushes the write buffer into the file and closes the file.
Note that in XSPEC12, each plot command produces a separate page in 
the postscript file, unlike previously where each plot overwrote the 
previous plot.

**Examples:**

Produce a set of color postscript plots in landscape orientation  

```
// ... commands to produce a plot.
XSPEC> cpd   dataplot.ps/cps
XSPEC> plot data chi
XSPEC> plot ufspec
XSPEC> plot efficiency
XSPEC> cpd none
```

Will produce 3 plots in the file dataplot.ps

Note, in contrast, that the `hardcopy` command will print only the plot that 
is currently in a graphics frame.
