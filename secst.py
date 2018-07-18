import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import re as re

def get_secstdf(filename, Nres): # Get a dataframe of DSSP results
    res_list = []
    countrow = 0

    for line in open(filename):
        countrow += 1
        if line[0:10] == 'set ytics(':
            resfound_list = re.findall('\d{2,3}"', line)
            for i in range(0, len(resfound_list)):
                resnum = re.match('\d{2,3}', resfound_list[i])
                resnum = int(resnum.group())

        if line[0:18].strip() == '1.000    1.000':
            row = countrow - 1
    df_sec = pd.read_table(filename, delim_whitespace=True, skiprows=row, names=['time', 'resnum', 'secnum'])
    df_sec = df_sec[df_sec['time'] != 'end']
    df_sec = df_sec[df_sec['time'] != 'pause']
    df_sec = df_sec[df_sec['resnum'] != Nres + 1].astype(float)
    return df_sec

def secst_prob(df, secnum, Nres, startframe, lastframe): # Calculate a probability distributions of secondary structure
    sec_list = np.array([0 for i in range(0, Nres)])
    for i, v in df.iterrows():
        if v['secnum'] == secnum and v['time'] >= startframe:
            sec_list[int(v['resnum']) - 1] += 1
    return sec_list / ((lastframe - startframe) * 9)