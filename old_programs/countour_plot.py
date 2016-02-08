'''  *********************************************************************
      
	This program produce Contour Plots from 1D X-ray Diffraction Data	

	File Coded by : Sameera Abeykoon

 **************************************************************************'''

import numpy as np
import glob
import os,sys
import re
from os.path import exists
import pylab
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.cm
from pylab import figure, draw, zeros_like

def Read_Temp(dirpath):
    # Read the "temperture" from the metadata file
    A = glob.glob('*.tif.metadata')	
    A = np.sort(A)

    f = open("Temp.dat","w")
    Temp = np.array([])

    for file in A:
	file1 = open(file,"r")
	for line in file1:
            if 'temperature' in line:
		y=(line.split("temperature=")[1])
		y1=re.sub('["]', '', y)
		y1=float(y1)
		f.write("%f \n" %y1)
		Temp = np.append(Temp, y1)
    f.close()
    return Temp

def Read_DirectIntensity(dirpath):
    # Read the dircet intensity S[5] from the metadata file
    A = glob.glob('*.tif.metadata')	
    A = np.sort(A)
	
    f = open("I0.dat","w")
    S_Int = np.array([])

    for file in A:
	file1 = open(file,"r")
	
	for line in file1:
           if 'S[5]' in line:
		s = (line.split('S[5]=')[1])
		s = s.partition('S')
		s1 = re.sub('["]', '', s[0])
		s1 = float(s1)
		f.write("%s \n" %s1)
		S_Int = np.append(S_Int, s1)
    f.close()
    return S_Int
	

def OneD_Data(dirpath):
    # Get the data from the *.chi files
	
    A = glob.glob('*.chi')
    A=np.sort(A)
    s=len(A)
    no_columns = 2*s-1
    fcmap = matplotlib.cm.get_cmap()
	
    data = [np.loadtxt(f, usecols=[0, 1], unpack=False,skiprows=32) for f in A] 
    Data = np.concatenate(data, axis=1)                         	
    d = Data[:, r_[0, 1:no_columns:2]].T
    savetxt(path+'Data_chi.dat',d, fmt='%g')            
    Data = np.loadtxt(path+'Data_chi.dat', unpack='True')
    return Data	

def Plot_Contour(dirpath):
    #Plot the Contour plots of 1D diffraction data with different tempertures

    Data = OneD_Data(dirpath)

    T = Read_Temp(dirpath)
    Tlo = min(T)
    Thi = max(T)
	
    plt.figure()
    plt.title("X-Ray Diffraction Data - Contour Plots")
    plt.imshow(Data.T, extent=(0,10000,Tlo,Thi),origin='lower',  interpolation='quadric', aspect='auto')
    colorbar()
    plt.xlabel("r(${\AA}$)")
    plt.ylabel("Temperture (K)")
    grid(True, color = "white")
    show()
    return
    
	
if __name__ == "__main__":
    path=os.path.join(os.getcwd())
    Plot_Contour(path)
    
	
