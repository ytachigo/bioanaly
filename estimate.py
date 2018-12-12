import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

def jackknife(series, n):
    cutsample = [samples for samples in zip(*[iter(series.tolist())]*n)]
    nsp = len(cutsample)
    av_list = []

    for i in range(0, nsp): 
        resample = []
        for j in range(0, nsp):
            if j != i: resample += cutsample[i]
        av_list.append(np.mean(resample))

    jav = np.mean(av_list)
    delta = [(jav - av) * (jav - av) for av in av_list]
    jerr = np.sqrt(np.sum(delta) / (nsp - 1)) / np.sqrt(nsp)
    return jav, jerr
