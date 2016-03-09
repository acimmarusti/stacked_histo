"""stacked_histo.py

Stacked histogram function
Written as a workaround for:
Matplotlib bug #3883 - hist does NOT take only one data point
Should be fixed in Matplotlib >= 1.5.0

By Andres Cimmarusti

"""
from __future__ import division
import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from matplotlib import cm

def gauss_func(x, a, x0, sigma):

    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

def loren_func(x, a, x0, sigma):

    return a / ((x - x0)**2 + sigma**2)

def display(data, keywords, breakdown, supertitle, reso, lim=[], **kwparam):

    yscale_type = ''
    
    #Handle yscale changes#
    if 'yscale' in kwparam:

        yscale_type = kwparam['yscale']
    
    #Handle multiple data sets#
    keys = []
    
    if isinstance(keywords, basestring):

        keys.append(keywords)

    else:

        keys.extend(keywords)

    #Handle multiple breakdowns#
    brkdown = []
        
    if isinstance(breakdown, basestring):

        brkdown.append(breakdown)

    else:

        brkdown.extend(breakdown)

    #Subplot array#
    numplts = len(keys) * len(brkdown)

    a = np.ceil(numplts**0.5).astype(int)
    b = np.floor(1.*numplts/a).astype(int)

    fig = plt.figure()


    #Possible combinations#
    idx = 1
    
    possibilities = itertools.product(keys, brkdown)

    for keyword, breakby in possibilities:
    
        #Break down#
        brkset = list(set(data[breakby]))
        brkset.sort()
        nbrk = len(brkset)

        dat_brk = []

        for ite in brkset:

            data_ite = data[data[breakby] == ite]

            dat_ite = np.asarray(data_ite[keyword].copy())
                    
            dat_brk.append(dat_ite)


        ####Plotting####

        #Estimate plot range if not provided by user#
        if not lim:
        
            lim = [min(data[keyword]), max(data[keyword])]

        pltbin = np.floor((lim[-1] - lim[0]) / reso).astype(int)

        histo_range = lim

        sum_events = np.zeros(pltbin)

        #subplot breakdown#
        fig.add_subplot(a, b, idx)

        idx += 1
        
        allhisto = []

        #stacked histograms#
        for tt in xrange(nbrk):

            events, val = np.histogram(dat_brk[tt], pltbin, range=histo_range)

            histo = plt.bar(val[:pltbin], events, reso, color = cm.jet(1. * tt / nbrk), bottom = sum_events, edgecolor = 'none', label=brkset[tt])

            allhisto.append(histo)
            
            sum_events = sum_events + events

        plt.xlabel(keyword)
        plt.ylabel('Events')
        plt.legend(loc='best', fancybox=True, framealpha=0.5, title=breakby)
        if 'log' in yscale_type:
            plt.yscale('symlog')
        
    #fig.legend(allhisto, brkset, loc='best', fancybox=True, framealpha=0.5)
    fig.suptitle(supertitle)
    fig.set_tight_layout(True)

    return fig
