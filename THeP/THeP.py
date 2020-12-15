#The Tidal HEating Substraction Plot shows the net tidal heating due to a Cassini State.
#Thanks to Dr. David Fleming, whose code I based this script 
#on for VPlanet compatibility.

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
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

#Definitions
def Strip(pattern):      
    result = re.findall("\d+.\d+.+", pattern)
    result = float(result[0])
    return (result) 

InputDir = input("Input Directory:")

SInit=[]
BInit=[]
CInit=[]
SFin=[]
BFin=[]
CFin=[]
for root, dirs, files in os.walk(InputDir, topdown=False):
   for name in files:
        if name == "TGard.log":
            #print("File:" + os.path.join(root, name))
            LogName = str(os.path.join(root, name))
        #Isolation:
#>L We need to isolate the Obliquity from the log file so:
#Read in log file
            with open (LogName, 'rt') as log: 
                            SurfList= []    
                            for line in log:
                                if "(SurfEnFluxTotal)" in line:
                                    SurfList.append(line) 
                            #print(SurfList)
                            SurfDig = []
                            for index in SurfList:
                                num = Strip(index)
                                SurfDig.append(num)
                            #print(SurfDig)
                            SInit.append(SurfDig[0])
                            BInit.append(SurfDig[1])
                            CInit.append(SurfDig[2])
                            
                            if len(SurfList)>=4:
                                SFin.append(SurfDig[3])
                                BFin.append(SurfDig[4])
                                CFin.append(SurfDig[5])
                            else:
                                print("No Final State Reached")

print ("Files Found")

#Create an output file
OTFL = input("Create output file? y/n:")
if OTFL == 'y':
    csl = sys.stdout
    with open("THeP.log", 'w+') as out:
        sys.stdout = out
        print("Log File of THeP Energy Fluxes found")
        print("-----INITIAL-----")                      
        print ("--- BODY: TGb") 
        print(BInit)
        print ("--- BODY: TGc") 
        print(CInit)
        print("-----FINAL-----")  
        print ("---BODY: TGb:")
        print(BFin)
        print ("---BODY: TGc:")
        print(CFin)
        sys.stdout = csl
else: 
    print("No Output File Created, printing to console...")
    print("-----INITIAL-----")                      
    print ("--- BODY: TGb") 
    print(BInit)
    print ("--- BODY: TGc") 
    print(CInit)
    print("-----FINAL-----")  
    print ("---BODY: TGb:")
    print(BFin)
    print ("---BODY: TGc:")
    print(CFin)

                                
#Plotting:
fig, ax = plt.subplots(2,2, sharex=False);                                  
fig.set_size_inches(5,4);                                                 
fig.suptitle(str("Tidal Heating Plot (THeP)"), fontsize=16);
fig.tight_layout(pad=2, w_pad=1.5);    

ax[0,0].hist(np.array(BInit), bins=50, facecolor='Crimson');
ax[0,0].set_xlabel('Initial SurfEnFLux of TGb ($W/m^{2}$)', fontsize=10);
ax[0,0].set_ylabel('Number', fontsize=12);
#ax[0,0].set_xscale("log")
#ax[0,0].set_yscale("log")

ax[0,1].hist(np.array(CInit), bins=50, facecolor='OrangeRed');
ax[0,1].set_xlabel('Initial SurfEnFLux of TGc ($W/m^{2}$)', fontsize=10);
#ax[0,1].set_xscale("log")
#ax[0,1].set_yscale("log")

ax[1,0].hist(np.array(BFin), bins=50, facecolor='DarkOrange');
ax[1,0].set_xlabel('Final SurfEnFLux of TGb ($W/m^{2}$)', fontsize=10);
ax[1,0].set_ylabel('Number', fontsize=12);
#ax[1,0].set_xscale("log")
#ax[1,0].set_yscale("log")

ax[1,1].hist(np.array(CFin), bins=50, facecolor='SandyBrown');
ax[1,1].set_xlabel('Final SurfEnFLux of TGb ($W/m^{2}$)', fontsize=10);
#ax[1,1].set_xscale("log")
#ax[1,1].set_yscale("log")

if (sys.argv[1] == 'pdf'):
    fig.savefig(str('THeP.pdf'), bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig(str('THeP.png'), bbox_inches="tight", dpi=600)

