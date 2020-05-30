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
PARSER.add_argument('-o', '--outname', default='output.eps', help='output filename')
PARSER.add_argument('-e', '--earth', action='store_true', help='plot earth val')

ARGS = PARSER.parse_args()
PARAMS = Parameters().params

def plot_phase_space(ARGS):
    for fname in ARGS.fnames:
        print(fname)
        data = pd.read_csv(fname)

        xaxis = data[ARGS.column[0]].values[1:]
        xaxis /= PARAMS[ARGS.column[0]].norm

        yaxis = data[ARGS.column[1]].values[1:]
        yaxis /= PARAMS[ARGS.column[1]].norm

        snapshots = [0, -1]
        colors = ['ko', 'k*']
        msize = [10, 20]

        plt.plot(xaxis, yaxis, 'k')
        for idx, col, size in zip(snapshots, colors, msize):
            plt.plot(xaxis[idx], yaxis[idx], col, markersize=size)

    plt.xlabel(PARAMS[ARGS.column[0]].ylabel)
    plt.ylabel(PARAMS[ARGS.column[1]].ylabel)
    plt.grid()
    plt.savefig(ARGS.outname, format='eps', bbox_inches='tight')

if __name__ == "__main__":
    if len(ARGS.column) != 2:
        print("Please specify two columns for phase space.")
        sys.exit()
    plot_phase_space(ARGS)
