#The Tidal HEating Substraction Plot shows the net tidal heating due to a Cassini State.

#This script will create the control directory for THeSP to function. This control
#state needs to be run with vplanet separately.

#Thanks to Dr. David Fleming, whose code I based this script on for 
#VPlanet compatibility.
import os
import sys
import re
import shutil
import fileinput


#Definitions
def Seek(log, pattern):
    for line in log:
        result = re.findall(pattern, line)
        if len(result) != 0:
            return(result)
        #For not numbers
def Find(log, pattern):
    for line in log:
        result = re.findall(pattern, line)       
        if len(result) != 0:
            result = re.findall("\d+.\d+", result[0])
            result = float(result[0])
            return (result)
            #for numbers
def Copy(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
        
#User Inputs
InputDir = input("Input Directory:")

"""
What this thing needs to do:
    XFind the TGard.log file of each sim.
    XFind the final eccentricity of b and c and store them.
    XMake a copy of the folder. The whole thing. this is the control directory.
    XReplace all Eccentricities with the final ones stored.
    XSet ob to 0.
    XFind all instances of vpl.in
    X    set bDoForward to 0.
    Run multi-planet on the control directory.
        ask for the number of cores of the user.
"""
BEL=[]
CEL=[]

for root, dirs, files in os.walk(InputDir, topdown=False):
   for name in files:
        if name == "TGard.log":
            #print("File:" + os.path.join(root, name))
            LogName = str(os.path.join(root, name))
        #Isolation:
#Read in log files
            with open (LogName, 'rt') as log: 
                #Finding final b ecc
                fin = Seek(log,"----\sFINAL\sSYSTEM\sPROPERTIES\s----")
                bod = Seek(log, "-----\sBODY:\sTGb\s----") 
                ecc = Find(log, ".Eccentricity..*\d+.\d+")
#Example: (Eccentricity) Orbital Eccentricity []: 0.140092 
                BEL.append(ecc)            
            with open (LogName, 'rt') as log: 
                #Finding final c ecc
                fin = Seek(log,"----\sFINAL\sSYSTEM\sPROPERTIES\s----")
                bod = Seek(log, "-----\sBODY:\sTGc\s----") 
                ecc = Find(log, ".Eccentricity..*\d+.\d+")
          
                CEL.append(ecc)   
print("BEL"+str(len(BEL)))
print("CEL"+str(len(CEL)))
print("Files Found")


#Making a copy of InputDir as ConDir
ConDir = InputDir+"_CTRL"
print("Copying files...")
Copy(InputDir, ConDir)
#Commented for now because it works fine. 
#It'll just throw an error and keep going in the wild
print("Control Copy Created")

#Now in ConDir, make Obliquity 0 and Ecc match the previous one in both files.
#Then set all bDoForward to 0 so it doesn't run the full evolution.
nb=0 
nc=0
#These are trackers so we don't get lost in our files and lists.
for root, dirs, files in os.walk(ConDir, topdown=False):
    for name in files:
        if name == "TGb.in":
            #print("File:" + os.path.join(root, name))
            LogName = str(os.path.join(root, name))
            with open (LogName, 'rt') as log:
                #Set Obliquity to Zero
                obzero = "dCosObl " + "    0" + "    #Zeroed"
                ogecc= "dEcc    "+str(BEL[nb])+"    #Final Eccentricity"
                rmrot= "#Removed dRotPeriod"
            for line in fileinput.input(LogName, inplace=True):
                if "dCosObl" in line:
                    line = re.sub("dCosObl.*", obzero, line)
                if "dEcc" in line:
                    line = re.sub("dEcc.*", ogecc, line)
                if "dRotPeriod" in line:
                    line = re.sub("dRotPeriod.*", rmrot, line)
                    print("bForceEqSpin    1     #Tidal Lock")
                print("{}".format(line), end='')
            nb=nb+1
        if name == "TGc.in":
            #print("File:" + os.path.join(root, name))
            LogName = str(os.path.join(root, name))
            with open (LogName, 'rt') as log:
                #Set Obliquity to Zero
                obzero = "dCosObl " + "    1" + "    #Zeroed"
                ogecc= "dEcc    "+str(CEL[nc])+"    #Final Eccentricity"
                rmrot= "#Removed dRotPeriod"
        #print(obzero)
                #print(ogecc)
            
            for line in fileinput.input(LogName, inplace=True):
                if "dCosObl" in line:
                    line = re.sub("dCosObl.*", obzero, line)
                if "dEcc" in line:
                    line = re.sub("dEcc.*", ogecc, line)
                if "dRotPeriod" in line:
                    line = re.sub("dRotPeriod.*", rmrot, line)
                    print("bForceEqSpin    1     #Tidal Lock")
                print("{}".format(line), end='')
            nc=nc+1
        if name == "vpl.in":
            print("File:" + os.path.join(root, name))
            LogName = str(os.path.join(root, name))
            with open (LogName, 'rt') as log:
                #Set Obliquity to Zero
                dozero = "dStopTime    0    #No Evolution"
                gozero = "dOutputTime    0        #No Evolution"
                print(dozero)
            for line in fileinput.input(LogName, inplace=True):
                if "dStopTime" in line:
                    line = re.sub("dStopTime.*", dozero, line)
                if "dOutputTime" in line:
                    line = re.sub("dOutputTime.*", gozero, line)
                print("{}".format(line), end='')     
       
#print("b", nb, "c", nc)
#This checks the trackers, they should be equal to each other and the no. of sims
print("Files Edited")

#Need to create a "vspace.in" file for CTRL...
f= open("ctrl.in", "a+")    
for line in f:
    #f.write("srcfolder  .")
    f.write("destfolder  "+str(ConDir))
f.close()
#Note: This doesn't work, keep working on it later. Can do manually.

"""
#Now we run vplanet on ConDir and wait.
#os.system('cmd /k "multi-planet ./ctrl.in 5 >&TGMC_CTRL.out"')
#print("All Done!")
"""