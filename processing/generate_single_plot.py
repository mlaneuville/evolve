'''
Should be able to generate different time evolution plots.
    - choose folder (with comparison capability)
    - choose data to output and axis
'''
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PARAMS = {}
PARAMS['Atmosphere0'] = {'norm':4e18, 'ylabel':'N-content [PAL]', 'isLog':False, 'Earth':1}
PARAMS['Oceans0'] = {'norm':3.8e16, 'ylabel':'N-content [mM]', 'isLog':True, 'Earth':0.6}
PARAMS['Oceans1'] = {'norm':5.1e16, 'ylabel':'N-content [mM]', 'isLog':False, 'Earth':0.1}
PARAMS['Oceans2'] = {'norm':2.4e16, 'ylabel':'N-content [mM]', 'isLog':True, 'Earth':3e-4}
PARAMS['LMantle2'] = {'norm':2.5e16, 'ylabel':'N-content [ppm]', 'isLog':False, 'Earth':1}
PARAMS['UMantle2'] = {'norm':9.6e17, 'ylabel':'N-content [ppm]', 'isLog':False, 'Earth':1}
PARAMS['OCrust2'] = {'norm':1e15, 'ylabel':'N-content [ppm]', 'isLog':True, 'Earth':500}

PARSER = argparse.ArgumentParser()
PARSER.add_argument(dest='fnames', nargs='*', help='file to use for plotting')
PARSER.add_argument('-c', '--column', action='append', default=[], help='column(s) to plot')
PARSER.add_argument('-l', '--legend', action='append', default=[], help='legend labels')
PARSER.add_argument('-o', '--outname', default='output.png', help='output filename')
PARSER.add_argument('-e', '--earth', action='store_true', help='plot earth val')

ARGS = PARSER.parse_args()

COLORS = ['b', 'g', 'r']

FIG = plt.figure(figsize=(8, 8))

if len(ARGS.fnames) < 6:
    for fname in ARGS.fnames:
        data = pd.read_csv(fname)
        for col in ARGS.column:
            plt.plot(data['time'],
                     data[col]/PARAMS[col]['norm'],
                     lw=2)
else: # fill_between plot
    for i, col in enumerate(ARGS.column):
        min_vals = []
        max_vals = []
        for fname in ARGS.fnames:
            data = pd.read_csv(fname)
            if len(min_vals) == 0:
                min_vals = data[col]
                max_vals = data[col]
                continue

            min_vals = np.minimum(min_vals, data[col])
            max_vals = np.maximum(max_vals, data[col])

        plt.fill_between(data['time'],
                         min_vals/PARAMS[col]['norm'],
                         max_vals/PARAMS[col]['norm'],
                         lw=None, edgecolor=COLORS[i], facecolor=COLORS[i])

        if ARGS.earth:
            plt.axhline(y=PARAMS[col]['Earth'], color=COLORS[i], ls='--')
    

plt.title(ARGS.column[0])
plt.ylabel(PARAMS[ARGS.column[0]]['ylabel'])
plt.xlabel('Time since formation [Ma]')

if len(ARGS.legend) != 0:
    plt.legend(ARGS.legend, loc='best')

if PARAMS[ARGS.column[0]]['isLog']:
    plt.yscale('log')

plt.grid()
plt.savefig(ARGS.outname, format='png', bbox_inches='tight')
