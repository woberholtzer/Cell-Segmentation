import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import skimage.io
from skimage.transform import resize
from skimage.color import rgb2gray
from unionfindeff import *
import time


def load_cells_grayscale(filename, n_pixels=0):
    """
    Load in a grayscale image of the cells, where 1 is maximum brightness
    and 0 is minimum brightness

    Parameters
    ----------
    filename: string
        Path to image holding the cells
    n_pixels: int
        Number of pixels in the image
    
    Returns
    -------
    ndarray(N, N)
        A square grayscale image
    """
    cells_original = skimage.io.imread(filename)
    cells_gray = rgb2gray(cells_original)
    # Denoise a bit with a uniform filter
    cells_gray = ndimage.uniform_filter(cells_gray, size=10)
    cells_gray = cells_gray - np.min(cells_gray)
    cells_gray = cells_gray / np.max(cells_gray)
    N = int(np.sqrt(n_pixels))
    if n_pixels > 0:
        # Resize to a square image
        cells_gray = resize(cells_gray, (N, N), anti_aliasing=True)
    return cells_gray


def permute_labels(labels):
    """
    Shuffle around labels by raising them to a prime and
    modding by a large-ish prime, so that cells are easier
    to see against their backround
    Parameters
    ----------
    labels: ndarray(M, N)
        An array of labels for the pixels in the image
    Returns
    -------
    labels_shuffled: ndarray(M, N)
        A new image where the labels are different but still
        the same within connected components
    """
    return (labels ** 31) % 833


## TODO: Fill in your code here

def get_cell_labels(image_name, thresh):
    matches = UnionFindOpt(len(image_name) ** 2)
    labels_array = np.zeros((len(image_name), len(image_name)))
    # loop through array that holds pixels to see if neighboring pixels are above the threshold
    for i in range(len(image_name)-1):
        for j in range(len(image_name)-1):
            # union two pixels that are side by side if passes condition
            if image_name[i][j] > thresh and image_name[i + 1][j] > thresh:
                matches.union(i*len(image_name)+j, (i+1)*len(image_name)+j)
            # union two pixels that are stacked on top of each other if passes condition
            if image_name[i][j] > thresh and image_name[i][j + 1] > thresh:
                matches.union(i * len(image_name) + j, i * len(image_name) + (j+1))

    for i in range(len(image_name)):
        for j in range(len(image_name)):
            # fill the array with the root of each pixel so cells can be found in clumps
            labels_array[i][j] = matches.root((j + (len(image_name)) * i))
    return labels_array


def get_cluster_centers(cell_labels):
    # create empty list of lists for indices of pixels with same root
    list_labels = [[] for _ in range((len(cell_labels))**2)]
    for i in range(len(cell_labels)):
        for j in range(len(cell_labels)):
            # add each pixel's location to the index of it's root
            list_labels[int(cell_labels[i][j])].append([i, j])
    list_matches = []
    for i in range(len(list_labels)):
        # looking at only pairs...
        if len(list_labels[i]) > 1:
            total_x = 0
            total_y = 0
            counter = 0
            for j in range(len(list_labels[i])):
                # add up all first indices of a cell
                total_x += list_labels[i][j][0]
                # add up all second indices of a cell
                total_y += list_labels[i][j][1]
                # add to the counter to allow for average pixel location (center of cell)
                counter += 1
            # find the average using the total of the indices and the counter
            x = total_x//counter
            y = total_y//counter
            # add the center to the list
            list_matches.append((x, y))
    return list_matches


if __name__ == '__main__':
    thresh = 0.7
    I = load_cells_grayscale("Cells.jpg")
    labels = get_cell_labels(I, thresh)
    cells_original = skimage.io.imread("Cells.jpg")
    X = get_cluster_centers(labels)
    X = np.array(X)
    plt.imshow(cells_original)
    plt.scatter(X[:, 1], X[:, 0], c='C2')
    plt.show()
