'''
Should be able to generate different time evolution plots.
    - choose folder (with comparison capability)
    - choose data to output and axis
'''
import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams.update({'font.size': 20})

PARAMS = {}
PARAMS['Atmosphere0'] = {'norm':4e18, 'ylabel':'N-content [PAL]', 'isLog':False, 'Earth':1}
PARAMS['Oceans0'] = {'norm':3.8e16, 'ylabel':'N-content [mM]', 'isLog':False, 'Earth':0.63}
PARAMS['Oceans1'] = {'norm':5.1e16, 'ylabel':'N-content [mM]', 'isLog':False, 'Earth':1e-2}
PARAMS['Oceans2'] = {'norm':2.4e16, 'ylabel':'N-content [mM]', 'isLog':False, 'Earth':3e-4}
PARAMS['LMantle2'] = {'norm':2.5e18, 'ylabel':'N-content [ppm]', 'isLog':False, 'Earth':1.4}
PARAMS['UMantle2'] = {'norm':9.6e17, 'ylabel':'N-content [ppm]', 'isLog':False, 'Earth':3.5}
PARAMS['OCrust2'] = {'norm':1e15, 'ylabel':'N-content [ppm]', 'isLog':False, 'Earth':200}

PARSER = argparse.ArgumentParser()
PARSER.add_argument(dest='fnames', nargs='*', help='file to use for plotting')
PARSER.add_argument('-c', '--column', action='append', default=[], help='column(s) to plot')
PARSER.add_argument('-l', '--legend', action='append', default=[], help='legend labels')
PARSER.add_argument('-o', '--outname', default='output.eps', help='output filename')
PARSER.add_argument('-e', '--earth', action='store_true', help='plot earth val')
PARSER.add_argument('-d', '--deriv', action='store_true', help='plot time derivative')
PARSER.add_argument('-p', '--phase', action='store_true', help='plot phase space')

ARGS = PARSER.parse_args()

COLORS = ['b', 'g', 'r']

FIG = plt.figure(figsize=(8, 8))

def plot_phase_space(ARGS):
    for fname in ARGS.fnames:
        print(fname)
        data = pd.read_csv(fname)

        xaxis = data[ARGS.column[0]].values[1:]
        xaxis /= PARAMS[ARGS.column[0]]['norm']

        yaxis = data[ARGS.column[1]].values[1:]
        yaxis /= PARAMS[ARGS.column[1]]['norm']

        plt.plot(xaxis, yaxis, 'k')
        plt.plot(xaxis[-1], yaxis[-1], 'ro')

    plt.xlabel(PARAMS[ARGS.column[0]]['ylabel'])
    plt.ylabel(PARAMS[ARGS.column[1]]['ylabel'])
    plt.grid()
    plt.savefig(ARGS.outname, format='eps', bbox_inches='tight')

def plot_time_evolution(ARGS):
    if len(ARGS.fnames) < 5:
        for fname in ARGS.fnames:
            data = pd.read_csv(fname)
            for col in ARGS.column:
                yaxis = data[col].values
                yaxis /= PARAMS[col]['norm']
                if ARGS.deriv:
                    yaxis /= yaxis[-1]
                    yaxis = np.gradient(yaxis)
                plt.plot(data['time'][1:],
                         yaxis[1:],
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
    
            plt.fill_between(data['time'][1:],
                             min_vals[1:]/PARAMS[col]['norm'],
                             max_vals[1:]/PARAMS[col]['norm'],
                             lw=None, edgecolor=COLORS[i], facecolor=COLORS[i])
    
            if ARGS.earth:
                plt.axhline(y=PARAMS[col]['Earth'], color=COLORS[i], ls='--')
        
    
    #plt.title(ARGS.column[0])
    plt.ylabel(PARAMS[ARGS.column[0]]['ylabel'])
    plt.xlabel('Time since formation [Ma]')
    plt.xticks(np.arange(500, 4500, 1000))
    
    if len(ARGS.legend) != 0:
        plt.legend(ARGS.legend, loc='best')
    
    if PARAMS[ARGS.column[0]]['isLog']:
        plt.yscale('log')
    
    plt.grid()
    plt.savefig(ARGS.outname, format='eps', bbox_inches='tight')

if ARGS.phase:
    if len(ARGS.column) != 2:
        print("Please specify two columns for phase space.")
        sys.exit()
    plot_phase_space(ARGS)
else:
    plot_time_evolution(ARGS)
