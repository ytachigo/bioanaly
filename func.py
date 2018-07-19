import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

def floor(value, dignum):
    return int(value / dignum) * dignum

def ceil(value, dignum):
    return (int(value / dignum) + 1 ) * dignum

def crosscorr(vec0, vec1):
    value = np.dot(vec0, vec1) / (np.linalg.norm(vec0) * np.linalg.norm(vec1))
    return value