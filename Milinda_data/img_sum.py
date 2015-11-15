"""
This module will open .tiff files and add them and give
the average image
"""

import numpy as np
import fabio
import glob
import os, sys
import DM3lib as dm3


def sum_img(img_array):
    """
    This will provide the average value of the images
    Parameters
    ----------
    img_array: ndarray
        array of stack of images for one time correlation

    n_start: int
        starting image number

    n_end: int
        number of images

    Returns
    ------
    sum_img : array
        sum of all image arrays

    avg_img : array
        average of the images

    """
    sum_img = 0
    counter= 0
    for n in range(len(img_array)):
        sum_img += img_array[n]
        counter += 1
    sum_img = np.asarray(sum_img)
    avg_img = sum_img / (counter)
    return sum_img, avg_img


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

    print('loading ' + file)
    image = fabio.open(file)
    print image
    print image.shape
    image_data = image.data
    print 'Volume loaded successfully'
    return image_data


def load_dm3(file):
    """
    Parameters
    ----------

    Parameters
    ----------
    file : string
    Complete path to the file to be loaded into memory

    Returns
    -------
    output: NxN ndarray
    Returns a numpy array of the same data type as the original tiff file
    """
    image = dm3.DM3(file)
    image_data = image.imagedata

    return image_data


def check_words_filenames(A):
    """
    Parameters
    ----------
    A : list
        list contains all the *.tiff files
        (even *raw.tif,  *drak.tif, *metadata.tif)

    Returns
    -------
    B : list
        list now only contains *tif files
        after removing *raw.tif,  *drak.tif, *metadata.tif
    """
    words = ['metadata','raw','dark']
    B = []
    for filename in A:
        for i in words:
            if i in filename:
                B.append(filename)
    return B


if __name__ == "__main__":
    data_dir = raw_input("Enter the data directory path ")
    # eg: /Volumes/Data/BeamLines/XPD/tiff_files/Standard_Ni/

    A = glob.glob(os.path.join(data_dir, '*.dm3'))

    # find the new list with raw, metadata and dark in *tif
    B = check_words_filenames(A)

    # remove *dark.tif, *raw.tif, *metadata.tif
    C = [x for x in A if x not in B]

    img_stack = []
    for file in C:
        img_stack.append(load_dm3(file))

    sum_img, avg_img = sum_img(np.asarray(img_stack))





