"""
This script produces a reproduction of Figure 7 from Guez+2020, characterising Teegarden b and c, 
using VPLANET's STELLAR, EQTIDE, and DISTORB modules.

Ilyana A. Guez, University of Washington, 2020
"""

from __future__ import division, print_function

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import vplot as vpl
import sys
import re

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
output = vpl.GetOutput()

# Extract data
time = output.TGb.Time/1.0e6 # Scale to Myr
ecc1 = output.TGb.Eccentricity
ecc2 = output.TGc.Eccentricity
varpi1 = output.TGb.LongP
varpi2 = output.TGc.LongP
a1 = output.TGb.SemiMajorAxis
a2 = output.TGc.SemiMajorAxis

# Titling

eccb = "" 
tb = ""                           
tc = ""
incl = ""
ti= ""
obb= ""
obc= ""

with open ('TGb.in', 'rt') as inb: 	# Open file for reading text data.
	for line in inb:             	# For each line, stored as line,
		if "dEcc" in line:
			eccb=eccb+line
		if "dTidalQ" in line:            # add its contents to variable.
			tb=tb+line
		if "dObliquity" in line:
			obb=obb+line
			
with open ('TGc.in', 'rt') as inc: 	# Open file for reading text data.
	for line in inc:             	# For each line, stored as line,
		if "dInc" in line:
			incl=incl+line
		if "dTidalQ" in line:            # add its contents to variable.
			tc=tc+line
		if "dObliquity" in line:
			obc=obc+line

with open ('vpl.in', 'rt') as sysin:
	for line in sysin:
		if "dStopTime" in line:	
			ti=ti+line




eccsys=re.findall(r'\d+', eccb)
tideb=re.findall(r'\d+', tb)
tidec=re.findall(r'\d+', tc)
Inclin=re.findall(r'\d+', incl)
tyme=re.findall(r'\d+', ti)
oblib=re.findall(r'\d+', obb)
oblic=re.findall(r'\d+', obc)

eccsyss=str(eccsys[1])
tidebs=str(tideb[0])
tidecs=str(tidec[0])
Inclins=str(Inclin[0])
tymes=str(tyme[2])
oblibs=str(oblib[0])
oblics=str(oblic[0])


# Plot
fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True)
color = "k"


## Upper left: SMMA - TGb ##
axes[0,0].plot(time, a1, color="C3", zorder=-1, label="Teegarden-b")

# Format
axes[0,0].set_xlim(time.min(),time.max())
axes[0,0].legend(loc="best")
axes[0,0].set_ylim(0.0100,0.030)
axes[0,0].set_ylabel("Semi-major Axis [AU]")


## Upper right: Eccentricities b and c ##
axes[0,1].plot(time, ecc1, color="C3", zorder=-1)
axes[0,1].plot(time, ecc2, color="C0", zorder=-1)

# Format
axes[0,1].set_xlim(time.min(),time.max())
#axes[0,1].set_ylim(0.0,0.2)
axes[0,1].set_ylabel("Eccentricity")

## Lower left: SMMA - Teegarden c ##
axes[1,0].plot(time, a2, color="C0", zorder=-1, label="Teegarden-c")

# Format
axes[1,0].set_xlim(time.min(),time.max())
axes[1,0].legend(loc="best")
axes[1,0].set_ylim(0.0425,0.0440)
axes[1,0].set_xlabel("Time [Myr]")
axes[1,0].set_ylabel("Semi-major Axis [AU]")

## Lower right: diff between longitude of periapses ##
varpiDiff = np.fabs(np.fmod(varpi1-varpi2, 360.0))
axes[1,1].scatter(time, varpiDiff, color="C3", s=10, zorder=-1)

# Format
axes[1,1].set_xlim(time.min(),time.max())
axes[1,1].set_ylim(0, 360)
axes[1,1].set_xlabel("Time [Myr]")
axes[1,1].set_ylabel(r"$\Delta \varpi$ [$^{\circ}$]")



# Final formating
fig.tight_layout()
for ax in axes.flatten():
    # Rasterize
    ax.set_rasterization_zorder(0)

    # Set tick locations
    ax.set_xticklabels(["0", "50", "100", "150", "200", "250"])
    ax.set_xticks([0, 50, 100, 150, 200, 250])

# Show late-term ecc damping
inset1 = fig.add_axes([0.74, 0.735, 0.2, 0.2])
inset1.plot(time, ecc1, color="C3", zorder=20)
inset1.plot(time, ecc2, color="C0", zorder=20)

inset1.set_xlabel("Time [Myr]", fontsize=8)
inset1.set_ylabel("Eccentricity", fontsize=8)
inset1.set_xlim(10,1000)
inset1.set_xticks([10, 100, 1000])
inset1.set_xticklabels(["10", "100", "1000"], fontsize=8)
inset1.set_yticks([1.0e-4, 1.0e-3, 1.0e-2])
inset1.set_yticklabels(["$10^{-4}$", "$10^{-3}$", "$10^{-2}$"], fontsize=8)
inset1.set_yscale("log")

# Show early apsidal locking
inset2 = fig.add_axes([0.74, 0.235, 0.2, 0.2])
inset2.scatter(time, varpiDiff, color="C3", s=10, zorder=20)

#inset2.set_xlim(0.1,3)
#inset2.set_ylim(0,360)
inset2.set_xscale("log")
inset2.set_yticks([0, 180, 360])
inset2.set_yticklabels(["0", "180", "360"], fontsize=12)
inset2.set_ylabel(r"$\Delta \varpi$ [$^{\circ}$]", fontsize=12)
inset2.set_xticks([0.1, 0.25, 0.5, 1, 2, 3])
inset2.set_xticklabels(["0.1", "0.25", "0.5", "1", "2", "3"], fontsize=12)
inset2.set_xlabel("Time [Myr]", fontsize=12)

if (sys.argv[1] == 'pdf'):
    fig.savefig("Orbit_1E{4:s}I{0:s}E{1:s}Tb{2:s}c{3:s}Ob{5:s}c{6:s}.pdf".format(Inclins, eccsyss, tidebs, tidecs, tymes, oblibs, oblics), bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig("Orbit_1E{4:s}I{0:s}E{1:s}Tb{2:s}c{3:s}Ob{5:s}c{6:s}.png".format(Inclins, eccsyss, tidebs, tidecs, tymes, oblibs, oblics), bbox_inches="tight", dpi=600)
#fig.savefig("Rodriguez2011_Figs23.pdf", bbox_inches="tight", dpi=600)
