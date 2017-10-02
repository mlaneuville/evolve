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

rcParams.update({'font.size': 20,
                 'axes.axisbelow': True})

PARAMS = {}
PARAMS['Atmosphere0'] = {'norm':4e18, 'ylabel':'N-content [PAL]', 'isLog':False, 'Earth':1}
PARAMS['Oceans0'] = {'norm':3.8e16, 'ylabel':'N-content [mM]', 'isLog':True, 'Earth':0.63}
PARAMS['Oceans1'] = {'norm':5.1e16, 'ylabel':'N-content [mM]', 'isLog':False, 'Earth':1e-2}
PARAMS['Oceans2'] = {'norm':2.4e16, 'ylabel':'N-content [mM]', 'isLog':False, 'Earth':3e-4}
PARAMS['LMantle2'] = {'norm':2.5e18, 'ylabel':'N-content [ppm]', 'isLog':False, 'Earth':1.4}
PARAMS['UMantle2'] = {'norm':9.6e17, 'ylabel':'N-content [ppm]', 'isLog':True, 'Earth':3.5}
PARAMS['OCrust2'] = {'norm':1e15, 'ylabel':'N-content [ppm]', 'isLog':True, 'Earth':200}
PARAMS['Atmosphere2'] = {'norm':1, 'ylabel':'N-content [kg]', 'isLog':True, 'Earth':1e15} # biosphere
PARAMS['BioticContribution0'] = {'norm':1, 'ylabel':'N-content [kg]', 'isLog':True, 'Earth':1} # biosphere
PARAMS['BioticContribution1'] = {'norm':1, 'ylabel':'Synthesis pathway', 'isLog':False, 'Earth':1} # biosphere
PARAMS['BioticContribution2'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':False, 'Earth':1} # biosphere
PARAMS['Henry0'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':False, 'Earth':1} # biosphere
PARAMS['AbioticFixation0'] = {'norm':1e10, 'ylabel':'Abiotic fixation [1e10 kg/yr]', 'isLog':False, 'Earth':1} # biosphere
PARAMS['HydrothermalCirculation0'] = {'norm':1e10, 'ylabel':'HT. circulation from NO$_x$ [1e10 kg/yr]', 'isLog':False, 'Earth':1} # biosphere
PARAMS['HydrothermalCirculation1'] = {'norm':1e6, 'ylabel':'HT. circulation from N$_2$ [1e6 kg/yr]', 'isLog':False, 'Earth':1} # biosphere
PARAMS['FreundlichAdsorption0'] = {'norm':1e10, 'ylabel':'Freundlich adsorption [1e10 kg/yr]', 'isLog':False, 'Earth':1} # biosphere
PARAMS['Volcanism0'] = {'norm':1e10, 'ylabel':'Volcanic N-flux as N$_2$ [1e10 kg/yr]', 'isLog':False, 'Earth':1} # biosphere 
PARAMS['Volcanism1'] = {'norm':1, 'ylabel':'Volcanic N-flux as NH$_x$ [kg/yr]', 'isLog':True, 'Earth':1} # biosphere
PARAMS['Volcanism2'] = {'norm':1, 'ylabel':'Volcanic N-flux as NH$_x$ [kg/yr]', 'isLog':True, 'Earth':1} # biosphere
PARAMS['Subduction0'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':True, 'Earth':1} # biosphere
PARAMS['Convection0'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':True, 'Earth':1} # biosphere
PARAMS['CometDelivery0'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':True, 'Earth':1} # biosphere
PARAMS['Impacts0'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':True, 'Earth':1} # biosphere
PARAMS['Continents2'] = {'norm':1, 'ylabel':'N-content [kg]', 'isLog':False, 'Earth':1}

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

COLORS = ['k', 'g', 'r', 'b']

FIG = plt.figure(figsize=(8, 8))
handles = []

def plot_phase_space(ARGS):
    for fname in ARGS.fnames:
        print(fname)
        data = pd.read_csv(fname)

        xaxis = data[ARGS.column[0]].values[1:]
        xaxis /= PARAMS[ARGS.column[0]]['norm']

        yaxis = data[ARGS.column[1]].values[1:]
        yaxis /= PARAMS[ARGS.column[1]]['norm']

        bio = np.where(data["time"] > 1000)[0][0]
        snapshots = [0, -1]
        colors = ['ko', 'r*']
        msize = [10, 20]

        plt.plot(xaxis, yaxis, 'k')
        for idx, col, size in zip(snapshots, colors, msize):
            plt.plot(xaxis[idx], yaxis[idx], col, markersize=size)

    plt.xlabel(PARAMS[ARGS.column[0]]['ylabel'])
    plt.ylabel(PARAMS[ARGS.column[1]]['ylabel'])
    plt.grid()
    plt.savefig(ARGS.outname, format='eps', bbox_inches='tight')

def plot_time_evolution(ARGS):
    if len(ARGS.fnames) < 5:
        for j,fname in enumerate(sorted(ARGS.fnames)):
            print(fname)
            data = pd.read_csv(fname)
            for i, col in enumerate(ARGS.column):
                yaxis = data[col].values
                yaxis /= PARAMS[col]['norm']
                if ARGS.deriv:
                    yaxis /= yaxis[-1]
                    yaxis = np.gradient(yaxis)
                h, = plt.plot(data['time'][0:],
                             yaxis[0:], COLORS[j],
                             lw=2)
                handles.append(h)
                if ARGS.earth:
                    #plt.axhline(y=PARAMS[col]['Earth'], color=COLORS[i], ls='--', lw=2)
                    plt.axhline(y=PARAMS[col]['Earth'], color='k', ls='--', lw=2)
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
                                 min_vals[1:]/PARAMS[col]['norm'],
                                 max_vals[1:]/PARAMS[col]['norm'],
                                 lw=None, edgecolor=COLORS[i], facecolor=COLORS[i])
            handles.append(h)
    
            if ARGS.earth:
                plt.axhline(y=PARAMS[col]['Earth'], color=COLORS[i], ls='--', lw=2)
        
    
    #plt.title(ARGS.column[0])
    plt.ylabel(PARAMS[ARGS.column[0]]['ylabel'])
    plt.xlabel('Time since formation [Ma]')
    plt.xlim(0, 4500)
    plt.xticks(np.arange(500, 4500, 1000))
    
    if len(ARGS.legend) != 0:
        plt.legend(handles, ARGS.legend, loc='upper left')
    
    if PARAMS[ARGS.column[0]]['isLog']:
        plt.yscale('log')

    print(ARGS.column[0][:3])
    if ARGS.column[0][:3] == 'Vol': # volcanism
        plt.ylim(1e9, 1e11)
    if col == "Volcanism0":
        plt.ylim(0.5, 1.0)

    if ARGS.notation:
        if ARGS.notation == '(d)':
            plt.title(ARGS.notation, x=0.9, y=0.1)
        else:
            plt.title(ARGS.notation, x=0.9, y=0.85)
    
    plt.grid(ls='dashed')
    plt.savefig(ARGS.outname, format='eps', bbox_inches='tight')

if ARGS.phase:
    if len(ARGS.column) != 2:
        print("Please specify two columns for phase space.")
        sys.exit()
    plot_phase_space(ARGS)
else:
    print(ARGS.fnames)
    plot_time_evolution(ARGS)
