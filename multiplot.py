"""multiplot.py

Pandas visualization, seaborn and others are great, but they expect data in a certain format. Sometimes shaping the data into that format brings its own complications (e.g. increasing number of rows while keeping certain columns constant)
This is my attempt to automate plotting relying directly on matplotlib and data contained in a pandas data frame.

By Andres Cimmarusti

"""
from __future__ import division, print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from itertools import combinations,product

from univariate import uni_graph
from bivariate import bi_graph

def put_in_list(unk_input):

    out_list = []
    
    if isinstance(unk_input, basestring):
        out_list.append(unk_input)
    else:
        out_list.extend(unk_input)
    
    return out_list

def graph(supertitle, data, keywords, breakdown=[()], analysis='univariate', plot_type='relational', **kwparam):
    
    #Handle scale changes#
    xscale_type = ''
    yscale_type = ''
    
    if 'xscale' in kwparam:
        xscale_type = kwparam['xscale']

    if 'yscale' in kwparam:
        yscale_type = kwparam['yscale']

    #User-defined number of plots#
    if 'num_plots' in kwparam:
        nplots = kwparam['num_plots']
    
    #Handle multiple data sets#
    keys = put_in_list(keywords)

    #Handle multiple breakdowns#
    brkdown = put_in_list(breakdown)

    if len(brkdown) < 1:
        hue = 1
    else:
        hue = len(brkdown)

    #Univariate of Bivariate analysis#
    if analysis == 'bivariate' and len(keys) > 1:
        diff_plots = list(combinations(keys, 2))
    elif analysis == 'univariate' or len(keys) < 2:
        diff_plots = keys

    if len(keys) < 2:
        analysis = 'univariate'

    #Subplot array#
    num_diff_plots = len(diff_plots)
    numplts = num_diff_plots * hue

    a = np.ceil(numplts**0.5).astype(int)
    b = np.floor(1.*numplts/a).astype(int)

    fig = plt.figure()


    #Possible combinations#
    idx = 1

    possible = list(product(diff_plots, brkdown))

    if not possible:

        print("Possible combinations list is empty. If plotting without breakdown make sure breakdown=[()]\n")
        exit(0)

    for cols, breakby in possible:
        
        #Packing and unpacking variables#
        toplot = put_in_list(cols)

        tick_rot = 0
        
        if len(toplot) == 2 and analysis == 'bivariate':
            xlabel, ylabel = toplot
        elif len(toplot) == 1 and analysis == 'univariate':
            if plot_type == 'box' or plot_type == 'violin':
                ylabel, = toplot
                xlabel = ''
                tick_rot = 30
            elif plot_type == 'hist':
                xlabel, = toplot
                ylabel = 'Events'
        else:
            xlabel = ''
            ylabel = ''

        #Break down#
        if breakby:
            brkset = list(set(data[breakby]))
            brkset.sort()
            nbrk = len(brkset)

            dat_brk = []

            for ite in brkset:

                data_ite = data[data[breakby] == ite]

                dat_ite = np.asarray(data_ite[toplot].copy())

                #if ite == 'FDH402':
                    #print(data_ite[toplot].head())
                    #print(dat_ite[:10])
                
                dat_brk.append(dat_ite)

            plot_data = dat_brk

        else:

            brkset = []
            plot_data = np.asarray(data[toplot].copy())

        if len(plot_data) == 0:
            print("Dataset for " + layer + "with breakdown is empty, skipping!")
            continue
        
        ####Plotting####

        #subplot breakdown#
        fig.add_subplot(a, b, idx)
        idx += 1

        if analysis == 'univariate':
            uni_graph(plot_data, brkset, plot_type, toplot)
        elif analysis == 'bivariate':
            #bi_graph()
            print("In progress...")
            pass

        #Plot axes decoration#
        plt.xticks(rotation=tick_rot)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        if breakby:
            plt.legend(loc='best', fancybox=True, framealpha=0.5, title=breakby)
        else:
            plt.legend(loc='best', fancybox=True, framealpha=0.5)
        if 'log' in yscale_type:
            plt.yscale('symlog')
        if 'log' in xscale_type:
            plt.xscale('symlog')

    fig.suptitle(supertitle)
    fig.set_tight_layout(True)

    return fig
