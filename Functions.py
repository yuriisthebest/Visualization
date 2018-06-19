import numpy as np
import pandas as pd
from PIL import Image  # uses pillow
import matplotlib.pyplot as plt
import sys, os
from collections import namedtuple

"For the Jaccard_withPackages"
from sklearn.metrics import jaccard_similarity_score

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 500)


"""
Code snippet to import the dataset

:Author: Yuri Maas
"""
def Jaccard_withPackages(path1, path2):
    """
    Finds the amount of elements of the intersection of path1 and path2
    (path1[i] == path2[i]) and devides it by the total unmber of elements

    :author: Yuri Maas
    :param path1: The integer set of values to be compared with path2
    :param path2: The integer set of values to be compared with path1
    """
    return jaccard_similarity_score(path1, path2)


def Jaccard(path1, path2):
    """
    Finds the amount of elements of the intersection of path1 and path2
    (path1[i] == path2[i]) and devides it by the total unmber of elements

    :author: Yuri Maas
    :param path1: The integer set of values to be compared with path2
    :param path2: The integer set of values to be compared with path1
    """
    intersection = 0
    shortlenth = [len(path1) if len(path1) <= len(path2) else len(path2)]
    for i in range(shortlenth[0]):
        if path1[i] == path2[i]:
            intersection += 1
    return intersection / shortlenth[0]


def compareScanpathNumbers_Jaccard_fast(path1, path2, margin):
    """
    Finds the amount of elements of the intersection of path1 and path2
    (path1[i] == path2[i]) and devides it by the total unmber of elements

    :author: Yuri Maas
    :param path1: The integer set of values to be compared with path2
    :param path2: The integer set of values to be compared with path1
    """
    similarity = 0
    shortlenth = [len(path1) if len(path1) <= len(path2) else len(path2)]
    for i in range(shortlenth[0]):
        if abs(path1[i] - path2[i]) < margin:
            similarity += 1
    return similarity / shortlenth[0]


def compareScanpaths_Jaccard_fast(path1, path2):
    if path1[0][2] != path2[0][2]:
        raise ValueError("Scanpaths are not for the same puzzle")

    similarity = 0
    shortlenth = [len(path1) if len(path1) <= len(path2) else len(path2)]
    currentRes = resolutions.get_values()[int(path1[0][2][:2]) - 1]
    marginX = currentRes[1] * 0.02  # Percentage margin X-axis
    marginY = currentRes[2] * 0.02  # Percentage margin Y-axis 1% ~= 12

    # Getting the coordinates and using Jaccard on them
    X1, Y1 = get_scanpath_coordinates(path1)
    X2, Y2 = get_scanpath_coordinates(path2)
    similarity += compareScanpathNumbers_Jaccard_fast(X1, X2, marginX)
    similarity += compareScanpathNumbers_Jaccard_fast(Y1, Y2, marginY)
    return similarity / 2


def get_scanpaths(data):
    """
    Loops over de data and returns the scanpaths from it

    :author: Yuri Maas
    :param data: The data from which to get the scanpaths from
    :note: The data has to be preprocessed by removeFixationsOutsideMap
    """
    # Loop over the dataset to find scanpaths
    current_scanpath = []
    final_scanpaths = []
    for i in range(len(data)):
        current_scanpath.append(data.get_values()[i])

        # If the next fixation point belongs to another puzzle,
        #  the current scanpath is over and a new one should be started
        # Assumption: The same puzzle is never twice in a row in the data
        try:
            if data.get_values()[i][2] != data.get_values()[i + 1][2]:
                final_scanpaths.append(current_scanpath)
                current_scanpath = []

        # If an IndexError occurs, the last element tried to read the next,
        #  so the final scanpath is over
        except IndexError:
            final_scanpaths.append(current_scanpath)
            return final_scanpaths


def get_scanpath_coordinates(path):
    """
    Returns the X and Y values in seperate arrays

    :author: Yuri Maas
    :param path: The scanpath to get the X and Y values from
    """
    X = [path[i][5] for i in range(len(path))]
    Y = [path[i][6] for i in range(len(path))]
    return X, Y



def calculate_overlap(path1, path2):
    """
       calculates the overlap between 2 bouding boxes

       :author: Maaike van delft
       :param path1: a scanpath to compare
              path2: a scanpath to compare
       """

    Rect = namedtuple ('Rectangle', 'xmin ymin xmax ymax')

    X, Y = get_scanpath_coordinates(path1)
    xmin_1 = min(X)
    xmax_1 = max(X)
    ymin_1 = min(Y)
    ymax_1 = max(Y)
    R1 = Rect(xmin_1, ymin_1, xmax_1, ymax_1)

    get_scanpath_coordinates(path2)
    xmin_2 = min(X)
    xmax_2 = max(X)
    ymin_2 = min(Y)
    ymax_2 = max(Y)
    R2 = Rect(xmin_2, ymin_2, xmax_2, ymax_2)

    dx = min(R1.xmax, R2.xmax) - max(R1.xmin, R2.xmin)
    dy = min(R1.ymax, R2.ymax) - max(R1.ymin, R2.ymin)
    if (dx >= 0) and (dy >= 0):
        area = dx * dy
        area_1 = (R1.xmax - R1.xmin) * (R1.ymax - R1.ymin)
        area_2 = (R2.xmax - R2.xmin) * (R2.ymax - R2.ymin)
        total_area = area_1 + area_2
        return area / total_area

def get_visual_attention_map(stimuli, data):
    """
    gets the image of a certain stimuli
    :author Maaike van Delft
    :param the stimuli where we want the image from

    """
    script_dir = sys.path[0]
    image_path = os.path.join(script_dir, 'MetroMapsEyeTracking/stimuli/' + stimuli )
    img = Image.open(image_path)
    plt.imshow(img)

    df = np.array(data.loc[data['StimuliName'] == stimuli])
    dfx = df[:,4]
    dfy = df[:,5]
    x = np.array(dfx, dtype = float)
    y = np.array(dfy, dtype=float)

    implot = plt.imshow(img)
    heatmap_z, xedges, yedges = np.histogram2d(x,y,bins = 30)
    extent_2 = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.plot()
    plt.imshow(heatmap_z.T, extent = extent_2, origin = 'lower', camp = 'inferno', alpha= 0.5)
    plt.colorbar()
    return plt.show()

#get_visual_attention_map('01_Antwerpen_S1.jpeg', data)
