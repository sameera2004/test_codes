import glob
import os


def check_words_filenames(A):
    """
    This function will remove raw, metadata, dark tif files from
    the list of tif files, if there are these files in the original
    list
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
