from __future__ import division, print_function

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import vplot as vpl
import sys
import numpy as np

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
InputDir = "./Canari1K3/Canarirand_002"
InputDirO = "./Canari1K3_AGES/Canarirand_002"
output = vpl.GetOutput(InputDir)
outputO = vpl.GetOutput(InputDirO)
print("Directories Located")


# Extract data
time = output.TGb.Time/1.0e6 # Scale to Myr
time0 = outputO.TGb.Time/1.0e6 #scale
eccb = output.TGb.Eccentricity
eccc = output.TGc.Eccentricity
obbb = outputO.TGb.Obliquity
obbc = outputO.TGc.Obliquity
rotb = output.TGb.RotPer
rotc = output.TGc.RotPer
tidbc = output.TGb.SurfEnFluxEqtide
tidcc = output.TGc.SurfEnFluxEqtide
tidbca = outputO.TGb.SurfEnFluxEqtide
tidcca = outputO.TGc.SurfEnFluxEqtide
incb = output.TGb.Inc
incc= output.TGc.Inc
ab = output.TGb.LongA
ac = output.TGc.LongA
pb = output.TGb.ArgP
pc = output.TGc.ArgP

#Math
varpib = ab+pb
varpic = ac+pc
varpiDiff = np.fabs(np.fmod(varpib-varpic, 360.0))

mutinc=np.arccos(np.cos(incb)*np.cos(incc) + np.sin(incb)*np.sin(incc)*np.cos(ab-ac))


print("Files Found")

# Plot
fig, axes = plt.subplots(nrows=2, ncols=3, sharex=False)
fig.set_size_inches(16,10);                                            
fig.tight_layout(pad=2, w_pad=1.5); 
#b = LightGreen / DimGray
#c = Plum / DarkGray

axes[0, 0].plot(time, eccb, color="Black", label="Teegarden b")
axes[0, 0].plot(time, eccc, color="DarkGray", label="Teegarden c")
axes[0, 0].legend(loc="best")
axes[0, 0].set_xlim(0,1500)
axes[0, 0].set_xlabel("Time (Gyr)")
axes[0, 0].set_ylabel("Eccentricity")
axes[0, 0].set_xticks([0, 1000])
axes[0, 0].set_xticklabels(["0", "1"])

axes[0, 1].plot(time, rotb, color="Black")
axes[0, 1].plot(time, rotc, color="DarkGray")
axes[0, 1].set_xlim(0,1500)
axes[0, 1].set_xlabel("Time (Gyr)")
axes[0, 1].set_ylabel("Rotational Period (days)")
axes[0, 1].set_xlabel("Time (Gyr)")
axes[0, 1].set_xticks([0, 1000])
axes[0, 1].set_xticklabels(["0", "1"])

axes[0, 2].plot(time, tidbc, color="Black")
axes[0, 2].plot(time, tidcc, color="DarkGray")
axes[0, 2].set_xlim(0, 1500)
#axes[0, 2].set_ylim(0.0001, 1000000)
axes[0, 2].set_xlabel("Time (Gyr)")
axes[0, 2].set_ylabel("Tidal Heating (W/m$^{2}$)")
axes[0, 2].set_yscale('log')
axes[0, 2].set_xticks([0, 1000])
axes[0, 2].set_xticklabels(["0", "1"])

axes[1,0].plot(time, mutinc, color="Black")
axes[1,0].set_xlim(0,1500)
axes[1,0].set_xlabel("Time (Gyr)")
axes[1,0].set_ylabel("Mutual Inclination (deg)")
axes[1,0].set_xlabel("Time (Gyr)")
axes[1,0].set_yscale('log')
axes[1, 0].set_xticks([0, 1000])
axes[1, 0].set_xticklabels(["0", "1"])
axes[1,0].set_yticks([0.1, 1, 5])
axes[1,0].set_yticklabels(["0.1","1","5"])

#axes[1,1].scatter(time, varpib, color="Black", s=10, zorder=20)
#axes[1,1].scatter(time, varpic, color="DarkGrey", s=10, zorder=20)
axes[1,1].scatter(time, varpiDiff, color="Black", s=10, zorder=20)
#axes[1,1].set_ylim(0,360)
axes[1,1].set_xlim(0, 1500)
axes[1,1].set_yticks([0, 180, 360])
axes[1,1].set_yticklabels(["0", "180", "360"], fontsize=12)
axes[1,1].set_ylabel(r"$\Delta \varpi$ [$^{\circ}$]", fontsize=12)
axes[1,1].set_xticks([0, 1000])
axes[1,1].set_xticklabels(["0", "1"])
axes[1,1].set_xlabel("Time (Gyr)")
"""
axes[1,2].plot(time, incb, color="Black")
axes[1,2].plot(time, incc, color="DarkGrey")
axes[1,2].set_xlim(0,1500)
axes[1,2].set_xlabel("Time (Gyr)")
axes[1,2].set_ylabel("Mutual Inclination (deg)")
axes[1,2].set_xlabel("Time (Gyr)")
axes[1,2].set_yscale('log')
axes[1,2].set_xticks([0, 2000, 4000, 6000, 8000])
axes[1,2].set_xticklabels(["0", "2", "4", "6", "8"])
axes[1,2].set_yticks([0.01, 0.1, 1, 10])
axes[1,2].set_yticklabels(["0.01", "0.1","1","10"])
"""

if (sys.argv[1] == 'pdf'):
    fig.savefig('POE-C.pdf', bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig('POE-C.png', bbox_inches="tight", dpi=600)


fig2, axes = plt.subplots(nrows=1, ncols=2, sharex=False)
#fig.set_size_inches(5,4);                                            
fig2.tight_layout(pad=2, w_pad=1.5); 
#b = LightGreen / DimGray
#c = Plum / DarkGray

axes[0].plot(time0, obbb, color="Black", label="Teegarden b")
axes[0].plot(time0, obbc, color="DarkGray", label="Teegarden c")
axes[0].set_xlim(time0.min(),time0.max())
axes[0].legend(loc="best")
axes[0].set_xlim(0, 0.1)
axes[0].set_ylabel("Obliquity (deg)")
axes[0].set_xlabel("Time (kyr)")
axes[0].set_xticks([0, 0.1])
axes[0].set_xticklabels(["0", "100"])

axes[1].plot(time0, tidbca, color="Black")
axes[1].plot(time0, tidcca, color="DarkGray")
axes[1].set_xlim(0, 0.1)
#axes[1].set_ylim(100, 100000)
axes[1].set_xlabel("Time (kyr)")
axes[1].set_ylabel("Tidal Heating (W/m$^{2}$)")
axes[1].set_yscale('log')
axes[1].set_xticks([0, 0.1])
axes[1].set_xticklabels(["0", "100"])


if (sys.argv[1] == 'pdf'):
    fig2.savefig('POE-A.pdf', bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig2.savefig('POE-A.png', bbox_inches="tight", dpi=600)