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

def convert_3dtomatrix(series0, series1, seriesv, 
                       binnum0, binnum1, minmax_list=0):
# Convert 3D data sets to a matrix which is used for plotting a heatmap

    if minmax_list == 0:
        maxv0 = series0.max()
        maxv1 = series1.max()
        minv0 = series0.min()
        minv1 = series1.min()
        hdelta0 = (maxv0 - minv0) / binnum0
        hdelta1 = (maxv1 - minv1) / binnum1

    else:
        maxv0 = minmax_list[0]
        maxv1 = minmax_list[1]
        minv0 = minmax_list[2]
        minv1 = minmax_list[3]
        hdelta0 = (maxv0 - minv0) / binnum0
        hdelta1 = (maxv1 - minv1) / binnum1

    df = pd.DataFrame({'series0': series0.values.tolist(), 
                                  'series1': series1.values.tolist(),
                                  'seriesv': seriesv.values.tolist()})
    hist2d_list = [[0 for col in range(0, binnum1 + 1)] \
                            for row in range(0, binnum0 + 1)]

    for i, v in df.iterrows():
        hindex0 = int((v['series0'] - minv0) / hdelta0)
        hindex1 = int((v['series1'] - minv1) / hdelta1)
        hist2d_list[hindex0][hindex1] += v['seriesv']
        print(hindex0, hindex1, v['seriesv'], hist2d_list[hindex0][hindex1])
    return np.array(hist2d_list)

def crosscorr(vec0, vec1, tau):
    if tau == 0:
        value = np.dot(vec0, vec1) / \
                (np.linalg.norm(vec0) * np.linalg.norm(vec1))
    if tau > 0:
        value = np.dot(vec0[tau:], vec1[:-tau]) / \
            (np.linalg.norm(vec0[tau:]) * np.linalg.norm(vec1[:-tau]))
    return value
