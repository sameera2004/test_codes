#!/usr/bin/env python
############################################################################
#    Statistics or Reduced Representation of 2D images
#   (Mean, Total Intensity, Standard Deviation )
#   Note : - Read the .tiff file(load_tif) using FabIO
#
#
#               Brookhaven Nationla Laboratotry
#               NSLS - II Data Project
#  File Coded by: Sameera Abeykoon
#
#
#
##############################################################################


import os
import sys
import numpy as np
import glob
import matplotlib.pyplot as plt
import fabio


def load_tif(file):
    """
    Parameters
    ----------
    file_name: string
    Complete path to the file to be loaded into memory
    ----------------------------------------------------
    Returns
    -------
    output: NxN ndarray
    Returns a numpy array of the same data type as the original tiff file
    """
    filename = os.path.basename(file)
    print('loading ' + filename)
    image = fabio.open(file)
    image_data = image.data
    return image_data


def RR_MPlot(x, rrdatam, rrdatat, rrdatas, norm=None):
    '''
    Parameters
    ----------
    x = ndarray
    length M array of x values
    rrdatam : ndarray
    MxN array of data
    rrdatat : ndarray
    MxN array of data
    rrdatas : ndarray
    MxN array of data
    norm : scalar, ndarray or None
    if None, defaults to 1.  Valure used to normalize data.
    Returns
    -------
    -------------------------------
    Reduced Representation Choices
    --------------------------------
    Mean
    Total Intensity
    Standard Deviation
    '''
    f, axarr = plt.subplots(3, sharex=True)
    axarr[0].scatter(x, rrdatam)
    axarr[0].set_title('Reduced Representation')
    axarr[0].set_ylabel('Mean')
    axarr[1].scatter(x, rrdatat)
    axarr[1].set_ylabel('Total Intensity')
    axarr[2].scatter(x, rrdatas)
    axarr[2].set_ylabel('Standard Devaition')
    plt.show()
    return


def RRMChoice(dirpath):
    print 'Reduced Representation of 2D image Data'
    A = glob.glob(os.path.join(dirpath, '*.tif'))
    rrdatam = np.array([])
    rrdatat = np.array([])
    rrdatas = np.array([])
    noTif = len(A)
    for file in A:
        image_data = load_tif(file)
        rrm = np.mean(image_data)
        rrt = np.sum(image_data)
        rrs = np.sum(image_data)
        image_data = None
        rrdatam = np.append(rrdatam, rrm)
        rrdatat = np.append(rrdatat, rrt)
        rrdatas = np.append(rrdatas, rrs)
    x = np.arange(noTif)
    RR_MPlot(x, rrdatam, rrdatat, rrdatas)
    return x, rrdatam, rrdatat, rrdatas


def RR_Plot(x, rrdata, Title):
    '''
    Parameters
    ----------
    x = ndarray
    length M array of x values
    rrdatam : ndarray
    MxN array of data
    Title : string
    Choice of reduced representation
    norm : scalar, ndarray or None
    if None, defaults to 1.  Valure used to normalize data.
    Returns
    -------
    -------------------------------
    Reduced Representation Choices
    --------------------------------
    Mean
    Total Intensity
    Standard Deviation
    '''
    f, ax = plt.subplots()
    ax.scatter(x, rrdata)
    ax.set_title('Reduced Representation: '+Title)
    ax.set_ylabel(Title)
    plt.show()
    return


def RR1Choice(dirpath):
    print 'Reduced Representation of 2D image Data'
    print 'Mean( type m), Total Intensity(type t), Standard Deviation(type s)'
    rrchoice = raw_input('Please enter the reduced reprensentation ')
    print 'You Entered = ', rrchoice
    #
    if rrchoice == 'm':
        f = lambda x: np.mean(x)
        Title = 'Mean'
    elif rrchoice == 't':
        f = lambda x: np.sum(x)
        Title = 'Total Intensity'
    elif rrchoice == 's':
        f = lambda x: np.std(x)
        Title = 'Standard Deviation'
    A = glob.glob(os.path.join(dirpath, '*.tif'))
    rrdata = np.array([])
    noTif = len(A)
    for file in A:
        image_data = load_tif(file)
        rr = f(image_data)
        image_data = None
        rrdata = np.append(rrdata, rr)
    x = np.arange(noTif)
    RR_Plot(x, rrdata, Title)
    return x, rrdata, Title


if __name__ == '__main__':
    dirpath = os.path.join(os.getcwd())
    print 'Reduced Representation of 2D Image'
    # RR1Choice(dirpath) # for one choice of reduced representation
    RRMChoice(dirpath)

# End of the File
