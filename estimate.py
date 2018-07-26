import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

def jackknife(series, n):
    av_list = []
    for samples in zip(*[iter(series.tolist())]*n):
        av_list.append(np.mean(samples))
    jav = np.mean(av_list)
    delta = [(jav - av) * (jav - av) for av in av_list]
    jerr = np.sqrt(np.sum(delta) / (n - 1)) / np.sqrt(n)
    return jav, jerr