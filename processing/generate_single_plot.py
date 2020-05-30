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

from parameters import Parameters

rcParams.update({'font.size': 20, 'axes.axisbelow': True})

PARSER = argparse.ArgumentParser()
PARSER.add_argument(dest='fnames', nargs='*', help='file to use for plotting')
PARSER.add_argument('-c', '--column', action='append', default=[], help='column(s) to plot')
PARSER.add_argument('-l', '--legend', action='append', default=[], help='legend labels')
PARSER.add_argument('-o', '--outname', default='output.eps', help='output filename')
PARSER.add_argument('-e', '--earth', action='store_true', help='plot earth val')
PARSER.add_argument('-d', '--deriv', action='store_true', help='plot time derivative')
PARSER.add_argument('-p', '--phase', action='store_true', help='plot phase space')
PARSER.add_argument('-n', '--notation', help='plot description, i.e., (a), (b)...')

ARGS = PARSER.parse_args()
PARAMS = Parameters().params

COLORS = ['k', 'k', 'k', 'k']
STYLES = ['-', ':', '-.', '--']

FIG = plt.figure(figsize=(8, 8))
handles = []


def plot_time_evolution(ARGS):
    if len(ARGS.fnames) < 5:
        for j,fname in enumerate(sorted(ARGS.fnames)):
            print(fname)
            data = pd.read_csv(fname)
            for i, col in enumerate(ARGS.column):
                yaxis = data[col].values
                yaxis /= PARAMS[col].norm
                if ARGS.deriv:
                    yaxis /= yaxis[-1]
                    yaxis = np.gradient(yaxis)
                h, = plt.plot(data['time'][0:],
                             yaxis[0:], COLORS[j], ls=STYLES[j], lw=2)
                handles.append(h)
                if ARGS.earth:
                    #plt.axhline(y=PARAMS[col]['Earth'], color=COLORS[i], ls='--', lw=2)
                    plt.axhline(y=PARAMS[col].earthscale, color='k', ls='--', lw=2)
                #if col == "FreundlichAdsorption0":
                #    plt.ylim(1, 3)
                if col == "Oceans21":
                    plt.yscale("log")
                    if fname.split("/")[-1] == "out_E6_4.txt":
                        plt.ylim(1e-4, 3e2)
                    else:
                        plt.ylim(1e1, 150)
                if col == "Atmosphere2":
                    plt.ylim(1e14, 1e18)
                if col == "Volcanism0":
                    plt.ylim(1e9, 2e10)
    else: # fill_between plot
        for i, col in enumerate(ARGS.column):
            min_vals = []
            max_vals = []
            for fname in ARGS.fnames:
                data = pd.read_csv(fname)
                if len(min_vals) == 0:
                    min_vals = data[col].values
                    max_vals = data[col].values
                    continue
    
                min_vals = np.minimum(min_vals, data[col].values)
                max_vals = np.maximum(max_vals, data[col].values)
    
            h = plt.fill_between(data['time'][1:],
                                 min_vals[1:]/PARAMS[col].norm,
                                 max_vals[1:]/PARAMS[col].norm,
                                 lw=None, edgecolor=COLORS[i], facecolor=COLORS[i])
            handles.append(h)
    
            if ARGS.earth:
                plt.axhline(y=PARAMS[col].earthscale, color=COLORS[i], ls='--', lw=2)
        
    
    #plt.title(ARGS.column[0])
    plt.ylabel(PARAMS[ARGS.column[0]].ylabel)
    plt.xlabel('Time since formation [Ma]')
    plt.xlim(0, 4500)
    plt.xticks(np.arange(500, 4500, 1000))
    
    if len(ARGS.legend) != 0:
        if ARGS.notation == '(d)' or ARGS.notation == '(c)':
            plt.legend(handles, ARGS.legend, loc='lower right')
        else:
            plt.legend(handles, ARGS.legend, loc='upper left')
    
    if PARAMS[ARGS.column[0]].islog:
        plt.yscale('log')

    print(ARGS.column[0][:3])
    if ARGS.column[0][:3] == 'Vol': # volcanism
        plt.ylim(1e9, 1e11)
    if col == "Atmosphere0":
        plt.ylim(0., 1.5)
    if col == "LMantle2":
        plt.ylim(0., 5.)
    if col == "Oceans1":
        plt.ylim(0, 10)
    if col == "Oceans2":
        plt.ylim(0, 800)

    if ARGS.notation:
        plt.title(ARGS.notation, x=0.9, y=0.85)
    
    plt.grid(ls='dashed')
    plt.savefig(ARGS.outname, format='eps', bbox_inches='tight')

if __name__ == "__main__":
    plot_time_evolution(ARGS)
