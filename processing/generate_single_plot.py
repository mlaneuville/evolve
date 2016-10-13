'''
Should be able to generate different time evolution plots.
    - choose folder (with comparison capability)
    - choose data to output and axis
'''
import argparse
import pandas as pd
import matplotlib.pyplot as plt

PARAMS = {}
PARAMS['Atmosphere0'] = {'norm':4e18, 'ylabel':'N-content [PAL]', 'isLog':False}
PARAMS['Oceans0'] = {'norm':3.8e16, 'ylabel':'N-content [mM]', 'isLog':True}
PARAMS['Oceans1'] = {'norm':5.1e16, 'ylabel':'N-content [mM]', 'isLog':False}
PARAMS['Oceans2'] = {'norm':2.4e16, 'ylabel':'N-content [mM]', 'isLog':True}
PARAMS['LMantle2'] = {'norm':2.5e16, 'ylabel':'N-content [ppm]', 'isLog':False}
PARAMS['UMantle2'] = {'norm':9.6e17, 'ylabel':'N-content [ppm]', 'isLog':False}
PARAMS['OCrust2'] = {'norm':1e15, 'ylabel':'N-content [ppm]', 'isLog':True}

PARSER = argparse.ArgumentParser()
PARSER.add_argument(dest='fnames', nargs='*', help='file to use for plotting')
PARSER.add_argument('-c', '--column', default='Atmosphere0', type=str, help='column to plot')
PARSER.add_argument('-l', '--legend', action='append', default=[], help='legend labels')
PARSER.add_argument('-f', '--fname', default='output.png', help='output filename')

ARGS = PARSER.parse_args()

FIG = plt.figure(figsize=(8, 8))

if len(ARGS.fnames) < 4:
    for fname in ARGS.fnames:
        data = pd.read_csv(fname)
        plt.plot(data['time'],
                data[ARGS.column]/PARAMS[ARGS.column]['norm'],
                lw=2)
else: # fill_between plot
    other_data = []
    for fname in ARGS.fnames:
        data = pd.read_csv(fname)
        if len(other_data) == 0:
            other_data = data
            continue

        plt.fill_between(data['time'],
                         data[ARGS.column]/PARAMS[ARGS.column]['norm'],
                         other_data[ARGS.column]/PARAMS[ARGS.column]['norm'],
                         lw=None, edgecolor='b')

        other_data = data
    

plt.title(ARGS.column)
plt.ylabel(PARAMS[ARGS.column]['ylabel'])
plt.xlabel('Time since formation [Ma]')

if len(ARGS.legend) != 0:
    plt.legend(ARGS.legend, loc='best')

if PARAMS[ARGS.column]['isLog']:
    plt.yscale('log')

plt.grid()
plt.savefig(ARGS.fname, format='png', bbox_inches='tight')
