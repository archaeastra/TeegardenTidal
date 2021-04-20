#The Tidal Heating Substraction Plot shows the net tidal heating due to a Cassini State.
#Thanks to Dr. David Fleming, whose code I based this script 
#on for VPlanet compatibility.

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import re
import math

#InputDir = input("Input Directory:")
InputDir = "./Canari1K_AGES"
#Hard coded because I'm tired of typing this in

#Definitions
def Strip(pattern):      
    result = re.findall("\d+.\d+.+", pattern)
    result = float(result[0])
    return (result)
def Seek(log, pattern):
    for line in log:
        result = re.findall(pattern, line)
        if len(result) != 0:
            return(result)
def Find(log, pattern):
    for line in log:
        result = re.findall(pattern, line)
        #print(result)       
        if len(result) != 0:
            result = Strip(line)
            return (result)
def Degrees(list):
    for index in range(0,len(list)):
        list[index] = np.array(list[index], dtype=float)
        list[index] = math.degrees(list[index])
    return list

def Repair(list):
    for index in range(0,len(list)):
        #print(str(type(list[index])))
        if str(type(list[index])) == "<class 'NoneType'>":
            list[index] = int(0)
            print("Empty Index Zeroed")
            #print(list[index])
    return(list)


# Check correct number of arguments
if (len(sys.argv) != 2):
    print('ERROR: Incorrect number of arguments.')
    print('Usage: '+sys.argv[0]+' <pdf | png>')
    exit(1)
if (sys.argv[1] != 'pdf' and sys.argv[1] != 'png'):
    print('ERROR: Unknown file format: '+sys.argv[1])
    print('Options are: pdf, png')
    exit(1)

#CTRL = input("Has a CTRL file been created y/n?:")
CTRL = 'y'
if CTRL == 'y':
    ConDir = InputDir+"_CTRL"
elif CTRL == 'n':
    print("Please run THeSP_Control first.")
else:
    print("Invalid response")
    quit()
    
#Arrays for sorting the values. 
BInit=[]
CInit=[]
BFin=[]
CFin=[]
BInitC=[]
CInitC=[]
BFinC=[]
CFinC=[]
#Create an output file

#OTFL = input("Create output file? y/n:")
OTFL = "y"
csl = sys.stdout
if OTFL == 'y':
    out = open("THeSP.log", 'w+')
    sys.stdout = out
    print("Log File of Tidal Heats found")
else: 
    print("No Output File Created, proceeding to console...")
    
    
#Collection of b log files:
for root, dirs, files in os.walk(InputDir, topdown=False):
    for name in files:
        if name == "TGard.log":
            LogName = str(os.path.join(root, name))
            with open (LogName, 'rt') as log: 
                #Finding initial obs
                Seek(log,"----\sINITIAL\sSYSTEM\sPROPERTIES\s----")
                Seek(log, "-----\sBODY:\sTGb\s----") 
                obb = Find(log, "\(SurfEnFluxTotal\)")
                BInit.append(obb)
                Seek(log, "-----\sBODY:\sTGc\s----") 
                obc = Find(log, "\(SurfEnFluxTotal\)")
                CInit.append(obc)
                if OTFL == 'y':
                    print("----FILE:" + os.path.join(root, name))
                    print("--INITIAL--")
                    print("BODY-b:"+str(obb))
                    print ("BODY-c:"+str(obc))
            with open (LogName, 'rt') as log: 
                #Finding final obs
                Seek(log,"----\sFINAL\sSYSTEM\sPROPERTIES\s----") 
                Seek(log, "-----\sBODY:\sTGb\s----") 
                obb = Find(log, "\(SurfEnFluxTotal\)")
                BFin.append(obb)
                Seek(log, "-----\sBODY:\sTGc\s----") 
                obc = Find(log, "\(SurfEnFluxTotal\)")
                CFin.append(obc)
                if OTFL == 'y':
                    print("--FINAL--") 
                    print("BODY-b:"+str(obb))
                    print ("BODY-c:"+str(obc))
                    
print("Files Found")         
                       
#Collection of b control files:
for root, dirs, files in os.walk(ConDir, topdown=False):
    for name in files:
        if name == "TGard.log":
            LogName = str(os.path.join(root, name))
            with open (LogName, 'rt') as log: 
                #Finding initial obs
                Seek(log,"----\sINITIAL\sSYSTEM\sPROPERTIES\s----")
                Seek(log, "-----\sBODY:\sTGb\s----") 
                obb = Find(log, "\(SurfEnFluxTotal\)")
                BInitC.append(obb)
                Seek(log, "-----\sBODY:\sTGc\s----") 
                obc = Find(log, "\(SurfEnFluxTotal\)")
                CInitC.append(obc)
                if OTFL == 'y':
                    print("----FILE:" + os.path.join(root, name))
                    print("--INITIAL--")
                    print("BODY-b:"+str(obb))
                    print ("BODY-c:"+str(obc))
            with open (LogName, 'rt') as log: 
                #Finding final obs
                Seek(log,"----\sFINAL\sSYSTEM\sPROPERTIES\s----") 
                Seek(log, "-----\sBODY:\sTGb\s----") 
                obb = Find(log, "\(SurfEnFluxTotal\)")
                BFinC.append(obb)
                Seek(log, "-----\sBODY:\sTGc\s----") 
                obc = Find(log, "\(SurfEnFluxTotal\)")
                CFinC.append(obc)
                if OTFL == 'y':
                    print("--FINAL--") 
                    print("BODY-b:"+str(obb))
                    print ("BODY-c:"+str(obc))
print("Control Files Found")

sys.stdout = csl

                                     
#Math
for list in BInit, BInitC, BFin, BFinC, CInit, CInitC, CFin, CFinC:
    Repair(list)


BI=[]
CI=[]
BF=[]
CF=[]
print("B:", len(BInit), "BC:", len(BInitC))

for n in range(0, len(BInit)):
        print(n)   
        print(type(BFin[n]))
        BI.append(BInit[n]-BInitC[n])
        CI.append(CInit[n]-CInitC[n])
        BF.append(BFin[n]-BFinC[n])
        CF.append(CFin[n]-CFinC[n])  

                    
#Plotting:
fig, ax = plt.subplots(1,2, sharex=False);                                  
fig.set_size_inches(8,3);                                            
#fig.suptitle(str("Tidal Heating Substraction Plot (THeSP)"), fontsize=16);
fig.tight_layout(pad=2, w_pad=1.5);    


ax[0].hist(np.array(BF), bins=50, facecolor='DimGray');
ax[0].set_xlabel('Final Cassini Surface Flux of b (W/m$^{2}$)', fontsize=8);
ax[0].set_ylabel('Number', fontsize=12);
ax[0].set_xlim(0,2)
ax[0].set_yscale("log")
#ax[0].set_xscale("log")


ax[1].hist(np.array(CF), bins=17, facecolor='Gray');
ax[1].set_xlabel('Final Cassini Surface FLux of c (W/m$^{2}$)', fontsize=8);
#ax[1].set_xscale("log")
ax[1].set_yscale("log")

plt.show()

if (sys.argv[1] == 'pdf'):
    fig.savefig(str('THeSP.pdf'), bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig(str('THeSP.png'), bbox_inches="tight", dpi=600)