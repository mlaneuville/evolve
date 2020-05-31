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

from tools import Parameters, loadfile

rcParams.update({'font.size': 20, 'axes.axisbelow': True})

PARSER = argparse.ArgumentParser()
PARSER.add_argument(dest='fnames', nargs='*', help='file to use for plotting')
PARSER.add_argument('-c', '--columns', action='append', default=[], help='column(s) to plot')
PARSER.add_argument('-o', '--outname', default='output.png', help='output filename')
PARSER.add_argument('-e', '--earth', action='store_true', help='plot earth val')

ARGS = PARSER.parse_args()
PARAMS = Parameters().params

COLORS = ['k', 'k', 'k', 'k']
STYLES = ['-', ':', '-.', '--']

FIG = plt.figure(figsize=(8, 8))
handles = []

def plot_time_evolution(ARGS):
    print(ARGS.fnames)
    if len(ARGS.fnames) < 5:
        for j, fname in enumerate(sorted(ARGS.fnames)):
            xaxis, yaxis = loadfile(fname, ARGS.columns, PARAMS)
            if xaxis is None:
                continue
            for i, col in enumerate(ARGS.columns):
                h, = plt.plot(xaxis, yaxis[i], COLORS[j], ls=STYLES[j], lw=2)
                handles.append(h)
                if ARGS.earth:
                    plt.axhline(y=PARAMS[col].earthscale, color='k', ls='--', lw=2)
    else: # fill_between plot
        for i, col in enumerate(ARGS.columns):
            min_vals = None
            max_vals = None
            for fname in ARGS.fnames:
                xaxis, yaxis = loadfile(fname, col, PARAMS)
                if xaxis is None:
                    continue

                if min_vals is None:
                    min_vals = yaxis[0]
                    max_vals = yaxis[0]
                    continue
    
                x_vals = xaxis
                min_vals = np.minimum(min_vals, yaxis[0])
                max_vals = np.maximum(max_vals, yaxis[0])
    
            h = plt.fill_between(x_vals, min_vals, max_vals,
                                 lw=None, edgecolor=COLORS[i], facecolor=COLORS[i])
            handles.append(h)
    
            if ARGS.earth:
                plt.axhline(y=PARAMS[col].earthscale, color=COLORS[i], ls='--', lw=2)
        
    
    plt.ylabel(PARAMS[ARGS.columns[0]].ylabel)
    plt.xlabel('Time since formation [Ma]')
    plt.xlim(0, 4500)
    plt.xticks(np.arange(500, 4500, 1000))
    
    if PARAMS[ARGS.columns[0]].islog:
        plt.yscale('log')

    plt.grid(ls='dashed')
    plt.savefig(ARGS.outname, format='png', bbox_inches='tight')

if __name__ == "__main__":
    plot_time_evolution(ARGS)
