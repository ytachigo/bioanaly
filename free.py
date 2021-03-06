import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import re as re

Kb = 1.38064852 * 6.022140857 * 0.001 # Boltzmann constant

def convergence(series, n):
    cutsamples = [samples for samples in zip(*[iter(series.tolist())] * n)]
    conv_list = [np.mean(sample) for sample in cutsamples]
    return conv_list

def frehist(series, binnum, temp, calcfre=True, rdf=False):
# Calculate a 1-dimensional free energy surface

    maxv = series.max()
    minv = series.min()
    hdelta = (maxv - minv) / binnum
    hist_list = np.array([0 for i in range(0, binnum + 1)])

    for i, v in series.iteritems():
        hindex = int((v - minv) / hdelta)
        hist_list[hindex] += 1

    prob = hist_list / len(series)

    if rdf == True:
        for i in range(0, len(prob)):
            radius = (minv + (i * hdelta))
            surfarea = 4 * np.pi * radius * radius
            prob[i] = prob[i] / surfarea

    if calcfre == True:
        freene = - Kb * temp * np.log(prob)
        minfreene = np.min(freene)
        freene1d = freene - minfreene # Fee energy landscape
    else: freene1d = prob

    sns.set_style('ticks') # Plot the free energy
    fig = plt.figure(figsize=(5, 5))
    mpl.rc('font', weight='bold')
    mpl.rcParams['axes.linewidth'] = 2.5
    filename = 'frehist.pdf'

    ax = fig.add_subplot(1,1,1)
    ax.plot(freene1d, color='Red', linewidth=3)
    ax.set_xticks(np.arange(0, binnum + 1, binnum / 5))
    ax.set_xticklabels(minv + np.arange(0, binnum + 1, binnum / 5) * hdelta,
                       fontsize=15)
    ax.tick_params(labelsize=15)
    plt.savefig(filename, dpi=350)
    plt.show()
    return freene

def frehist2d(series0, series1, binnum0, binnum1, temp,
              calcfre=True, rdf=False):
    maxv0 = series0.max()
    maxv1 = series1.max()
    minv0 = series0.min()
    minv1 = series1.min()
    hdelta0 = (maxv0 - minv0) / binnum0
    hdelta1 = (maxv1 - minv1) / binnum1
    df = pd.DataFrame({'series0': series0.values.tolist(),
                       'series1': series1.values.tolist()})
    hist2d_list = np.array([[0 for col in range(0, binnum1 + 1)] \
                           for row in range(0, binnum0 + 1)])

    for i, v in df.iterrows():
        hindex0 = int((v['series0'] - minv0) / hdelta0)
        hindex1 = int((v['series1'] - minv1) / hdelta1)
        hist2d_list[hindex0][hindex1] += 1

    prob = hist2d_list / len(series0)

    if rdf == True:
        for i in range(0, len(prob)):
            radius = (minv0 + (i * hdelta0))
            surfarea = 4 * np.pi * radius * radius
            prob[i] = prob[i] / surfarea

    prob_nonzero = [[j for j in prob[i] if j != 0] for i in range(0, len(prob))]
    prob_nonzero = [prob_nonzero[i] for i in range(0, len(prob)) if len(prob_nonzero[i]) != 0]
    
    maxprob = np.max([np.max(prob[i]) for i in range(0, binnum0)])
    minprob = np.min([np.min(prob_nonzero[i]) for i in range(0, len(prob_nonzero))])

    if calcfre == True:
        freene = - Kb * temp * np.ma.log(prob)
        minfreene = - Kb * temp * np.log(maxprob)
        freene2d = freene - minfreene # Fee energy landscape
    else: freene2d = prob

    sns.set_style('ticks') # Plot the free energy
    fig = plt.figure(figsize=(6, 5))
    mpl.rc('font', weight='bold')
    mpl.rcParams['axes.linewidth'] = 2.5
    filename = 'fre2dhist.pdf'
    cm = make_cmap(['maroon', 'red', 'yellow', 'greenyellow', \
                    'cyan', 'blue', 'navy'])

    fremax = - Kb * temp * np.log(minprob / maxprob)

    ax = fig.add_subplot(1,1,1)
    pccol = plt.pcolor(freene2d, cmap=cm, vmin=0, vmax=fremax)
    pcbar = plt.colorbar() # Colorbar
    pcbar.set_ticks(np.arange(0, fremax, fremax / 5))
    pcbar.ax.tick_params(labelsize=17, width=4)
    pcbar.set_label('(kJ/mol)', fontsize=16, fontweight='bold')
    if calcfre == False: pcbar.set_label('Probability', \
                                         fontsize=16, fontweight='bold')
    ax.set_xticks(np.arange(0, binnum1 + 1, binnum1 / 5))
    ax.set_yticks(np.arange(0, binnum0 + 1, binnum0 / 5))
    ax.set_xticklabels(minv1 + np.arange(0, binnum1 + 1, binnum1 / 5) * hdelta1, 
                       fontsize=15)
    ax.set_yticklabels(minv0 + np.arange(0, binnum0 + 1, binnum0 / 5) * hdelta0, \
                       fontsize=15)
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
