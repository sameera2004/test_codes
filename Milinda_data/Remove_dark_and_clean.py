# This module will open .tiff files and do the dark file subtraction

import numpy as np
import fabio
import glob
import os, sys
import matplotlib.pyplot as plt


def load_tif(file):
    """
    Parameters
    ----------
    file : string
    Complete path to the file to be loaded into memory

    Returns
    -------
    output: NxN ndarray
    Returns a numpy array of the same data type as the original tiff file
    """
    image = fabio.open(file)
    image_data = image.data
    return image_data

def remove_dark(A):
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
    
    clean_data = []  # save the cleaned data
    
    for name in A:
        if "dark" in name:   # check the dark files
            dark_data = load_tif(name)  
            print ("+++++ bad" , name)
        else:
            arr = load_tif(name)
            print ("good", name)
            #  clean the data
            clean_data.append(arr - dark_data)  
    return np.asarray(clean_data)
    
    
if __name__ == "__main__":
    data_dir = "/Volumes/MILINDA/"
    A = glob.glob(os.path.join(data_dir, "*tiff"))
    
    print len(A)
    
    clean_data = remove_dark(A)
    
    print (clean_data.shape)
    
    fig = plt.subplot()
    plt.imshow(clean_data[0])
    plt.show()
     