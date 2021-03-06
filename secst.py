import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import re as re
from itertools import groupby

def get_secdf(filename, nres): # Get a dataframe of DSSP results
    res_list = []
    countrow = 0

    for line in open(filename):
        countrow += 1
        if line[0:10] == 'set ytics(':
            resfound_list = re.findall('\d{2,3}"', line)
            for i in range(0, len(resfound_list)):
                resnum = re.match('\d{2,3}', resfound_list[i])
                resnum = int(resnum.group())
                res_list.append(resnum)

        if line[0:19].strip() == '1.000    1.000':
            row = countrow - 1
    df_sec = pd.read_table(filename,
                           delim_whitespace=True,
                           skiprows=row,
                           names=['time', 'resnum', 'secnum'])
    df_sec = df_sec[df_sec['time'] != 'end']
    df_sec = df_sec[df_sec['time'] != 'pause']
    df_sec = df_sec[df_sec['resnum'] != nres + 1].astype(float)
    return df_sec

def secprob(df, secnum, nres, mdnum, startframe, lastframe): # Calculate a probability distributions of secondary structure
    sec_list = np.array([0 for i in range(0, nres)])
    sectime_list = [[] for i in range(0, nres)]
    df = df[df['time'] >= startframe] # time must be larger than 1
    df = df[df['time'] < lastframe]

    for rn, sn in zip(df['resnum'], df['secnum']):
        if sn == secnum:
            sec_list[int(rn) - 1] += 1
            sectime_list[int(rn) - 1].append(1)
        if sn != secnum:
            sectime_list[int(rn) - 1].append(0)
    return sec_list / ((lastframe - startframe) * mdnum), sectime_list

def secprob_time(sectime_list, binnum):
    cutsample = [samples for samples in zip(*[iter(np.array(sectime_list).T)] * binnum)]
    nsp = len(cutsample)
    secprt_list = []

    for i in range(0,nsp):
        secprt_list.append(np.mean(cutsample[i]))
    return secprt_list

def  get_cddf(df, nres, ncd, lastframe): # Calculate a helix content
    elcomph = 42500 * (1 - (3 / nres))
    elcoil = 640
    totfg_list = [[0 for i in range(0, nres)] for i in range(0, lastframe)]
    helixc_list = []

    for i, v in df.iterrows():
        if v['time'] < lastframe:
            if v['secnum'] == 4:
                totfg_list[int(v['time'])][int(v['resnum'] - 1)] += 1

    for i, totfg in enumerate(totfg_list):
        elcalc = 0
        for j, fg in groupby(totfg):
            if j == 1:
                nh = sum(1 for f in fg)
                elcalc += (nh - ncd) * (elcomph / nres)

        if elcalc > 0:
            helixc = (elcalc - elcoil) / (elcomph - elcoil)
        else: helixc = 0

        helixc_list.append(helixc * 100)
        df_cd = pd.DataFrame({'cd': helixc_list})
    return df_cd
