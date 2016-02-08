############################################################################
#
# 1. Read the .tiff file(load_tif) using FabIO and plot
#    the 2D image(plot_image)
# 2. Summation of Tiff images
#
#               Brookhaven Nationla Laboratotry
#               NSLS - II Data Project
#  File Coded by: Sameera Abeykoon
#
#
#   FabIO
#   =====
#   FabIO is an I/O library for images produced by 2D X-ray detectors
#   and written in python. FabIO support images detectors from a dozen
#   of companies (including Mar, Dectris, ADSC, Hamamatsu, Oxford,.),
#   for a total of 20 different file formats (like CBF, EDF, TIFF, ...)
#   and offers an unified interface to their headers (as a python dictionary)
#   and datasets (as a numpy ndarray of integers or floats)
#   https://github.com/kif/fabio
#
##############################################################################

import os, sys
import numpy as np
import glob
import matplotlib.pyplot as plt
import fabio
import array
import Image


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
    image = fabio.open(filename)
    image_data = image.data
    plot_image(image.data, filename)
    print 'Volume loaded successfully'
    return image_data


def plot_image(image,filename):
    """  Plot the Image
    Parameters :
    image : NxN array
    image data (N X N array)
    -------------------------------------------------------------
    file : string
    file name ( with complete path)
    """
    plt.figure()
    plt.title(filename)
    plt.imshow(image, cmap='jet',alpha=1)
    plt.show()
    return


def datalist(path):
    A = glob.glob(os.path.join(path, '*.tif')) 
    
    for file in A:
	    image_data = load_tif(file)
        #plot_image(image_data, file)
    return


def DataSumImage(dirpath, y, x):
    """ Parameters
         path :  Complete path to the file to be loaded into memory
    """
    A = glob.glob(os.path.join(dirpath, '*.tif'))
    A = np.sort(A)
   
    Image1Data = np.array([])
    Image2 Data = np.array([])
    ImageSum = np.array([])
    n = 0
    if y in A:
        Image1Data = load_tif(file)
        ImageSum = np.array(Image1Data)
        for files in A:
            for file in files:
                Image2Data = load_tif(file)
                ImageSum = ImageDataSum(ImageSum, Image2Data)
        print ImageSum[1000, 1000]
        n += 1
    return ImageSum


def ImageDataSum(SumImage, Image2):

    """ Summation of images (N X N array)
    Parameters:
    -------------------------------------
    SumImage: Summation
    Image  : New image ( that has to sum)
    """
    SumMatrix = np.array(SumImage)
    ImageMatrix = np.array(Image2)
    ImageSum = SumMatrix + ImageMatrix
    return ImageSum  
 

def plot_SumImage(image):
    """  Plot the Summed Image
    Parameters :
    image : image data (N X N array)
    """	    
    plt.figure()
    plt.title("Summation of Tif Files")
    plt.imshow(image, cmap='jet',alpha=1)
    plt.show()

def write_SumImage_tif(filename, image):
    im = Image.fromarray(image)
    im.save(filename)
    print " saved"
    #img = ([])
    #img.data = image
    #img.write("summed_image.tif")
    return    

def get_directory(filename):
    print 'Please enter a path in which to place generated plots.'
    print 'Press <ENTER> to generate in the current directory.'
    path = raw_input('Path: ').strip()

    if len(path) > 0 and not os.path.exists(path):
        print 'The given path does not exist.'
        sys.exit()

    if not os.path.isabs(path):
        print 'Creating image: ' + os.path.join(os.getcwd(), path, filename)
    else:
        print 'Creating image: ' + os.path.join(path, filename)

    return os.path.join(path, filename)


def startSumImage(path):
    y = raw_input('Please enter starting image file name ')
    print " You Entered =  ", y
    
    x = int(input('Pleae enter number of images that you want to sum  '))
    print " You Entered = ",
    
    ImageSum = DataSumImage(path, y, x)
    
    filename = raw_input('Please enter a new file name for sum image (.tif) eg:- Sum_image   ')
    #print 'Press <Enter. to auto generate'
    #filename = raw_input('File: ').
    file_name = filename+".tif"
    print "New Summed Image file name (.tif)", file_name
    
    write_SumImage_tif(get_directory(file_name), ImageSum)
    return


if __name__ == '__main__':
    """   path :  Complete path to the file to be loaded into memory    """

    path = os.path.join(os.getcwd())
    startSumImage(path)
    datalist(path)
    #DataSumImage(path)
    #print "finished sum"datalist(path)
		

