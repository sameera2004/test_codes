import os, sys
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

    Returns
    -------
    output: NxN ndarray
    Returns a numpy array of the same data type as the original tiff file

    """
    
    filename = os.path.basename(file)
    print('loading ' + filename)
    image = fabio.open(file)
    image_data = image.data
    print 'Volume loaded successfully'
    return image_data, filename


def plot_image(image, filename):
    plt.figure()
    plt.title(filename)
    plt.imshow(image, cmap='jet',alpha=1)
    plt.show()


def datalist(path):
    A = glob.glob(os.path.join(path, '*.tif')) 
    datalist_l=len(A)
    print datalist_l
    for file in A:
        image_data, filename = load_tif(file)
        plot_image(image_data, filename)
    return


if __name__ == '__main__':
    path=os.path.join(os.getcwd())
    datalist(path)
