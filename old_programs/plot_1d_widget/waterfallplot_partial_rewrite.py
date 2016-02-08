'''  *********************************************************************
	This program produce differnt Waterfall plots

	1. In the first part extracts tempertaure data and direct intensity of X-ray's data ( Before hiting the sample S[5] ) 
	   from the .tif.metadata file for differnt integartion files.

	2. In the second parts take the integartion files (.chi) of the 2D X-ray Diffraction image (tif file)
   	   as an input and produce differnt waterfall plots		

 **************************************************************************'''

import numpy as np
import os,sys
from os.path import exists
import glob
import re
import matplotlib
import pylab 
from pylab import*
import matplotlib.pyplot as plt
import matplotlib.cm
from pylab import figure, draw, zeros_like
from mpl_toolkits.mplot3d import Axes3D

def Temp_Intensity():
	path=os.path.join(os.getcwd())
	AA=glob.glob("*.metadata")
	for file in AA:
    		if file.endswith("*.raw.tif.metadata"):
        		#print file
			#for file in glob.glob("*.")
			print "metadata exits"
			A = glob.glob('*.raw.tif.metadata')
		elif file.endswith("*.tif.metadata"):
			A = glob.glob('*.tif.metadata')
	#A = glob.glob('*.tif.metadata')	
	A = np.sort(A)
	
	# Write Temperture data and Direct Intensity of X-ray's 
	#data  in the (metadata) file to 2 differnet files
	f = open("Temp.dat","w")
	f1 = open("I0.dat","w")
	
	for file in A:
		file1 = open(file,"r")
		for line in file1:
        		if 'temperature' in line:
				y=(line.split("temperature=")[1])
				y1=re.sub('["]', '', y)
				y1=float(y1)
				f.write("%f \n" %y1)
			if 'S[5]' in line:
				s = (line.split('S[5]=')[1])
				s = s.partition('S')
				s1 = re.sub('["]', '', s[0])
				s1 = float(s1)
				f1.write("%s \n" %s1)
						
	f.close()
	f1.close()	

def _create_plot_component():
	path=os.path.join(os.getcwd())
	A = glob.glob('*.chi') 
	A=np.sort(A)
	s=len(A)
	T = np.loadtxt('Temp.dat', unpack=True) 
	#T = sort(Temp)
	Tlo = min(T)
	Thi = max(T)
	I0 = np.loadtxt("I0.dat",unpack=True)	
	fcmap = matplotlib.cm.get_cmap()
	no_columns = 2*s-1
	data = [np.loadtxt(f, usecols=[0, 1], unpack=False,skiprows=32) for f in A] 
	Data = np.concatenate(data, axis=1)                         	
	d = Data[:, r_[0, 1:no_columns:2]].T
	savetxt(path+'Data_chi.dat',d, fmt='%g')            
	Data = np.loadtxt(path+'Data_chi.dat', unpack='True')	

	plt.figure()
	plt.title("X-Ray Diffraction Data")
	plt.xlabel("Q (${nm}^{-1}$)")
	plt.ylabel("Intensity")

	for i in range (1,s):
		Ti = T[i - 1]
		Ii = I0[i - 1]
    		color = fcmap((Ti - Tlo) / (1.0 * Thi - Tlo))
    		plt.plot(Data[:,0],Data[:,i] + (i*10000),color=color,alpha=.8)	

	plt.figure()
	plt.title("X-Ray Diffraction Data")
	plt.xlabel("Q (${nm}^{-1}$)")
	plt.ylabel("Normalized Intensity")

	for i in range (1,s):
		Ti = T[i - 1]
		Ii = I0[i - 1]
    		color = fcmap((Ti - Tlo) / (1.0 * Thi - Tlo))
    		plt.plot(Data[:,0],Data[:,i]/Ii + (i*10),color=color,alpha=.8)	
	

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
		Ii = I0[i - 1]
    		color = fcmap((Ti - Tlo) / (1.0 * Thi - Tlo))
    		yi = (pylab.zeros_like(xi)+i)/Ii
    		ax3.plot(xi, (((yi/yi)-1)+Ti), zi, color=color)

	#  Give values to select the X and Y range
	p=0  
	q=300

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
		zi=Data[p:q,i]/Ii # zi=Data[p:q,0]
    		color = fcmap((Ti - Tlo) / (1.0 * Thi - Tlo))
    		yi = (pylab.zeros_like(xi)+i)/Ii
    		ax3.plot(xi, (((yi/yi)-1)+Ti), zi, color=color)

def read_input_files(fpath, patterne,..):
    pass
    return data, q_vec, T
	
def plot_diff(ax, data, q_vec, c, norm=None):
    """
    Parameters
    ----------
    ax : Axes
        The axes to plot into
    data : ndarray
        MxN array of data
    q_vec : ndarray
        length M array of q-values
    c : ndarray
        scalars to be used for color mapping
    norm : scalar, ndarray or None
        if None, defaults to 1.  Valure used to normalize data.

    Returns
    -------
    lns : list
        list of line artists returned
    """
    if norm is None:
        norm = 1
    lns = []
    data = data / norm
    
    for d, _c in zip(data, c):
        ln, = ax.plot(q, d, color=_c)
    	lns.append(ln)
    return lns


if __name__ == "__main__":
    
    Temp_Intensity()
    _create_plot_component()
    show()
