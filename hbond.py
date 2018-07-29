import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import re as re
from itertools import groupby

def get_hbdf(filename): # Get a dataframe of hydrogen bond analysis
    respair_list = []
    countrow = 0

    for line in open(filename):
        countrow += 1
        if line[0:10] == 'set ytics(':
            resfound_list = re.findall('\d{2,3}@', line)
            for i in range(0, len(resfound_list), 2):
                pair0 = re.match('\d{2,3}', resfound_list[i])
                pair0 = int(pair0.group())
                pair1 = re.match('\d{2,3}', resfound_list[i + 1])
                pair1 = int(pair1.group())
                respair = [pair0, pair1]
                respair_list.append(respair)

        if line[0:20].strip() == '1.000    1.000' or line[0:20].strip() == '1.000     1.000':
            row = countrow - 1
    df_hb = pd.read_table(filename, 
                           delim_whitespace=True, 
                           skiprows=row, 
                           names=['time', 'respair', 'hbond'])
    df_hb = df_hb[df_hb['time'] != 'end']
    df_hb = df_hb[df_hb['time'] != 'pause']
    df_hb = df_hb[df_hb['respair'] != len(respair_list)].astype(float)
    return df_hb, respair_list

def hbnum(df, respr_list, Nmax, mdnum, startframe, lastframe, group0=[], group1=[]):
    # Calculate the number of hydrogen bonds per one frame
    hbnum_list = np.array([0 for i in range(0, Nmax)])
    df = df[df['time'] >= startframe]
    df = df[df['time'] <= lastframe]
    calc_list = []

    if len(group0) > 0 and len(group1) > 0:
        for i, pr in enumerate(respr_list):
            intersec0 = set(pr) & set(group0)
            intersec1 = set(pr) & set(group1)

            if len(intersec0) == len(intersec1) == 1:
                calc_list.append(i + 1)
    df = df[df['respair'].isin(calc_list)]

    for pr, hb in zip(df['respair'], df['hbond']):
        hbnum_list[respr_list[int(pr) - 1][0] - 1] += hb
        hbnum_list[respr_list[int(pr) - 1][1] - 1] += hb

    return hbnum_list / ((lastframe - startframe) * mdnum)