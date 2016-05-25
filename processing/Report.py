# -*- coding: utf-8 -*-
"""
@author: mlaneuville
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
from collections import OrderedDict
from PyPDF2 import PdfFileReader, PdfFileMerger
import graphviz
import os
import sys

class Report:
    def __init__(self, name, sim_dir="../output"):
        self.graph_fname = sim_dir + "/out_" + name + ".dot"
        self.fname = sim_dir + "/out_" + name + ".txt"
        self.data = self.load_data(self.fname)
        self.output_file = "report_"+name+".pdf"
        self.timeseries = OrderedDict()
        self.subplots = []
        print(self.data.head())


    def load_data(self, fname):
        return pd.read_csv(fname)


    def get_label(self, name):
        species = {"0": "N2", "1": "NOx", "2": "NH4"}
        label = name
        if isinstance(name, list):
            label = []
            for value in name:
                if value[-1].isdigit():
                    label.append(value[:-1] + " -- " + species[value[-1]])
                else:
                    label.append(value)
        return label


    def add_timeseries(self, name, colnames=[], ylabel="", isLog=False, norm=[]):
        if len(colnames) == 0:
            colnames = [name]
        if len(colnames) != len(norm):
            val = 1 if len(norm) == 0 else norm[0]
            norm = [val for x in colnames]
    
        fig, ax = plt.subplots(1, 1)
        self.timeseries[name] = {'fig':fig, 'ax':ax, 'ylabel':ylabel,
                                 'isLog':isLog, 'colnames':colnames, 'norm':norm} 


    def add_subplot(self, plots):
        if len(plots) == 0 or len(plots) > 4:
            print("Wrong number of plots: "+str(len(plots)))
            sys.exit()

        fig, axarr = plt.subplots(2, 2, sharex=True)

        cols = []
        ylabels = []
        norms = []
        islog = []
        for k, plot in plots.items():
            cols.append(plot['cols'])
            ylabels.append(plot['ylabel'])

            norm = [1] if 'norm' not in plot.keys() else plot['norm']
            norms.append(norm)

            log = True if 'isLog' in plot.keys() else False
            islog.append(log)

        self.subplots.append({'fig':fig, 'ax':axarr, 'cols':cols, 'ylabels':ylabels, 'norms':norms, 'isLog':islog}) 

    def process(self):

        for k, v in self.timeseries.items():
            print("Plotting "+k)
            for column, norm in zip(v['colnames'], v['norm']):
                label = self.get_label(column)
                data = self.data[column][1:]/norm
                if v['isLog']:
                    data = abs(data)
                v['ax'].plot(self.data['time'][1:], data, 
                             lw=2, label=label)

            v['ax'].legend(loc='best')
            v['ax'].set_ylabel(v['ylabel'])
            v['ax'].set_xlabel("Time since formation [Ma]")
            v['ax'].set_title(k)
            v['ax'].grid()

            if v['isLog']:
                v['ax'].set_yscale('log')

        for sub in self.subplots:
            for i, (col, norm, log) in enumerate(zip(sub['cols'], sub['norms'], sub['isLog'])):
                idx = (i/2, i%2)
                data = self.data[col][1:]/norm
                label = self.get_label(col)
                sub['ax'][idx].plot(self.data['time'][1:], data, lw=2)
                sub['ax'][idx].set_xticks(np.arange(0, 4500, 1000))
                sub['ax'][idx].set_ylabel(sub['ylabels'][i])
                leg = sub['ax'][idx].legend(labels=label, loc='best')
                leg.draw_frame(False)
                if log:
                    sub['ax'][idx].set_yscale('log')
                sub['ax'][idx].grid()
                sub['fig'].tight_layout()
                if i >= 2:
                    sub['ax'][idx].set_xlabel("Time since formation [Ma]")


    def to_file(self):

        graph_src = open(self.graph_fname, "r")
        dot = graphviz.Source(graph_src.read(), engine="dot", format="pdf")
        dot.render()

        with PdfPages(self.output_file) as pdf:
            for k, v in self.timeseries.items():
                pdf.savefig(v['fig'])
                plt.close()

            for v in self.subplots:
                pdf.savefig(v['fig'])
                plt.close()


        graph = PdfFileReader("Source.gv.pdf")
        report = PdfFileReader(self.output_file)
        merger = PdfFileMerger()
        merger.append(graph)
        merger.append(report)
        merger.write(self.output_file)
        os.remove("Source.gv.pdf")
        os.remove("Source.gv")
