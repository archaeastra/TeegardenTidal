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

#Definitions
def Strip(pattern):      
    result = re.findall("\d+.\d+.+", pattern)
    result = float(result[0])
    return (result) 

# Check correct number of arguments
if (len(sys.argv) != 2):
    print('ERROR: Incorrect number of arguments.')
    print('Usage: '+sys.argv[0]+' <pdf | png>')
    exit(1)
if (sys.argv[1] != 'pdf' and sys.argv[1] != 'png'):
    print('ERROR: Unknown file format: '+sys.argv[1])
    print('Options are: pdf, png')
    exit(1)


InputDir = input("Input Directory:")
#InputDir = "./TGMC/TGMC5/Old/TGMCDistbncy"
CTRL = input("Has a CTRL file been created y/n?:")
if CTRL == 'y':
    ConDir = ConDir = InputDir+"_CTRL"
elif CTRL == 'n':
    print("Please run THeSP_Control first.")
else:
    print("Invalid response")
    quit()
    
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
print("Files Found")                                
SInitC=[]
BInitC=[]
CInitC=[]
SFinC=[]
BFinC=[]
CFinC=[]
for root, dirs, files in os.walk(ConDir, topdown=False):
   for name in files:
        if name == "TGard.log":
            #print("File:" + os.path.join(root, name))
            LogName = str(os.path.join(root, name))
        #Isolation:
#>L We need to isolate the Obliquity from the log file so:
#Read in log file
            with open (LogName, 'rt') as log: 
                            SurfListC= []    
                            for line in log:
                                if "(SurfEnFluxTotal)" in line:
                                    SurfListC.append(line) 
                            #print(SurfListC)
                            SurfDigC = []
                            for index in SurfListC:
                                num = Strip(index)
                                SurfDigC.append(num)
                            #print(SurfDigC)
                            SInitC.append(SurfDigC[0])
                            BInitC.append(SurfDigC[1])
                            CInitC.append(SurfDigC[2])
                            
                            if len(SurfListC)>=4:
                                SFinC.append(SurfDigC[3])
                                BFinC.append(SurfDigC[4])
                                CFinC.append(SurfDigC[5])
print("Control Files Found")    



                                       
#Math
for list in BInit, BInitC, BFin, BFinC, CInit, CInitC, CFin, CFinC:
    #print(list)
    for n in range(len(list)):
        list[n]=float(list[n])
BI=[]
CI=[]
BF=[]
CF=[]
for n in range(0, len(BInit)):
        #print(n)   
        BI.append(BInit[n]-BInitC[n])
        CI.append(CInit[n]-CInitC[n])
        BF.append(BFin[n]-BFinC[n])
        CF.append(CFin[n]-CFinC[n])  

#Create an output file
OTFL = input("Create output file? y/n:")
if OTFL == 'y':
    csl = sys.stdout
    with open("THeSPbycn.log", 'w+') as out:
        sys.stdout = out
        print("Log File of THeSP Energy Fluxes found")
        print("-----INITIAL-----")                      
        print ("--- BODY: TGb") 
        print(BI)
        print ("--- BODY: TGc") 
        print(CI)
        print("-----FINAL-----")  
        print ("---BODY: TGb:")
        print(BF)
        print ("---BODY: TGc:")
        print(CF)
        sys.stdout = csl
else: 
    print("No Output File Created, printing to console...")
    print("-----INITIAL-----")                      
    print ("--- BODY: TGb") 
    print(BI)
    print ("--- BODY: TGc") 
    print(CI)
    print("-----FINAL-----")  
    print ("---BODY: TGb:")
    print(BF)
    print ("---BODY: TGc:")
    print(CF)
                    
#Plotting:
fig, ax = plt.subplots(2,2, sharex=False);                                  
fig.set_size_inches(5,4);                                            
fig.suptitle(str("Tidal Heating Substraction Plot (THeSP)"), fontsize=16);
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

ax[1,0].hist(np.array(BF), bins=50, facecolor='DarkOrange');
ax[1,0].set_xlabel('Final Cassini SurfEnFLux of TGb ($W/m^{2}$)', fontsize=10);
ax[1,0].set_ylabel('Number', fontsize=12);
#ax[1,0].set_xscale("log")
#ax[1,0].set_yscale("log")

ax[1,1].hist(np.array(CF), bins=50, facecolor='SandyBrown');
ax[1,1].set_xlabel('Final Cassini SurfEnFLux of TGc ($W/m^{2}$)', fontsize=10);
#ax[1,1].set_xscale("log")
#ax[1,1].set_yscale("log")

if (sys.argv[1] == 'pdf'):
    fig.savefig(str('THeSPbycn.pdf'), bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig(str('THeSPbycn.png'), bbox_inches="tight", dpi=600)


