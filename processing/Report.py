# -*- coding: utf-8 -*-
"""
@author: mlaneuville
"""
import pandas as pd
import matplotlib.pyplot as plt

class Report:
    def __init__(self, name, sim_dir="../output"):
        self.fname = sim_dir + "/out_" + name + ".txt"
        self.data = self.load_data(self.fname)
        print(self.data.info())

    def load_data(self, fname):
        return pd.read_csv(fname)

    def plot_timeseries(self, name, ylabel="", isLog=False):
        plt.plot(self.data['time'][1:], self.data[name][1:], lw=2)
        plt.ylabel(ylabel)
        plt.xlabel("Time since formation [Ma]")
        plt.grid()
        if isLog:
            plt.yscale('log')
        plt.savefig("report_"+name+".pdf")
        plt.close()
