from ipywidgets import interact
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import glob

A = glob.glob(os.path.join(data_dir, "*tiff"))
Data = imread(A)

def view_image(i):
    fig, ax = plt.subplots()
    ax.imshow(Data[i], interpolation='nearest', 
                  origin='lower', norm= LogNorm(vmin=0.1, vmax=4000) )
    ax.set_title("Browse the Image Stack")
    plt.show()
    
interact(view_image, i=(0, Data.shape[0]-1))
