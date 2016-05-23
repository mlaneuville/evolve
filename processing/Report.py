# -*- coding: utf-8 -*-
"""
@author: mlaneuville
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Report:
    def __init__(self, name, sim_dir="../output"):
        self.fname = sim_dir + "/out_" + name + ".txt"
        self.data = self.load_data(self.fname)
        self.output_file = "report_"+name+".pdf"
        self.timeseries = {}
        print(self.data.info())


    def load_data(self, fname):
        return pd.read_csv(fname)


    def add_timeseries(self, name, colnames=[], ylabel="", isLog=False):
        fig, ax = plt.subplots(1, 1)
        if len(colnames) == 0:
            colnames = [name]
        self.timeseries[name] = {'fig':fig, 'ax':ax, 'ylabel':ylabel,
                                 'isLog':isLog, 'colnames':colnames} 


    def process(self):

        fig, ax = plt.subplots(1, 1)


        for k, v in self.timeseries.items():
            print("Plotting "+k)
            for column in v['colnames']:
                v['ax'].plot(self.data['time'][1:], self.data[column][1:], lw=2)
            v['ax'].set_ylabel(v['ylabel'])
            v['ax'].set_xlabel("Time since formation [Ma]")
            v['ax'].set_title(k)
            v['ax'].grid()

            if v['isLog']:
                v['ax'].set_yscale('log')


    def to_file(self):
        with PdfPages(self.output_file) as pdf:
            for k, v in self.timeseries.items():
                pdf.savefig(v['fig'])
                plt.close()
