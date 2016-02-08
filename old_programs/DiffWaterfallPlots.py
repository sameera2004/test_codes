'''***********************************************************************************
      
	This program produce Differnt Waterfall Plots from 1D X-ray Diffraction Data		

	File Coded by : Sameera Abeykoon

 **************************************************************************************'''


import numpy as np
import os,sys
from os.path import exists
import glob
import re
#import matplotlib
import pylab 
from pylab import*
import matplotlib.pyplot as plt
import matplotlib.cm
from pylab import figure, draw, zeros_like
from mpl_toolkits.mplot3d import Axes3D


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
    A = np.sort(A)
    s = len(A)
    no_columns = 2*s-1
    fcmap = matplotlib.cm.get_cmap()
	
    data = [np.loadtxt(f, usecols=[0, 1], unpack=False,skiprows=32) for f in A] 
    Data = np.concatenate(data, axis=1)                         	
    d = Data[:, r_[0, 1:no_columns:2]].T
    savetxt(path+'Data_chi.dat',d, fmt='%g')            
    Data = np.loadtxt(path+'Data_chi.dat', unpack='True')
    return Data


def Plot_waterfall(dirpath):
    #Plot the waterfall plots of 1D diffraction data with different tempertures

    Data = OneD_Data(dirpath) # 1D X-ray diffratction data

    T = Read_Temp(dirpath)    # Tempetures
    s = len(T)
    Tlo = min(T)
    Thi = max(T)
    
    fcmap = matplotlib.cm.get_cmap()
 
    plt.figure()
    plt.title("X-Ray Diffraction Data")
    plt.xlabel("Q (${nm}^{-1}$)")
    plt.ylabel("Intensity")

    for i in range (1,s):
	Ti = T[i - 1]
	color = fcmap((Ti - Tlo) / (1.0 * Thi - Tlo))
    	plt.plot(Data[:,0],Data[:,i] + (i*10000),color=color,alpha=.8)
    show()
    return


def Plot_waterfallN(dirpath):
    #Plot the waterfall plots of 1D normalized (direct x-ray intensity) diffraction data with different tempertures 

    Data = OneD_Data(dirpath) # 1D X-ray diffratction data

    T = Read_Temp(dirpath) # Tempetures
    s= len(T)   
    Tlo = min(T)
    Thi = max(T)

    I0 = Read_DirectIntensity(dirpath)  # Direct Intensity of X-ray beam
	
    fcmap = matplotlib.cm.get_cmap()
 
    plt.figure()
    plt.title("X-Ray Diffraction Data")
    plt.xlabel("Q (${nm}^{-1}$)")
    plt.ylabel("Normalized Intensity")

    for i in range (1,s):
	Ti = T[i - 1]
	Ii = I0[i - 1]
    	color = fcmap((Ti - Tlo) / (1.0 * Thi - Tlo))
    	plt.plot(Data[:,0],Data[:,i]/Ii + (i*10),color=color,alpha=.8)	    
    show()
    return


def Plot_3Dwaterfall(dirpath):
    #Plot the waterfall plots of 1D diffraction data with different tempertures

    Data = OneD_Data(dirpath) # 1D X-ray diffratction data

    T = Read_Temp(dirpath)    # Tempetures
    s= len(T)
    Tlo = min(T)
    Thi = max(T)
    
    fcmap = matplotlib.cm.get_cmap()

    fig = figure()
    ax3 = Axes3D(fig)
    pylab.title("X-ray Diffraction Data- WaterFall Plot")
    pylab.xlabel("Q (${nm}^{-1}$)")
    pylab.ylabel("Temperature (K)")
    xi=Data[:,0]

    # this sets the view elevation and azimuth in degrees
    ax3.view_init(20, 220)
    for i in range(1,s): 
        zi=Data[:,i] # zi=Data[p:q,0]
        Ti = T[i - 1]
	color = fcmap((Ti - Tlo) / (1.0 * Thi - Tlo))
    	yi = (pylab.zeros_like(xi)+i)
    	ax3.plot(xi, (((yi/yi)-1)+Ti), zi, color=color)
    show()
    return


def Plot_3DwaterfallN(dirpath):
    #Plot the 3D waterfall plots of 1D normalized (direct x-ray intensity) diffraction data with different tempertures 

    Data = OneD_Data(dirpath) # 1D X-ray diffratction data

    T = Read_Temp(dirpath)    # Tempetures
    s = len(T)
    Tlo = min(T)
    Thi = max(T)

    I0 = Read_DirectIntensity(dirpath)  # Direct Intensity of X-ray beam
      
    fcmap = matplotlib.cm.get_cmap()

    #  Give values to select the X and Y range
    p = 0  
    q = 300

    fig = figure()
    ax3 = Axes3D(fig)
    pylab.title("X-ray Diffraction Data- Normalized Intensity")
    pylab.xlabel("Q (${nm}^{-1}$)")
    pylab.ylabel("Temperature (K)")
    xi=Data[p:q,0]

    # this sets the view elevation and azimuth in degrees
    ax3.view_init(20, 220)
    for i in range(1,s): 
        Ti = T[i - 1]
	Ii = I0[i - 1]
	zi = Data[p:q,i]/Ii # zi=Data[p:q,0]
    	color = fcmap((Ti - Tlo) / (1.0 * Thi - Tlo))
    	yi = (pylab.zeros_like(xi)+i)/Ii
    	ax3.plot(xi, (((yi/yi)-1)+Ti), zi, color=color)
    show()
    return


if __name__ == "__main__":
    path=os.path.join(os.getcwd())
    Plot_waterfall(path)
    Plot_waterfallN(path)
    Plot_3Dwaterfall(path)
    Plot_3DwaterfallN(path)
