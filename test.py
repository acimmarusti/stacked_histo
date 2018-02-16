from __future__ import division, print_function
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

keys = [('xf','yf'),('xr','yr')]
brkdown = ['tool']
analysis = 'univariate'
plot_type = 'box'

if len(brkdown) < 1:

    hue = 1
    breakd = [()]

else:

    hue = len(brkdown)
    breakd = brkdown

if analysis == 'bivariate' and len(keys) > 1:
    diff_plots = list(combinations(keys, 2))
elif analysis == 'univariate' or len(keys) < 2:
    diff_plots = keys

if len(keys) < 2:
    analysis = 'univariate'
        
#Supported plot types#
#Univariate#
uni_types = ['hist','box','violin']
#Bivariate#
bi_types = ['relational','hist']

if (analysis == 'bivariate' and (not plot_type in bi_types)) or (analysis == 'univariate' and (not plot_type in uni_types)):

    print(plot_type + " is unsupported for " + analysis + " type")
            
    exit(0)
    
print(diff_plots)
print(breakd)

#Subplot array#
num_diff_plots = len(diff_plots)
numplts = num_diff_plots * hue

print("Number of different plots: ", num_diff_plots)

#Possible combinations#
possibilities = product(diff_plots, breakd)

possible = list(possibilities)

print(possible)

if not possible:

    print("Possible combinations list is empty. If plotting without breakdown make sure breakdown=[()]\n")
    exit(0)

for cols, breakby in possible:

    #Packing and unpacking variables#
    toplot = put_in_list(cols)

    print(toplot)
    
    if len(toplot) == 2 and analysis == 'bivariate':
        xlabel, ylabel = toplot
    elif len(toplot) == 1 and analysis == 'univariate':
        xlabel, = toplot
        ylabel = 'Events'
    else:
        xlabel = ''
        ylabel = ''

    print(xlabel,ylabel)


