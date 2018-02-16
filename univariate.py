from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from common import bestbins,check_support

def uni_graph(data, brkset, plot_type, other_labels):

    #Supported plot types#
    uni_types = ['hist','box','violin']

    check_support(plot_type, uni_types, 'univariate')

    #Rejoin data previously separated by breakdown#
    join_dat = []
    for item in data:

        join_dat.extend(item)

    #Full range of data#
    dat_range = np.ptp(join_dat)

    nbrk = len(brkset)

    #Estimate best num of bins#
    pltbin = bestbins(join_dat)

    if pltbin < 1:
        print("Dataset with breakdown is empty, skipping!")

    #Histogram range#
    #histo_range = [min(join_dat), min(join_dat) + dat_range]
    
    if plot_type == 'hist':

        if brkset:
            #stack_hist(data, brkset, pltbin)
            plt.hist(data, pltbin, histtype='bar', stacked=True, fill=True, label=brkset)
        else:
            plt.hist(data, pltbin, histtype='bar', fill=True)

    if plot_type == 'box':

        if brkset:
            plt.boxplot(data, labels=brkset)
        else:
            plt.boxplot(data, labels=other_labels)

    if plot_type == 'violin':

        if brkset:
            plt.violinplot(data, brkset, showmedians=True, showextrema=True, showmeans=True)
        else:
            plt.violinplot(data, other_labels, showmedians=True, showextrema=True, showmeans=True)

def stack_hist(data, brkset, pltbin):

    sum_events = np.zeros(pltbin)
        
    allhisto = []

    #stacked histograms#
    for tt in xrange(nbrk):

        events, val = np.histogram(data[tt], pltbin, range=histo_range)

        histo = plt.bar(val[:pltbin], events, dat_range / pltbin, color = cm.jet(1. * tt / nbrk), bottom = sum_events, edgecolor = 'none', label=brkset[tt])

        allhisto.append(histo)
            
        sum_events = sum_events + events

    #fig.legend(allhisto, brkset, loc='best', fancybox=True, framealpha=0.5)
