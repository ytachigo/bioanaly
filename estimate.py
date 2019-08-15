import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

def jackknife(series, nsp):
    cutsample = [samples for samples in zip(*[iter(series.tolist())] * nsp)]
    nb = len(cutsample)
    av_sample = np.mean(series)
    psdv_list = []

    for i in range(0, nb):
        resample = []
        for j in range(0, nb):
            if j != i: resample += cutsample[i]
        psdv = (nb * av_sample) - ((nb - 1) * np.mean(resample))
        psdv_list.append(psdv)

    jav = np.mean(psdv_list)
    jvar = np.var(psdv_list, ddof=1)
    jerr = np.sqrt(jvar / nb)
    return jav, jerr
