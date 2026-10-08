---
name: abund
aliases: [xabund]
also_documents: []
source: XSabund.tex
---

# abund

**set the solar abundances**

Set the abundance table for elements up to Zinc (Z=30) used in the plasma emission and photoelectric absorption models, in linear ratios to Hydrogen. The tables used are derived from various papers, most of which quote the log base ten abundance with Hydrogren set at 12. The table from Lodders et al 2009 for the proto-solar values gives the values normalized to N(Si), which are normalized to Hydrogen before calculating the linear ratio. The default abundance table in Xspec is Anders E. & Grevesse N., 1989 (angr).

**Syntax:** `abund` <option>

where `<option>` is:

}

`angr` & [Anders E. & Grevesse N. (1989, Geochimica et Cosmochimica Acta 53, 197)](https://ui.adsabs.harvard.edu/abs/1989GeCoA..53..197A/abstract) (Photospheric, using Table 2)

`aspl` & [Asplund M., Grevesse N., Sauval A.J. & Scott P. (2009, ARAA, 47, 481)](https://ui.adsabs.harvard.edu/abs/2009ARA&A..47..481A/abstract) (Photospheric, using Table 1)

`feld` & [Feldman U.(1992, Physica Scripta 46, 202)](https://ui.adsabs.harvard.edu/abs/1992PhyS...46..202F/abstract)

`aneb` & [Anders E. & Ebihara (1982, Geochimica et Cosmochimica Acta 46, 2363)](https://ui.adsabs.harvard.edu/abs/1982GeCoA..46.2363A/abstract)

`grsa` & [Grevesse, N. & Sauval, A.J. (1998, Space Science Reviews 85, 161)](https://ui.adsabs.harvard.edu/abs/1998SSRv...85..161G/abstract)

`wilm` & [Wilms J., Allen A. & McCray R. (2000, ApJ 542, 914)](https://ui.adsabs.harvard.edu/abs/2000ApJ...542..914W /abstract)

`lodd` & [Lodders K (2003, ApJ 591, 1220)](https://ui.adsabs.harvard.edu/abs/2003ApJ...591.1220L/abstract) (Photospheric, using Table 1)

`lpgp` & [Lodders K., Palme H., Gail H.P. (2009, Landolt-Börnstein, New Series, vol VI/4B, pp 560–630)](https://ui.adsabs.harvard.edu/abs/2009LanB...4B..712L/abstract) (Photospheric, using Table 4)

`lpgs` & [Lodders K., Palme H., Gail H.P. (2009, Landolt-Börnstein, New Series, vol VI/4B, pp 560–630)](https://ui.adsabs.harvard.edu/abs/2009LanB...4B..712L/abstract) (Proto-solar, using Table 10)

`felc` & [Feldman U., Mandelbaum P., Seely J.L., Doschek G.A. & Gursky H. (1992, ApJSS 81, 387)](https://ui.adsabs.harvard.edu/abs/1992ApJS...81..387F/abstract) (Coronal)

`file <filename>` & where `<filename>` is the path to and name of an ASCII file containing 30 lines, for the first 30 elements, with one number value per line. Set all abundance numbers relative to H. 

If no `<option>` is given, the `abund` command reports which abundance table is currently in use.

The tables are:

{{1.5}

Z  & El & angr     & aspl     & feld     & aneb     & grsa     & wilm    

1  & H  & 1.00E+00 & 1.00E+00 & 1.00E+00 & 1.00E+00 & 1.00E+00 & 1.00E+00

2  & He & 9.77E-02 & 8.51E-02 & 9.77E-02 & 8.01E-02 & 8.51E-02 & 9.77E-02

3  & Li & 1.45E-11 & 1.12E-11 & 1.26E-11 & 2.19E-09 & 1.26E-11 & 0.00E+00

4  & Be & 1.41E-11 & 2.40E-11 & 2.51E-11 & 2.87E-11 & 2.51E-11 & 0.00E+00

5  & B  & 3.98E-10 & 5.01E-10 & 3.55E-10 & 8.82E-10 & 3.55E-10 & 0.00E+00

6  & C  & 3.63E-04 & 2.69E-04 & 3.98E-04 & 4.45E-04 & 3.31E-04 & 2.40E-04

7  & N  & 1.12E-04 & 6.76E-05 & 1.00E-04 & 9.12E-05 & 8.32E-05 & 7.59E-05

8  & O  & 8.51E-04 & 4.90E-04 & 8.51E-04 & 7.39E-04 & 6.76E-04 & 4.90E-04

9  & F  & 3.63E-08 & 3.63E-08 & 3.63E-08 & 3.10E-08 & 3.63E-08 & 0.00E+00

10 & Ne & 1.23E-04 & 8.51E-05 & 1.29E-04 & 1.38E-04 & 1.20E-04 & 8.71E-05

11 & Na & 2.14E-06 & 1.74E-06 & 2.14E-06 & 2.10E-06 & 2.14E-06 & 1.45E-06

12 & Mg & 3.80E-05 & 3.98E-05 & 3.80E-05 & 3.95E-05 & 3.80E-05 & 2.51E-05

13 & Al & 2.95E-06 & 2.82E-06 & 2.95E-06 & 3.12E-06 & 2.95E-06 & 2.14E-06

14 & Si & 3.55E-05 & 3.24E-05 & 3.55E-05 & 3.68E-05 & 3.55E-05 & 1.86E-05

15 & P  & 2.82E-07 & 2.57E-07 & 2.82E-07 & 3.82E-07 & 2.82E-07 & 2.63E-07

16 & S  & 1.62E-05 & 1.32E-05 & 1.62E-05 & 1.89E-05 & 2.14E-05 & 1.23E-05

17 & Cl & 3.16E-07 & 3.16E-07 & 3.16E-07 & 1.93E-07 & 3.16E-07 & 1.32E-07

18 & Ar & 3.63E-06 & 2.51E-06 & 4.47E-06 & 3.82E-06 & 2.51E-06 & 2.57E-06

19 & K  & 1.32E-07 & 1.07E-07 & 1.32E-07 & 1.39E-07 & 1.32E-07 & 0.00E+00

20 & Ca & 2.29E-06 & 2.19E-06 & 2.29E-06 & 2.25E-06 & 2.29E-06 & 1.58E-06

21 & Sc & 1.26E-09 & 1.41E-09 & 1.48E-09 & 1.24E-09 & 1.48E-09 & 0.00E+00

22 & Ti & 9.77E-08 & 8.91E-08 & 1.05E-07 & 8.82E-08 & 1.05E-07 & 6.46E-08

23 & V  & 1.00E-08 & 8.51E-09 & 1.00E-08 & 1.08E-08 & 1.00E-08 & 0.00E+00

24 & Cr & 4.68E-07 & 4.37E-07 & 4.68E-07 & 4.93E-07 & 4.68E-07 & 3.24E-07

25 & Mn & 2.45E-07 & 2.69E-07 & 2.45E-07 & 3.50E-07 & 2.45E-07 & 2.19E-07

26 & Fe & 4.68E-05 & 3.16E-05 & 3.24E-05 & 3.31E-05 & 3.16E-05 & 2.69E-05

27 & Co & 8.32E-08 & 9.77E-08 & 8.32E-08 & 8.27E-08 & 8.32E-08 & 8.32E-08

28 & Ni & 1.78E-06 & 1.66E-06 & 1.78E-06 & 1.81E-06 & 1.78E-06 & 1.12E-06

29 & Cu & 1.62E-08 & 1.55E-08 & 1.62E-08 & 1.89E-08 & 1.62E-08 & 0.00E+00

30 & Zn & 3.98E-08 & 3.63E-08 & 3.98E-08 & 4.63E-08 & 3.98E-08 & 0.00E+00

}

{{1.5}

Z  & El & lodd     & lgpp     & lgps     & felc    

1  & H  & 1.00E+00 & 1.00E+00 & 1.00E+00 & 1.00E+00

2  & He & 7.92E-02 & 8.41E-02 & 9.69E-02 & 7.94E-02

3  & Li & 1.90E-09 & 1.26E-11 & 2.15E-09 & 0.00E+00

4  & Be & 2.57E-11 & 2.40E-11 & 2.36E-11 & 0.00E+00

5  & B  & 6.03E-10 & 5.01E-10 & 7.26E-10 & 0.00E+00

6  & C  & 2.45E-04 & 2.45E-04 & 2.78E-04 & 3.89E-04

7  & N  & 6.76E-05 & 7.24E-05 & 8.19E-05 & 1.00E-04

8  & O  & 4.90E-04 & 5.37E-04 & 6.06E-04 & 7.76E-04

9  & F  & 2.88E-08 & 3.63E-08 & 3.10E-08 & 0.00E+00

10 & Ne & 7.41E-05 & 1.12E-04 & 1.27E-04 & 1.20E-04

11 & Na & 1.99E-06 & 2.00E-06 & 2.23E-06 & 8.51E-06

12 & Mg & 3.55E-05 & 3.47E-05 & 3.98E-05 & 1.41E-04

13 & Al & 2.88E-06 & 2.95E-06 & 3.27E-06 & 1.10E-05

14 & Si & 3.47E-05 & 3.31E-05 & 3.86E-05 & 1.26E-04

15 & P  & 2.88E-07 & 2.88E-07 & 3.20E-07 & 0.00E+00

16 & S  & 1.55E-05 & 1.38E-05 & 1.63E-05 & 1.86E-05

17 & Cl & 1.82E-07 & 3.16E-07 & 2.00E-07 & 0.00E+00

18 & Ar & 3.55E-06 & 3.16E-06 & 3.58E-06 & 3.80E-06

19 & K  & 1.29E-07 & 1.32E-07 & 1.45E-07 & 0.00E+00

20 & Ca & 2.19E-06 & 2.14E-06 & 2.33E-06 & 8.51E-06

21 & Sc & 1.17E-09 & 1.26E-09 & 1.33E-09 & 0.00E+00

22 & Ti & 8.32E-08 & 7.94E-08 & 9.54E-08 & 0.00E+00

23 & V  & 1.00E-08 & 1.00E-08 & 1.11E-08 & 0.00E+00

24 & Cr & 4.47E-07 & 4.37E-07 & 5.06E-07 & 0.00E+00

25 & Mn & 3.16E-07 & 2.34E-07 & 3.56E-07 & 0.00E+00

26 & Fe & 2.95E-05 & 2.82E-05 & 3.27E-05 & 1.26E-04

27 & Co & 8.13E-08 & 8.32E-08 & 9.07E-08 & 0.00E+00

28 & Ni & 1.66E-06 & 1.70E-06 & 1.89E-06 & 6.92E-06

29 & Cu & 1.82E-08 & 1.62E-08 & 2.09E-08 & 0.00E+00

30 & Zn & 4.27E-08 & 4.17E-08 & 5.02E-08 & 0.00E+00

}

**Examples:**

XSPEC>abund
angr:  Anders E. & Grevesse N. Geochimica et Cosmochimica Acta 53, 197 (1989)
XSPEC>abund ?
Change/Report the solar abundance table in use
    Syntax: abund [ feld | angr | aneb | grsa | wilm | lodd | aspl | lpgp | lpgs ]
            abund file </path/to/filename>
            (define & load new vector from data in <filename>)
XSPEC>abund lodd
 Solar Abundance Vector set to lodd:  Lodders, K. ApJ 591, 1220 (2003)
XSPEC>abund
lodd:  Lodders, K. ApJ 591, 1220 (2003)
