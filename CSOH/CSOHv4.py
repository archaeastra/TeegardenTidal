#Cassini State Obliquity Histogram, by Lyan I.A. Guez.
#A script to plot the distribution of obliquities in a Monte Carlo VSpace run.
#Thanks to Dr. David Fleming, whose code I based this script on for VPlanet compatibility.

import matplotlib as mpl
mpl.use('Agg')
#This is used when plotting without a screen
import matplotlib.pyplot as plt
import os
import vplot as vpl
import sys
import numpy as np

"""
# Check correct number of arguments
if (len(sys.argv) != 2):
    print('ERROR: Incorrect number of arguments.')
    print('Usage: '+sys.argv[0]+' <pdf | png>')
    exit(1)
if (sys.argv[1] != 'pdf' and sys.argv[1] != 'png'):
    print('ERROR: Unknown file format: '+sys.argv[1])
    print('Options are: pdf, png')
    exit(1)
"""
#InputDirb = input("Input Directory b:")
#InputDirc = input("Input Directory c:")
#You may also hard code the addresses
InputDir = "./Canari1K3"
InputDirFin = "./Canari1K3_AGES"

#Definitions

#Arrays for sorting the values. 
BInit=[]
CInit=[]
BFin=[]
CFin=[]

# Extract data
try:
    sims = sorted(next(os.walk(os.path.join(InputDir,'.')))[1])
except StopIteration:
    pass

for f in sims:
    #print(f)
    output = vpl.GetOutput(InputDir + "/" + str(f))

    BInit.append(output.TGb.Obliquity[0])
    CInit.append(output.TGc.Obliquity[0])

try:
    sims = sorted(next(os.walk(os.path.join(InputDirFin,'.')))[1])
except StopIteration:
    pass

for f in sims:
    #print(f)
    output = vpl.GetOutput(InputDirFin + "/" + str(f))

    BFin.append(output.TGb.Obliquity[-1] + 1)
    CFin.append(output.TGc.Obliquity[-1] + 1)



print ("Files Found")


#Plotting:
fig, ax = plt.subplots(2,2, sharex=False);                                  
fig.set_size_inches(8,6);                                                 
#fig.suptitle("Cassini State Obliquity Distribution", fontsize=12);
fig.tight_layout(pad=2, w_pad=1.5);      

ax[0,0].hist(BInit, bins=25, facecolor='Black');
ax[0,0].set_xlabel('Initial Obliquity of b', fontsize=12);
ax[0,0].set_ylabel('Number', fontsize=10);
ax[0,0].set_xticks([0, 60, 120, 180]);
ax[0,0].set_xticklabels(["0", "60", "120", "180"]);

ax[0,1].hist(CInit, bins=25, facecolor='DarkGray');
ax[0,1].set_xlabel('Initial Obliquity of c', fontsize=12);
ax[0,1].set_xticks([0, 60, 120, 180]);
ax[0,1].set_xticklabels(["0", "60", "120", "180"]);

ax[1,0].hist(BFin, bins = np.logspace(np.log10(1), np.log10(3), 100), facecolor='Black');
ax[1,0].set_xlabel('Final Obliquity of b (deg)', fontsize=12);
ax[1,0].set_ylabel('Number', fontsize=10);
#ax[1,0].set_xlim(0,1);
#ax[1,0].set_yscale('log');
ax[1,0].set_xscale('log');
ax[1,0].set_xticks([1, 1.5, 2, 3]);
ax[1,0].set_xticklabels(["0", "0.5", "1.0", "2.0"]);


ax[1,1].hist(CFin, bins=np.logspace(np.log10(1), np.log10(100), 70), facecolor='DarkGray');
ax[1,1].set_xlabel('Final Obliquity of c (deg)', fontsize=12);
#ax[1,1].set_xlim(0,60);
ax[1,1].set_xscale('log');
#ax[1,1].set_yscale('log');
ax[1,1].set_xticks([1, 11, 101]);
ax[1,1].set_xticklabels(["0", "10", "100"]);


#plt.show()

if (sys.argv[1] == 'pdf'):
    fig.savefig("CSOH.pdf", bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig("CSOH.png", bbox_inches="tight", dpi=600)
