---
name: diagrsp
aliases: [xdiagrsp]
also_documents: []
source: XSdiagrsp.tex
---

# diagrsp

**set a 'perfect' response for a spectrum**

Diagonalize the current response matrix for ideal response.

**Syntax:** `diagrsp` 

This command diagonalizes the current response matrix. The response matrix 
is set so that the channel values are mapped directly into the corresponding 
energy ranges, based on the channel energies and energy response range of the 
current response matrix.  

This command is very similar to running `dummyrsp` in mode 1, with two important 
differences.  Unlike `dummyrsp`, usage of this command requires that an 
actual response is currently loaded.  It takes its energy range and channel binning 
information from this currently loaded response rather than user input parameters.  
Secondly, this does not change the effeciency (ie. effective area) as a function 
of energy stored for the current detector. Invoking this command will simulate a 
detector with perfect spectral resolution. If you wish to simulate a detector with 
perfect resolution AND perfect efficiency, use the `dummyrsp` command.

The previous response matrices can be reimplemented with the `response` command, 
with no arguments. Any use of the `data` and `notice` commands will 
replace the dummy diagonal response with the correct set of matrices.
