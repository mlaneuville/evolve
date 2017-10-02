'''
'''

from glob import glob
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from math import degrees, atan2

rcParams.update({'font.size': 20})

PARAMS = {}
PARAMS['Atmosphere0'] = {'norm':4e18, 'ylabel':'N-content [PAL]', 'isLog':True, 'Earth':1}
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
PROPERTIES['man-mix'] = {'xlabel':'Mantle mixing rate [-]'}
PROPERTIES['oce-mix'] = {'xlabel':'Ocean HT. circulation rate [-]'}
PROPERTIES['man-ox'] = {'xlabel':'Mantle redox state [-]'}
PROPERTIES['atm-ox'] = {'xlabel':'Atmosphere redox state [-]'}
PROPERTIES['out2in'] = {'xlabel':'Biotic direction ratio [-]'}
PROPERTIES['F0'] = {'xlabel':'Biotic cycling rate [-]'}


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-f', '--folder', action='append', default=[], help='data directory')
PARSER.add_argument('-o', '--outname', default='output.eps', help='output filename')
PARSER.add_argument('-l', '--legend', action='append', default=[], help='legend labels')
PARSER.add_argument('-c', '--column', action='append', default=[], help='column(s) to plot')
PARSER.add_argument('-r', '--relative', action='store_true', help='divide by value at t=0')
PARSER.add_argument('-n', '--notation', help='plot description, i.e., (a), (b)...')

ARGS = PARSER.parse_args()

DATA_DIRECTORY = ARGS.folder
COLORS = ['b', 'g', 'r']



FIG = plt.figure(figsize=(8, 8))

#for folder in sorted(os.listdir(DATA_DIRECTORY)):
#    if not os.path.isdir(DATA_DIRECTORY+folder):
#        continue
#
#    folder = DATA_DIRECTORY + folder

yaxis = [[ [] for x in ARGS.column ] for y in ARGS.folder]
y_err = [[ [] for x in ARGS.column ] for y in ARGS.folder]
values = [[ [] for x in ARGS.column ] for y in ARGS.folder]

for k, folder in enumerate(ARGS.folder):
    xaxis = []
    files = glob(folder+'/*.txt')
    for data_file in sorted(files, key=lambda x: float(x.split("/")[-1].split("_")[-1][:-4])):
        dataframe = pd.read_csv(data_file)
        param = float(data_file.split("/")[-1].split("_")[-1][:-4])
        print(data_file,param)
    
        print(ARGS.column)
        for i, col in enumerate(ARGS.column):
            norm = PARAMS.get(col, PARAMS_DEFAULT)['norm']
            values[k][i].append(dataframe[col].values[-1]/norm)
    
        xaxis.append(param)
    
        for i in range(len(ARGS.column)):
            #yaxis[i].append(np.mean(values[i])) why was I taking the mean here?!
            yaxis[k][i].append(values[k][i][-1])
            y_err[k][i].append(np.std(values[k][i]))

for i in range(len(ARGS.column)):
    for k, folder in enumerate(ARGS.folder):
        yval = np.array(yaxis[k][i])
        if ARGS.relative:
            yval /= yaxis[i][0]
        yerr = np.array(y_err[k][i])

        if len(ARGS.folder) > 1:
            plt.plot(xaxis, yval, COLORS[k], lw=2, label=ARGS.column[i])
        else:
            plt.plot(xaxis, yval, COLORS[i], lw=2, label=ARGS.column[i])
#    plt.fill_between(xaxis, yval-yerr, yval+yerr, facecolor=COLORS[i], alpha=0.5)

#if PARAMS[ARGS.column[0]]['isLog']:
    #plt.yscale('log')
#plt.xscale('log')

plt.ylim(0)
plt.xlim(0, 1)
plt.xlabel(PROPERTIES[ARGS.folder[0].split("/")[-2]]['xlabel'])

ylabel = PARAMS.get(col, PARAMS_DEFAULT)['ylabel']
plt.ylabel(ylabel)

def labelLine(line,x,label=None,align=True,**kwargs):

    ax = line.get_axes()
    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if (x < xdata[0]) or (x > xdata[-1]):
        print('x label location is outside data range!')
        return

    #Find corresponding y co-ordinate and angle of the
    ip = 1
    for i in range(len(xdata)):
        if x < xdata[i]:
            ip = i
            break

    y = ydata[ip-1] + (ydata[ip]-ydata[ip-1])*(x-xdata[ip-1])/(xdata[ip]-xdata[ip-1])

    if not label:
        label = line.get_label()

    if align:
        #Compute the slope
        dx = xdata[ip] - xdata[ip-1]
        dy = ydata[ip] - ydata[ip-1]
        ang = degrees(atan2(dy,dx))

        #Transform to screen co-ordinates
        pt = np.array([x,y]).reshape((1,2))
        trans_angle = ax.transData.transform_angles(np.array((ang,)),pt)[0]

    else:
        trans_angle = 0

    #Set a bunch of keyword arguments
    if 'color' not in kwargs:
        kwargs['color'] = line.get_color()

    if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
        kwargs['ha'] = 'center'

    if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
        kwargs['va'] = 'center'

    if 'backgroundcolor' not in kwargs:
        kwargs['backgroundcolor'] = ax.get_axis_bgcolor()

    if 'clip_on' not in kwargs:
        kwargs['clip_on'] = True

    if 'zorder' not in kwargs:
        kwargs['zorder'] = 2.5

    ax.text(x,y,label,rotation=trans_angle,**kwargs)

def labelLines(lines,align=True,xvals=None,legend=None,**kwargs):

    ax = lines[0].get_axes()
    labLines = []
    labels = []

    #Take only the lines which have labels other than the default ones
    for line in lines:
        label = line.get_label()
        if "_line" not in label:
            labLines.append(line)
            labels.append(label)
    if legend:
        labels = legend

    if xvals is None:
        xmin,xmax = ax.get_xlim()
        xvals = np.linspace(xmin,xmax,len(labLines)+2)[1:-1]

    for line,x,label in zip(labLines,xvals,labels):
        labelLine(line,x,label,align,**kwargs)

#labelLines(plt.gca().get_lines(), xvals=[1e-7, 1e-7, 1e-7], legend=ARGS.legend, zorder=2.5)

if ARGS.notation:
    plt.title(ARGS.notation, x=0.9, y=0.7)

if len(ARGS.legend) != 0:
    plt.legend(ARGS.legend, loc='upper left')

plt.grid()
plt.savefig(ARGS.outname, format='eps', bbox_inches='tight')
