import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

def jackknife(series, n):
    av_list = []
    cutsample = [samples for samples in zip(*[iter(series.tolist())]*n)]
    Nsp = len(cutsample)

    for i in range(0, Nsp): 
        resample = []
        for j in range(0, Nsp):
            if j != i: resample += cutsample[i]
        av_list.append(np.mean(resample))

    jav = np.mean(av_list)
    delta = [(jav - av) * (jav - av) for av in av_list]
    jerr = np.sqrt(np.sum(delta) / (Nsp - 1)) / np.sqrt(Nsp)
    bias = (Nsp - 1) * (jav - series.mean())
    return jav, jerr, bias