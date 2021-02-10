"""
Planet Orbit Evolution. Based on code by Dr. D. Fleming, by I.A.Guez.
Makes a plot of various planet stats
"""

from __future__ import division, print_function

import matplotlib as mpl
#mpl.use('Agg')
#Used when plotting without a screen.
import matplotlib.pyplot as plt
import numpy as np
import vplot as vpl
import sys

# Check correct number of arguments
if (len(sys.argv) != 2):
    print('ERROR: Incorrect number of arguments.')
    print('Usage: '+sys.argv[0]+' <pdf | png>')
    exit(1)
if (sys.argv[1] != 'pdf' and sys.argv[1] != 'png'):
    print('ERROR: Unknown file format: '+sys.argv[1])
    print('Options are: pdf, png')
    exit(1)

#Typical plot parameters that make for pretty plot
mpl.rcParams['figure.figsize'] = (10,8)
mpl.rcParams['font.size'] = 16.0

# Load data
#InputDirb = input("Input Directory b:")
#InputDirc = input("Input Directory c:")
#You can also hard code the addresses.
InputDirb = "./TGMCDrand_002b"
InputDirc = "./TGMCDrand_002c"
outputb = vpl.GetOutput(InputDirb)
outputc = vpl.GetOutput(InputDirc)
print("Directories Located")


# Extract data
time = outputb.TGb.Time/1.0e6 # Scale to Myr
eccb = outputb.TGb.Eccentricity
eccc = outputc.TGc.Eccentricity
obbb = outputb.TGb.Obliquity
obbc = outputc.TGc.Obliquity
rotb = outputb.TGb.RotPer
rotc = outputc.TGc.RotPer
tidhb = outputb.TGb.SurfEnFluxEqtide
tidhc = outputc.TGc.SurfEnFluxEqtide
print("Files Found") 

# Plot
fig, axes = plt.subplots(nrows=2, ncols=2, sharex=False)
#fig.set_size_inches(5,4);                                            
fig.tight_layout(pad=2, w_pad=1.5);   

axes[0,0].plot(time, obbb, color="DimGray", label="Teegarden b")
axes[0,0].plot(time, obbc, color="DarkGray", label="Teegarden c")
axes[0,0].set_xlim(time.min(),time.max())
axes[0,0].legend(loc="best")
axes[0,0].set_xlim(0,0.25)
axes[0,0].set_ylabel("Obliquity (deg)")


axes[0,1].plot(time, eccb, color="DimGray")
axes[0,1].plot(time, eccc, color="DarkGray")
axes[0,1].set_xlim(time.min(),time.max())
axes[0,1].set_xlim(0,0.25)
axes[0,1].set_ylabel("Eccentricity")


axes[1,0].plot(time, rotb, color="DimGray")
axes[1,0].plot(time, rotc, color="DarkGray")
axes[1,0].set_xlim(time.min(),time.max())
axes[1,0].set_xlim(0,0.25)
axes[1,0].set_xlabel("Time [Myr]")
axes[1,0].set_ylabel("Rotational Period (days)")


axes[1,1].plot(time, tidhb, color="DimGray")
axes[1,1].plot(time, tidhc, color="DarkGray")
axes[1,1].set_xlim(time.min(),time.max())
axes[1,1].set_xlim(0, 0.25)
axes[1,1].axhline(y=300, linestyle='--', c="Gray")
axes[1,1].axhline(y=0.08, linestyle='--', c="Gray")
axes[1,1].text(0.002, 0.09, s="Earth")
axes[1,1].text(0.07, 360, s="Runaway Greenhouse")
axes[1,1].set_yscale('log')
axes[1,1].set_xlabel("Time [Myr]")
axes[1,1].set_ylabel("Tidal Heating ($W/m^{2}$)")

if (sys.argv[1] == 'pdf'):
    fig.savefig('POE.pdf', bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig('POE.png', bbox_inches="tight", dpi=600)
