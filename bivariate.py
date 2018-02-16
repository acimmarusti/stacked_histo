from __future__ import division, print_function
import numpy as np

from common import bestbins,check_support

def bi_graph():

    #Supported plot types#
    bi_types = ['relational','hist']

    check_support(plot_type, bi_types, 'bivariate')
