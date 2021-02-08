#ScatterPlot
#Plots a scatter plot of obliquity versus eccentricity with tidal heat varying dot size.
#Thanks to Dr. David Fleming, whose code I based this script on for VPlanet compatibility.

import matplotlib as mpl
#mpl.use('Agg')
#Used whe plotting without a screen.
import matplotlib.pyplot as plt
import numpy as np
import math
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

InputDirb = input("Input Directory b:")
InputDirc = input("Input Directory c:")
#Can also hard code the addresses.
#InputDirb = "D:/TGMCDistbycn"
#InputDirc = "D:/TGMCDistbncy"

#Definitions
def Strip(pattern):      
    result = re.findall("\d+.\d+.+", pattern)
    #print(result)
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
            #print(result)       
            return (result)
def Degrees(list):
    for index in range(0,len(list)):
        list[index] = np.array(list[index], dtype=float)
        list[index] = math.degrees(list[index])
    return list
def Log(list):
    for index in range(0,len(list)):
        list[index] = np.array(list[index], dtype=float)
        list[index] = np.log(list[index])
        #This is size tweaking for the plot, not necessary math
        list[index] = list[index]*5
    return list

#Arrays for sorting the values. 
EB=[]
OB=[]
TB=[]
EC=[]
OC=[]
TC=[]

#Create an output file

#OTFL = input("Create output file? y/n:")
OTFL = "n"
csl = sys.stdout
if OTFL == 'y':
    out = open("Scatter.log", 'w+')
    sys.stdout = out
    print("Log File of Values found")
else: 
    print("No Output File Created, proceeding to console...")
#The output prints the values Scatter finds to a text file: THeP.log, so they can be checked and/or used.

#Collection of b log files:
print('B')
for root, dirs, files in os.walk(InputDirb, topdown=False):
    for name in files:
        if name == "TGard.log":
            LogName = str(os.path.join(root, name))
            #Only need FINAL values
            with open (LogName, 'rt') as log: 
                Seek(log,"----\sFINAL\sSYSTEM\sPROPERTIES\s----") 
                Seek(log, "-----\sBODY:\sTGb\s----") 
                obb= Find(log, "\(Obliquity\)")
                thb = Find(log, "\(SurfEnFluxTotal\)")
                ecb= Find(log, "\(Eccentricity\)")
                EB.append(ecb)
                OB.append(obb)
                TB.append(thb)
                if OTFL == 'y':
                    print("----FILE:" + os.path.join(root, name)) 
                    print("BODY-b: Ob, Ecc, TidalHeat")
                    print(str(obb)+', '+str(ecb)+', '+str(thb))                  
#Collection of c log files:
print('C')
for root, dirs, files in os.walk(InputDirc, topdown=False):
    for name in files:
        if name == "TGard.log":
            LogName = str(os.path.join(root, name))
            #Only need FINAL values
            with open (LogName, 'rt') as log: 
                Seek(log,"----\sFINAL\sSYSTEM\sPROPERTIES\s----") 
                Seek(log, "-----\sBODY:\sTGc\s----")
                obc= Find(log, "\(Obliquity\)")
                thc= Find(log, "\(SurfEnFluxTotal\)")
                ecc= Find(log, "\(Eccentricity\)")
                EC.append(ecc)
                OC.append(obc)
                TC.append(thc)
                if OTFL == 'y':
                    print("----FILE:" + os.path.join(root, name)) 
                    print("BODY-c: Ob, Ecc, TidalHeat")
                    print(str(obc)+', '+str(ecc)+', '+str(thc))
sys.stdout = csl

print ("Files Found")

print('B')
print(EB,OB,TB)  
print('C')
print(EC,OC,TC)

#Math
for list in OB, OC:
    Degrees(list)

#Plotting:
fig, ax = plt.subplots(1,2);                                  
fig.set_size_inches(8,6);                                                 
#fig.suptitle("Review Plot", fontsize=12);
fig.tight_layout(pad=2, w_pad=1.5);      

ax[0].scatter(EB, OB, s=Log(TB), c='Black', label='Teegarden b');
ax[0].set_xlabel('Eccentricity', fontsize=8);
ax[0].set_ylabel('Obliquity (deg)', fontsize=12);
ax[0].set_ylim(0,3)
ax[0].legend(loc='best')

ax[1].scatter(EC, OC, s=Log(TC), c='Black', label='Teegarden c');
ax[1].set_xlabel('Eccentricity', fontsize=8);
ax[1].set_ylabel('Obliquity (deg)', fontsize=12);
#ax[0].set_ylim(0,50)
ax[1].legend(loc='best')

plt.show()

if (sys.argv[1] == 'pdf'):
    fig.savefig("Scatter.pdf", bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig("Scatter.png", bbox_inches="tight", dpi=600)
