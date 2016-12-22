'''
'''

import os
import sys
from glob import glob
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-f', '--folder', help='data directory')

ARGS = PARSER.parse_args()

COLNAMES = {    'Convection0':True,
                'FreundlichAdsorption0':True,
                'Subduction0':True,
                'Henry0':True,
                'HydrothermalCirculation0':True,
                'HydrothermalCirculation1':True,
                'Volcanism0':True,
                'Volcanism1':True,
                'Volcanism2':True,
                'Impacts0':True,
                'CometDelivery0':True,
                'AbioticFixation0':True,
                'AbioticFixation1':True }


DATA_DIRECTORY = ARGS.folder

results = {}
for x in COLNAMES.keys():
    if COLNAMES[x]:
        results[x] = []

def get_data():
    for folder in sorted(os.listdir(DATA_DIRECTORY)):
        if not os.path.isdir(DATA_DIRECTORY+folder):
            continue

        print(folder)
        folder = DATA_DIRECTORY + folder

        for data_file in glob(folder+'/*.txt'):
            dataframe = pd.read_csv(data_file)
            for col in COLNAMES.keys():
                if COLNAMES[col]:
                    results[col].append(dataframe[col].values[-1]/1e9) 
            break

    return results

def get_state_for_parameters(i):
    '''Returns present day fluxes for folder i'''
    folder = "%s%03d" %( DATA_DIRECTORY, i)
    print(folder)
    for data_file in glob(folder+'/*.txt'):
        dataframe = pd.read_csv(data_file)
        for col in sorted(COLNAMES.keys()):
            if COLNAMES[col]:
                print('{:25.25}\t{:.1e}'.format(col, dataframe[col].values[-1]))
        break

get_state_for_parameters(25)
sys.exit()

results = get_data()
results = pd.DataFrame(results)

g = sns.PairGrid(results)
g = g.map(plt.scatter)
plt.show()
