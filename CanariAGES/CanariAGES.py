#CanariAGES takes a basic VSPACE run output, from the log file, as a Canari input.
#Output is AGES, which is a copy of CANARI input but starting from it's final values
#allowing it to be run for the age of the system.
#See comment block below imports for details.

import os
import re
import shutil
import fileinput
import math
import numpy as np

"""
WHAT THIS THING NEEDS TO DO
X? Find all relevant parameters (targets*) in the CANARI
X Create a Copy of the CANARI as AGES
X? Replace all targets with their final values


*TARGETS ARE:
CosObl (AGES.in add, ignore)
RotPer (AGES.in add, keep anyway, do 2 AGES runs, one with replacement and one without)
Eccentricity
OrbPeriod
ArgP (math into LongP)
PrecA (AGES.in add, ignore)
Inclination
LongA

Make sure the Masses and Radii of the planets are the same across transfer.
WATCH OUT FOR CONVERSIONS

NOTE:
If running bycn/bncy runs, AGES will have to be run on each one individually
This doesn't handle split runs automatically.

When running afterwards, need to create an ages.in file, a vspace.in equivalent, 
to run from so we don't mess anything up. Remember to change the name.
"""

#CANARI = input("Input Directory:")
CANARI = "./Test"

#Definitions
    ##Value Hunters
def Strip(pattern):      
    result = re.findall("\d+.\d+..\d+", pattern)
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
        ##Logistics
def Copy(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
        ##Math
def Decon(list):
    for index in range(0,len(list)):
        list[index] = np.array(list[index], dtype=float)
        list[index] = math.degrees(list[index])
    return(list)
def makeDay(list):
    for index in range(0,len(list)):
        list[index] = np.array(list[index], dtype=float)
        list[index] = list[index] / 86400
    return(list)

#Arrays for sorting the values. 
EB=[]
OB=[]
RB=[]
#AB=[]
IB=[]
LB=[]
PB=[]

EC=[]
OC=[]
RC=[]
#AC=[]
IC=[]
LC=[]
PC=[]

#the AC/B list is for storing the argument of pericentre, should it be needed.


#Collection of CANARI files:
for root, dirs, files in os.walk(CANARI, topdown=False):
    for name in files:
        if name == "TGard.log":
            LogName = str(os.path.join(root, name))
            #Only need FINAL values
            with open (LogName, 'rt') as log: 
                Seek(log,"----\sFINAL\sSYSTEM\sPROPERTIES\s----") 
                
                Seek(log, "-----\sBODY:\sTGb\s----")
                rb = Find(log, "\(RotPer\)")
                ecb= Find(log, "\(Eccentricity\)")
                opb= Find(log, "\(OrbPeriod\)")
                apb= Find(log, "\(ArgP\)")
                inb= Find(log, "\(Inc\)")
                lab= Find(log, "\(LongA\)")
                EB.append(ecb)
                RB.append(rb)         
                OB.append(opb)   
                #AB.append(apb)
                IB.append(inb)
                LB.append(lab)
                PB.append(apb+lab)

                Seek(log, "-----\sBODY:\sTGc\s----")
                rc= Find(log, "\(RotPer\)")
                ecc= Find(log, "\(Eccentricity\)")
                opc= Find(log, "\(OrbPeriod\)")
                apc= Find(log, "\(ArgP\)")
                inc= Find(log, "\(Inc\)")
                lac= Find(log, "\(LongA\)")
                EC.append(ecc)
                RC.append(rc)
                OC.append(opc)
                #AC.append(apc)
                IC.append(inc)
                LC.append(lac)
                PC.append(apc+lac)
                
print ("Files Found")

print('B')
print(IB)
#print(AB)
print(OB)  
print('C')
print(IC)
#print(AC)
print(OC)

#Math
for list in IB, IC, LB, LC, PB, PC:
    Decon(list)
for list in OB, OC:
    makeDay(list)

#Just a checkpoint, comment out if working
print('B')
print(IB)
#print(AB)
print(OB)  
print('C')
print(IC)
#print(AC)
print(OC)

#Creating AGES Directory
AGES = CANARI+"_AGES"
print("Copying files...")
Copy(CANARI, AGES)
print("AGES Copy Created")



#Modifying the AGES Directory to match final CANARI values
nb=0 
nc=0
#These are trackers so we don't get lost in our files and lists.
for root, dirs, files in os.walk(AGES, topdown=False):
    for name in files:
        if name == "TGb.in":
            #print("File:" + os.path.join(root, name))
            LogName = str(os.path.join(root, name))
            with open (LogName, 'rt') as log:
                agpr="dRotPeriod    -"+str(RB[nb])+"    #Final Rotation Period"
                agec= "dEcc    "+str(EB[nb])+"    #Final Eccentricity"
                agob="dOrbPeriod    -"+str(OB[nb])+"    #Final Orbital Period"
                agin="dInc    "+str(IB[nb])+"    #Final Inclination"
                agla="dLongA    "+str(LB[nb])+"    #Final Ascending Node"
                aglp="dLongP    "+str(PB[nb])+"    #Final Longitude of Pericentre"
            for line in fileinput.input(LogName, inplace=True):
                if "dRotPeriod" in line:
                    line = re.sub("dRotPeriod.*", agpr, line)
                if "dEcc" in line:
                    line = re.sub("dEcc.*", agec, line)
                if "dOrbPeriod" in line:
                    line = re.sub("dOrbPeriod.*", agob, line)   
                if "dInc" in line:
                    line = re.sub("dInc.*", agin, line)
                if "dLongA" in line:
                    line = re.sub("dLongA.*", agla, line)
                if "dLongP" in line:
                    line = re.sub("dLongP.*", aglp, line) 
                print("{}".format(line), end='')
            nb=nb+1
        if name == "TGc.in":
            #print("File:" + os.path.join(root, name))
            LogName = str(os.path.join(root, name))
            with open (LogName, 'rt') as log:
                agpr="dRotPeriod    -"+str(RC[nc])+"    #Final Rotation Period"
                agec= "dEcc    "+str(EC[nc])+"    #Final Eccentricity"
                agob="dOrbPeriod    -"+str(OC[nc])+"    #Final Orbital Period"
                agin="dInc    "+str(IC[nc])+"    #Final Inclination"
                agla="dLongA    "+str(LC[nc])+"    #Final Ascending Node"
                aglp="dLongP    "+str(PC[nc])+"    #Final Longitude of Pericentre"
            for line in fileinput.input(LogName, inplace=True):
                if "dRotPeriod" in line:
                    line = re.sub("dRotPeriod.*", agpr, line)
                if "dEcc" in line:
                    line = re.sub("dEcc.*", agec, line)
                if "dOrbPeriod" in line:
                    line = re.sub("dOrbPeriod.*", agob, line)   
                if "dInc" in line:
                    line = re.sub("dInc.*", agin, line)
                if "dLongA" in line:
                    line = re.sub("dLongA.*", agla, line)
                if "dLongP" in line:
                    line = re.sub("dLongP.*", aglp, line) 
                print("{}".format(line), end='')
            nc=nc+1
        print("b", nb, "c", nc)
#This checks the trackers, they should be equal to each other and the no. of sims
print("Files Edited")
