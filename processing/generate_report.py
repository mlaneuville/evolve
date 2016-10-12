'''
Generate fluxes and evolution plots for a given run. If with_graph is set, will
also include the network graph in the output pdf.
'''

from collections import OrderedDict
from glob import glob
import argparse
from Report import Report

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-i', '--id', default=False, type=str,
                    help='Case ID, useful if there is more than one in folder')
PARSER.add_argument('-f', '--folder', default='output/', type=str,
                    help='folder where out_* are stored')

ARGS = PARSER.parse_args()

PLOTS_FLUXES = OrderedDict()
PLOTS_FLUXES["Atmosphere"] = {'cols':["Impacts", "CometDelivery"],
                              'ylabel':"Nitrogen flux [kg N/yr]", 'isLog':True}

PLOTS_FLUXES["Oceans1"] = {'cols':["FreundlichAdsorption", "HydrothermalCirculation"],
                           'ylabel':"Nitrogen flux [kg N/yr]", 'isLog':True}

PLOTS_FLUXES["Oceans2"] = {'cols':["AbioticFixation", "Henry"],
                           'ylabel':"Nitrogen flux [kg N/yr]"}

PLOTS_FLUXES["Interior"] = {'cols':["Subduction", "Convection", "Volcanism"],
                            'ylabel':"Nitrogen flux [kg N/yr]", 'isLog':True}

# TODO: norms should match that in generate_heatmap

PLOTS_EVO = OrderedDict()
PLOTS_EVO["Atmosphere"] = {'cols':["Atmosphere0"],
                           'ylabel':"Nitrogen content [PAL]",
                           'norm':[4e18]}

PLOTS_EVO["Oceans"] = {'cols':["Oceans0", "Oceans1", "Oceans2"],
                       'ylabel':"Nitrogen content [mmol/L]",
                       'norm':[1.8e16], 'isLog':True}

PLOTS_EVO["Crust"] = {'cols':["OCrust2"],
                      'ylabel':"Nitrogen content [ppm]",
                      'norm':[1.0e15], 'isLog':True}

PLOTS_EVO["Mantle"] = {'cols':["UMantle2", "LMantle2"],
                       'ylabel':"Nitrogen content [ppm]",
                       'norm':[8.2e17, 2.2e18], 'isLog':True}

if ARGS.id:
    r = Report(ARGS.id, sim_dir=ARGS.folder)

    r.add_subplot(PLOTS_FLUXES)
    r.add_subplot(PLOTS_EVO)

    r.process()
    r.to_file()
else:
    OUTPUT = glob(ARGS.folder+"/*.txt")
    for out in OUTPUT:
        file_id = out.split("out_")[-1]
        file_id = file_id.split(".txt")[0]

        r = Report(file_id, sim_dir=ARGS.folder)

        r.add_subplot(PLOTS_FLUXES)
        r.add_subplot(PLOTS_EVO)

        r.process()
        r.to_file(with_graph=False)
