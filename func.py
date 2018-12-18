import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sn

def floor(value, dignum):
    return int(value / dignum) * dignum

def ceil(value, dignum):
    return (int(value / dignum) + 1 ) * dignum

def reload(module):
    import importlib
    importlib.reload(module)

def concat_ordered(frames):
    ord_col = []
    for frame in frames:
        ord_col.extend(i for i in frame.columns if i not in ord_col)
    df_ord= pd.concat(frames)    
    return df_ord[ord_col]

def crosscorr(vec0, vec1, tau):
    if tau == 0:
        value = np.dot(vec0, vec1) / \
                (np.linalg.norm(vec0) * np.linalg.norm(vec1))
    if tau >= 0:
        value = np.dot(vec0[:tau], vec1[:-tau]) / \
            (np.linalg.norm(vec0[:tau]) * np.linalg.norm(vec1[:-tau]))
    return value