'''***********************************************************************************

	This program produce Differnt Waterfall Plots from 1D X-ray Diffraction Data

	File Coded by : Sameera Abeykoon

 **************************************************************************************'''

import numpy as np
import os,sys
from os.path import exists
import glob
import re
import matplotlib
from pylab import*
import matplotlib.pyplot as plt
import matplotlib.cm
# from pylab import figure, draw, zeros_like
from mpl_toolkits.mplot3d import Axes3D


def OneD_Data(path):
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


def plot_diff(ax, data, temp, intensity, c, norm=None):
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


def Plot_waterfallN(data, temp, inten, fcmap):
    # Plot the waterfall plots of 1D normalized (direct x-ray intensity)
    # diffraction data with different tempertures

    plt.figure(1)
    plt.title("X-Ray Diffraction Data")
    plt.xlabel("Q (${nm}^{-1}$)")
    plt.ylabel("Normalized Intensity")

    for i in range (1, len(temp)):
	Ti = temp[i - 1]
	Ii = inten[i - 1]
    	color = fcmap((Ti - min(temp)) / (1.0 * (max(temp) - min(temp))))
    	plt.plot(Data[:, 0],Data[:, i]/Ii + (i*10),color=color, alpha=.8)
    plt.show()
    return

def Plot_3Dwaterfall(Data, temp, intensity, fcmap):
    #Plot the waterfall plots of 1D diffraction data with different tempertures

    fig = plt.figure(1)
    ax3 = Axes3D(fig)
    plt.title("X-ray Diffraction Data- WaterFall Plot")
    plt.xlabel("Q (${nm}^{-1}$)")
    plt.ylabel("Temperature (K)")
    xi=Data[:, 0]

    # this sets the view elevation and azimuth in degrees
    ax3.view_init(20, 220)
    for i in range(1, len(temp)):
        zi=Data[:, i] # zi=Data[p:q,0]
        Ti = temp[i - 1]
	    color = fcmap((Ti - min(temp)) / (1.0 * (max(temp) - min(temp))))
    	yi = (plt.zeros_like(xi) + i)
    	ax3.plot(xi, (((yi/yi)-1)+Ti),  zi,  color=color)
    plt.show()
    return


if __name__ == "__main__":
    dirpath=os.path.join(os.getcwd())
    Data = OneD_Data(dirpath) # 1D X-ray diffratction data

    T = Read_Temp(dirpath) # Tempetures
    I0 = Read_DirectIntensity(dirpath)  # Direct Intensity of X-ray beam

    fcmap = matplotlib.cm.get_cmap()

    Plot_waterfallN(Data, T, I0, fcamp)

    Plot_3Dwaterfall(Data, T, I0, fcmap)