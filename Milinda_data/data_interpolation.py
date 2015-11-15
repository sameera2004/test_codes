import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import glob
import os, sys


def data_intrepolate(data_files, skiprows=4):
    """
    Parameters
    ----------
    data_files : files
        chi data files
    skiprows : int
        number of rows to skip to open the data file
        
    Returns
    -------
    old_data : array
        old data array
        shape [number of files, number of rows of data, number of columns=2]
        
    fix_data : array
        fixed y(intensity) array
        shape [number of files, number of rows of data]
    """
    Data = []
    i_data = []
    for data_file in data_files:
        #  open each data file
        data = np.loadtxt(data_file, skiprows=skiprows)
        Data.append(data) # write them to a list
        
        # There is a issue in the data between data[1205:1215, 0] therefore,
        # we want to remove that region
        x1, f_d1 = _process(data, 1150, 1205, 1215, 1265)
        
        # There is a issue in the data between data[1326:1332, 0] therefore,
        # we want to remove that region
        x2, f_d2 = _process(data, 1280, 1326, 1332, 1400)

        #  Now have to recreate the y values(intensity) using the new interpolation
        # values created from the new functions, have to find carefully the data points
        # for the f_d1 and f_d2 functions, can get a idea from x1 and x2 see whther
        # they at end1, start2 positions in the data set
        y1 = np.concatenate((data[0:1206, 1], f_d1[56:64]), axis=0)
        y2 = np.concatenate((y1, data[1214:1324, 1]), axis=0)
        y3 =  np.concatenate((y2, f_d2[44:53]), axis=0)
        y = np.concatenate((y3, data[1333::,1]), axis=0)
        i_data.append(y)
        #y.shape
        
        old_data = np.asarray(Data)
        fix_data = np.asarray(i_data)
        
    return old_data, fix_data


def _process(data, start1, end1, start2, end2):
    """
    Parameters
    ----------
    data : array
        data array shape (number of rows, number of cloums=2)
    start1 : int
        for interpolation the data, it need atleast 100 data points
        therefore start1 and end2 is just to chosse the data to see
        the bahaviour of the function
        
    end1 : int
        starting point of the data that we want to remove
    
    start2 : int
        end point of the data that we want to remove
    
    end2 : int
        for interpolation the data, it need atleast 100 data points
        therefore start1 and end2 is just to chosse the data to see
        the bahaviour of the function    
    """
    # There is a issue in the data between data[end1:start2, 0] therefore,
    # we want to remove that region
    x_d = np.concatenate((data[start1:end1, 0], data[start2:end2, 0]), axis=0)
    y_d = np.concatenate((data[start1:end1, 1], data[start2:end2, 1]), axis=0)

    # intreploation  function
    # has to behave as the x_d value and y_d values
    f_d = interp1d(x_d, y_d, bounds_error=False,
                    fill_value=0.,kind='cubic' )
    x = np.linspace(data[start1, 0], data[end2, 0] , (end2-start1))
        # create x data values for interpolation

    return x, f_d(x)


if __name__  ==  "__main__":
    data_dir = "/Volumes/Data/BeamLines/Milinda_Data/interpolation/"
    A = glob.glob(os.path.join(data_dir, '*.chi'))
                  
    old_data, fix_data = data_intrepolate(A, skiprows=4)
    
    #plot the results(old_data, fix_data)              
    plt.figure()    
    for i in range(0, old_data.shape[0]):
        plt.plot(old_data[i][:, 0], old_data[i][:, 1], '-b',
                 old_data[i][:, 0], fix_data[i], '-r')
        plt.legend(["data", "i_data"], loc='best')
    plt.show()