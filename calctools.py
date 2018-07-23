import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import re as re

Kb = 1.38064852 * 0.001 # Boltzmann constant

def frehist(series, binnum, T, calcfre=True): # Calculate a 1-dimensional free energy surface
    maxv = series.max()
    minv = series.min()
    hdelta = (maxv - minv) / binnum
    hist_list = np.array([0 for i in range(0, binnum + 1)])

    for i, v in series.iteritems():
        hindex = int((v - minv) / hdelta)
        hist_list[hindex] += 1

    logp = - Kb * T * np.log(hist_list / len(series))
    minlogp = np.min(logp)
    freene = logp - minlogp # Fee energy values

    if calcfre == False: freene = hist_list / binnum 

    sns.set_style('ticks') # Plot the free energy
    fig = plt.figure(figsize=(5, 5))
    mpl.rc('font', weight='bold')
    mpl.rcParams['axes.linewidth'] = 2.5
    filename = 'frehist.pdf'

    startlabel = int(minv) # Set the tick parameters
    lastlabel = int(maxv)
    step = int((maxv - minv) / 5)

    ax = fig.add_subplot(1,1,1)
    ax.plot(freene, color='Red', linewidth=3)
    ax.set_xticks(np.arange(0, binnum + 1, int(binnum / 5)))
    ax.set_xticklabels(np.arange(startlabel, lastlabel + 1, step), fontsize=15)
    ax.tick_params(labelsize=15)
    plt.savefig(filename, dpi=350)
    plt.show()
    return freene

def frehist2d(series0, series1, binnum0, binnum1, T, calcfre=True):
    maxv0 = series0.max()
    maxv1 = series1.max()
    minv0 = series0.min()
    minv1 = series1.min()
    hdelta0 = (maxv0 - minv0) / binnum0
    hdelta1 = (maxv1 - minv1) / binnum1
    df = pd.DataFrame({'series0': series0.values.tolist(), 'series1': series1.values.tolist()})
    hist2d_list = np.array([[0 for col in range(0, binnum1 + 1)] for row in range(0, binnum0 + 1)])

    for i, v in df.iterrows():
        hindex0 = int((v['series0'] - minv0) / hdelta0)
        hindex1 = int((v['series1'] - minv1) / hdelta1)
        hist2d_list[hindex0][hindex1] += 1

    maxhist2d = np.max([np.max(hist2d_list[i]) for i in range(0, binnum0)])
    freene2d = - Kb * T * np.ma.log(hist2d_list / maxhist2d) # Fee energy values
    
    if calcfre == False:
        maxhist2d = np.max([np.max(hist2d_list[i]) for i in range(0, binnum0)])
        freene2d = hist2d_list / len(series0)

    sns.set_style('ticks') # Plot the free energy
    fig = plt.figure(figsize=(6, 5))
    mpl.rc('font', weight='bold')
    mpl.rcParams['axes.linewidth'] = 2.5
    filename = 'fre2dhist.pdf'
    cm = make_cmap(['maroon', 'red', 'yellow', 'greenyellow', 'cyan', 'blue', 'navy'])

    startlabel0 = int(minv0) # Set the tick parameters
    startlabel1 = int(minv1)
    lastlabel0 = int(maxv0)
    lastlabel1 = int(maxv1)
    step0 = int((maxv0 - minv0) / 5)
    step1 = int((maxv1 - minv1) / 5)
    if step0 == 0: step0 = 1
    if step1 == 0: step1 = 1
    fremax = int(np.max([np.max(freene2d[i]) for i in range(0, binnum0)]))

    ax = fig.add_subplot(1,1,1)
    pccol = plt.pcolor(freene2d, cmap=cm, vmin=0, vmax=fremax)
    pcbar = plt.colorbar() # Colorbar
    pcbar.set_ticks(range(0, fremax))
    pcbar.ax.tick_params(labelsize=17, width=4)
    pcbar.set_label('(kJ /mol)', fontsize=16, fontweight='bold')
    if calcfre == False: pcbar.set_label('Probability', fontsize=16, fontweight='bold') 
    ax.set_xticks(np.arange(0, binnum1 + 1, int(binnum1 / 5)))
    ax.set_yticks(np.arange(0, binnum0 + 1, int(binnum0 / 5)))
    ax.set_xticklabels(np.arange(startlabel1, lastlabel1 + 1, step1), fontsize=15)
    ax.set_yticklabels(np.arange(startlabel0, lastlabel0 + 1, step0), fontsize=15)
    ax.tick_params(labelsize=15)
    plt.savefig(filename, dpi=350)
    plt.show()
    return freene2d

def make_cmap(colors): # Make a color map
    color_list = []
    colvalues = range(0, len(colors))
    cvmax = np.ceil(np.max(colvalues))

    for cv, c in zip(colvalues, colors):
        color_list.append((cv / cvmax, c))
    return LinearSegmentedColormap.from_list('custom_cmap', color_list)