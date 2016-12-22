'''
'''

from glob import glob
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

rcParams.update({'font.size': 20})

PARAMS = {}
PARAMS['Atmosphere0'] = {'norm':4e18, 'ylabel':'N-content [PAL]', 'isLog':False, 'Earth':1}
PARAMS['Oceans0'] = {'norm':3.8e16, 'ylabel':'N-content [mM]', 'isLog':True, 'Earth':0.6}
PARAMS['Oceans1'] = {'norm':5.1e16, 'ylabel':'N-content [mM]', 'isLog':False, 'Earth':0.1}
PARAMS['Oceans2'] = {'norm':2.4e16, 'ylabel':'N-content [mM]', 'isLog':True, 'Earth':3e-4}
PARAMS['LMantle2'] = {'norm':2.5e16, 'ylabel':'N-content [ppm]', 'isLog':False, 'Earth':1}
PARAMS['UMantle2'] = {'norm':9.6e17, 'ylabel':'N-content [ppm]', 'isLog':False, 'Earth':1}
PARAMS['OCrust2'] = {'norm':1e15, 'ylabel':'N-content [ppm]', 'isLog':True, 'Earth':500}
PARAMS['Volcanism0'] = {'norm':1e11, 'ylabel':'Degassing rate [10$^{11}$ kg yr$^{-1}$]', 'isLog':False}
PARAMS['Volcanism1'] = {'norm':1e11, 'ylabel':'Degassing rate [10$^{11}$ kg yr$^{-1}$]', 'isLog':False}
PARAMS['Volcanism2'] = {'norm':1e11, 'ylabel':'Degassing rate [10$^{11}$ kg yr$^{-1}$]', 'isLog':False}

PARAMS_DEFAULT = {'norm':1, 'ylabel':'[]', 'isLog':True, 'Earth':1}

PROPERTIES = {}
PROPERTIES['comp-conv'] = {'xlabel':'Mantle mixing rate [-]'}
PROPERTIES['comp-hydro'] = {'xlabel':'Oceans mixing rate [-]'}
PROPERTIES['redox-mantle'] = {'xlabel':'Mantle redox state [-]'}
PROPERTIES['redox-atmosphere'] = {'xlabel':'Atmosphere redox state [-]'}


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-f', '--folder', help='data directory')
PARSER.add_argument('-o', '--outname', default='output.eps', help='output filename')
PARSER.add_argument('-l', '--legend', action='append', default=[], help='legend labels')
PARSER.add_argument('-c', '--column', action='append', default=[], help='column(s) to plot')
PARSER.add_argument('-r', '--relative', action='store_true', help='divide by value at t=0')

ARGS = PARSER.parse_args()

DATA_DIRECTORY = ARGS.folder
COLORS = ['b', 'g', 'r']

xaxis = []

yaxis = [ [] for x in ARGS.column]
y_err = [ [] for x in ARGS.column]

FIG = plt.figure(figsize=(8, 8))

for folder in sorted(os.listdir(DATA_DIRECTORY)):
    if not os.path.isdir(DATA_DIRECTORY+folder):
        continue

    folder = DATA_DIRECTORY + folder

    values = [ [] for x in ARGS.column]

    for data_file in glob(folder+'/*.txt'):
        dataframe = pd.read_csv(data_file)
        param = int(data_file.split("/")[-2])

        for i, col in enumerate(ARGS.column):
            norm = PARAMS.get(col, PARAMS_DEFAULT)['norm']
            values[i].append(dataframe[col].values[-1]/norm)

    xaxis.append(param)

    for i in range(len(ARGS.column)):
        yaxis[i].append(np.mean(values[i]))
        y_err[i].append(np.std(values[i]))

for i in range(len(ARGS.column)):
    yval = np.array(yaxis[i])
    if ARGS.relative:
        yval /= yaxis[i][0]
    yerr = np.array(y_err[i])

    plt.plot(xaxis, yval, COLORS[i], lw=2, label=ARGS.column[i])
#    plt.fill_between(xaxis, yval-yerr, yval+yerr, facecolor=COLORS[i], alpha=0.5)

#plt.yscale('log')
#plt.ylim(1e-2, 1e3)
plt.xlabel(PROPERTIES[DATA_DIRECTORY.split("/")[-2]]['xlabel'])

ylabel = PARAMS.get(col, PARAMS_DEFAULT)['ylabel']
plt.ylabel(ylabel)

if len(ARGS.legend) != 0:
    plt.legend(ARGS.legend, loc='best')
#else:
#    plt.legend(loc='best')
plt.grid()
plt.savefig(ARGS.outname, format='eps', bbox_inches='tight')
