# This module will open .tiff files and do the dark file subtraction

import numpy as np
import glob
import os, sys
from tifffile import imsave, imread


def remove_dark(A, folder):
    """
    This function will subtract the dark files from the data files
    Parameters
    ----------
    A : list
        list of tiff files
        
    Returns
    -------
    clean_data : array
        dark subtracted data , clean data
        shape (number of clean images, detectore shape 0, detecotor shape 1)
    """
    
    clean_data_arr = []  # save the cleaned data
    for name in A:
        if "dark" in name:   # check the dark files
            dark_data = imread(name)  
            print ("+++++ bad", name)
        else:
            arr = imread(name)
            print ("good", name)
            #  clean the data
            clean_data = arr - dark_data 
            #print (os.path.join(name))
            imsave(name, clean_data)
            clean_data_arr.append(clean_data)
    return np.asarray(clean_data_arr)