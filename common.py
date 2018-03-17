from __future__ import division, print_function
import numpy as np

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def check_support(support_query, supported_types, analysis):
    
    if not support_query in supported_types:

        print(support_query + " is unsupported for " + analysis + " analysis")
            
        exit(0)

def bestbins(data):

    #Try to convert data to numpy array#
    try:
        proc_data = np.array(data)
    except Exception as e:
        print('Tried to convert data to numpy array but failed, returning None')
        return None
    
    #Number of data#
    ndata = 1
    for dim in proc_data.shape:
        ndata *= dim

    if ndata <= 1:
        print('Data insufficient or empty')
        return None        

    ##Sturges estimator - good for normal data and smaller datasets##
    bins_sturges = np.log2(ndata) + 1

    ##Freedman-Diaconis estimator - robust against outliers, good for large datasets##

    #Inter-quartile range - Robust against outliers, similar to stdev#
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    
    if isclose(iqr, 0):
        round_arg = bins_sturges
    else:
        #FD Estimator#
        binwidth = 2 * iqr / (ndata ** (1/3))
        bins_fd = np.ptp(data) / binwidth

        #Maximum of the two - As done by numpy.histogram with 'auto' option#
        round_arg = max([bins_sturges, bins_fd])

    #bins = np.round(min([round_arg, np.ptp(data)]))
    bins = np.round(round_arg)
    
    return bins
