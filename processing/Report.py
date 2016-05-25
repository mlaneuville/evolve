# -*- coding: utf-8 -*-
"""
@author: mlaneuville
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
from collections import OrderedDict
from PyPDF2 import PdfFileReader, PdfFileMerger
import graphviz
import os

class Report:
    def __init__(self, name, sim_dir="../output"):
        self.graph_fname = sim_dir + "/out_" + name + ".dot"
        self.fname = sim_dir + "/out_" + name + ".txt"
        self.data = self.load_data(self.fname)
        self.output_file = "report_"+name+".pdf"
        self.timeseries = OrderedDict()
        print(self.data.head())


    def load_data(self, fname):
        return pd.read_csv(fname)


    def get_label(self, name):
        species = {"0": "N2", "1": "NOx", "2": "NH4"}
        label = name
        if name[-1].isdigit():
            label = name[:-1] + " -- " + species[name[-1]]
        return label


    def add_timeseries(self, name, colnames=[], ylabel="", isLog=False, norm=1):
        if len(colnames) == 0:
            colnames = [name]

        fig, ax = plt.subplots(1, 1)
        self.timeseries[name] = {'fig':fig, 'ax':ax, 'ylabel':ylabel,
                                 'isLog':isLog, 'colnames':colnames, 'norm':norm} 


    def process(self):

        for k, v in self.timeseries.items():
            print("Plotting "+k)
            for column in sorted(v['colnames']):
                label = self.get_label(column)
                data = self.data[column][1:]/v['norm']
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


    def to_file(self):

        graph_src = open(self.graph_fname, "r")
        dot = graphviz.Source(graph_src.read(), engine="dot", format="pdf")
        dot.render()

        with PdfPages(self.output_file) as pdf:
            for k, v in self.timeseries.items():
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
