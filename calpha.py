import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import re as re

def get_calpha(nres, startframe, lastframe, cutoff=8, distance=False): # Get alpha carbon distance
    df_list = []
    for i in range(1, nres + 1):
        filename = 'calpha%d.dat' % i
        name_list = ['frame']
    
        for j in range(1, nres + 1):
            if i <= j:
                dist = 'dist_%d' % j
                name_list.append(dist)
    
        df_dist = pd.read_table(filename, delim_whitespace=True,  skiprows=1, names=name_list)
        df_dist = df_dist.drop('frame', axis=1).astype(float)
        df_dist = df_dist[startframe:lastframe]

        if distance == False:
            for k in range(0, i):
                df_dist.iloc[k,:][df_dist.iloc[k,:] <= cutoff] = 1
                df_dist.iloc[k,:][df_dist.iloc[k,:] > cutoff] = 0

        df_list.append(df_dist)
    return df_list

def get_matrix(df_list, nres): # Make a matrix from alpha carbon data sets
    matrix = [[0 for col in range(0, nres)] for row in range(0, nres)]
    for row in range(0, nres):
        for col in range(0, nres):
            if col >= row:
                df = df_list[row]
                matrix[row][col] = df.iloc[:,col-row].mean()
                matrix[col][row] = df.iloc[:,col-row].mean()
    return np.array(matrix)
