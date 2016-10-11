from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import os

columns = ["Atmosphere0", "Oceans0", "Oceans1", "Oceans2", "LMantle2", "UMantle2", "OCrust2"]

units = {"Atmosphere0": "PAL",
         "Oceans0": "mM", 
         "Oceans1": "mM", 
         "Oceans2": "mM", 
         "LMantle2": "ppm", 
         "UMantle2": "ppm", 
         "OCrust2": "ppm"}

norms = {"Atmosphere0": 4e18,  # PAL
         "Oceans0": 3.8e16,    # mM ; molar = m*1e3 g/(28g/mol)/1.35e21 L
         "Oceans1": 5.1e16,    # mM ; average of 30 and 46 g/mol
         "Oceans2": 2.4e16,    # mM ; average of 17 and 18 g/mol
         "LMantle2": 2.5e18,   # ppm ; v(lmantle) = 6.3e20 m3, rho = 4000 kg/m3
         "UMantle2": 9.6e17,   # ppm ; v(umantle) = 2.4e20 m3, rho = 4000 kg/m3 
         "OCrust2": 1e15}      # ppm ; msed = 1.04e21 kg

DATA_DIRECTORY = "../output/"

def make_time_plot(field, norm, time):
    xval = []
    yval = []

    for folder in sorted(os.listdir(DATA_DIRECTORY)):
        if not os.path.isdir(DATA_DIRECTORY+folder):
            continue
    
        folder = DATA_DIRECTORY + folder
        ndata = len(glob(folder+'/*.txt'))
    
        for data_file in glob(folder+'/*.txt'):
            df = pd.read_csv(data_file)
            oxi = int(data_file.split("/")[2][4:7])

            reservoir = df[field].values[time]
            simtime = df["time"].values[time]

            xval.append(reservoir/norm)
            yval.append(oxi)

    print(np.min(xval))
    print(np.max(xval))

    print(np.min(yval))
    print(np.max(yval))

    
    plt.figure()

    xr = np.logspace(-2, 2, 26)
    yr = np.linspace(75, 100, 26)
    counts, _, _ = np.histogram2d(xval, yval, bins=(xr, yr))
    print(counts.shape)

#    xr = np.linspace(0, 5, len(xr)-1)
#    yr = np.linspace(75, 100, len(yr)-1)
#    X, Y = np.meshgrid(xr, yr)

    levels = np.linspace(0, 0.5, 101)
#    plt.contourf(counts, levels)
    plt.pcolormesh(xr, yr, counts.T)
    plt.colorbar()
    plt.clim(0, ndata)
    
    plt.xscale('log')

    plt.title("%s - %04d Ma" % (field, simtime))
    plt.xlabel("N-content [%s]" % units[field])
    plt.ylabel("Redox state [-]")
    plt.savefig("%s-%03d.png" % (field, time), format="png")
    plt.close()

def run_timeloop(field):
    print(field)
    norm = norms[field]
    for i in range(180):
        print(i)
        make_time_plot(field, norm, i)

#run_timeloop("Oceans1")
for field in columns:
    run_timeloop(field)
