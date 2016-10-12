'''
Generates a series of heatmaps to show the distribution of nitrogen content in a
given reservoir (x-axis) as a function of redox parameter (y-axis). The color
scale is a histogram of the distribution of random runs for a given redox value.
'''

from glob import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

COLUMNS = ["Atmosphere0", "Oceans0", "Oceans1", "Oceans2", "LMantle2", "UMantle2", "OCrust2"]

UNITS = {"Atmosphere0": "PAL",
         "Oceans0": "mM",
         "Oceans1": "mM",
         "Oceans2": "mM",
         "LMantle2": "ppm",
         "UMantle2": "ppm",
         "OCrust2": "ppm"}

NORMS = {"Atmosphere0": 4e18,  # PAL
         "Oceans0": 3.8e16,    # mM ; molar = m*1e3 g/(28g/mol)/1.35e21 L
         "Oceans1": 5.1e16,    # mM ; average of 30 and 46 g/mol
         "Oceans2": 2.4e16,    # mM ; average of 17 and 18 g/mol
         "LMantle2": 2.5e18,   # ppm ; v(lmantle) = 6.3e20 m3, rho = 4000 kg/m3
         "UMantle2": 9.6e17,   # ppm ; v(umantle) = 2.4e20 m3, rho = 4000 kg/m3
         "OCrust2": 1e15}      # ppm ; msed = 1.04e21 kg

DATA_DIRECTORY = "../output/"

def get_full_data(field_, norm, time):
    '''Get data (time and field vectors) for a given time. Fetches output from
       all folders in DATA_DIRECTORY.'''

    xval = []
    yval = []

    for folder in sorted(os.listdir(DATA_DIRECTORY)):
        if not os.path.isdir(DATA_DIRECTORY+folder):
            continue

        folder = DATA_DIRECTORY + folder
        ndata = len(glob(folder+'/*.txt'))

        for data_file in glob(folder+'/*.txt'):
            dataframe = pd.read_csv(data_file)
            oxi = int(data_file.split("/")[2][4:7])

            reservoir = dataframe[field_].values[time]
            simtime = dataframe["time"].values[time]

            xval.append(reservoir/norm)
            yval.append(oxi)

    return xval, yval, simtime, ndata



def make_time_plot(field_, norm, time):
    '''Makes the heatmap for a given time and field.'''

    xval, yval, simtime, ndata = get_full_data(field_, norm, time)

    print(np.min(xval))
    print(np.max(xval))

    print(np.min(yval))
    print(np.max(yval))

    plt.figure()

    xbins = np.logspace(-2, 2, 26)
    ybins = np.linspace(75, 100, 26)
    counts, _, _ = np.histogram2d(xval, yval, bins=(xbins, ybins))
    print(counts.shape)

    plt.pcolormesh(xbins, ybins, counts.T)
    plt.colorbar()
    plt.clim(0, ndata)

    plt.xscale('log')

    plt.title("%s - %04d Ma" % (field_, simtime))
    plt.xlabel("N-content [%s]" % UNITS[field_])
    plt.ylabel("Redox state [-]")
    plt.savefig("%s-%03d.png" % (field_, time), format="png")
    plt.close()



def run_timeloop(field_):
    '''Makes all heatmaps for a given field'''
    print(field_)
    norm = NORMS[field_]
    for i in range(180):
        print(i)
        make_time_plot(field_, norm, i)



#run_timeloop("Oceans1")
for field in COLUMNS:
    run_timeloop(field)
