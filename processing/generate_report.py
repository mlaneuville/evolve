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
#PLOTS_FLUXES["Atmosphere"] = {'cols':["Impacts0", "CometDelivery0"],
#                              'ylabel':"Nitrogen flux [kg N/yr]", 'isLog':True}

PLOTS_FLUXES["Oceans1"] = {'cols':["FreundlichAdsorption0", "HydrothermalCirculation0"],
                           'ylabel':"Nitrogen flux [kg N/yr]", 'isLog':True}

PLOTS_FLUXES["Oceans2"] = {'cols':["AbioticFixation0", "Henry0"],
                           'ylabel':"Nitrogen flux [kg N/yr]"}

PLOTS_FLUXES["Continent"] = {'cols':["Weathering0", "Subduction1"],
                             'ylabel':"Nitrogen flux [kg N/yr]"}

PLOTS_FLUXES["Interior"] = {'cols':["Subduction0", "Convection0", "Volcanism0"],
                            'ylabel':"Nitrogen flux [kg N/yr]", 'isLog':True}

# TODO: norms should match that in generate_heatmap

PLOTS_EVO = OrderedDict()
PLOTS_EVO["Atmosphere"] = {'cols':["Atmosphere0", "CCrust2"],
                           'ylabel':"Nitrogen content [PAL]", 'isLog':False,
                           'norm':[4e18, 4e18], 'earth':[1, 1]}

PLOTS_EVO["Oceans"] = {'cols':["Oceans0", "Oceans1", "Oceans2"],
#PLOTS_EVO["Oceans"] = {'cols':["Oceans2"],
                       'ylabel':"Nitrogen content [mM]",
                       'norm':[3.8e16, 5.1e16, 2.4e16], 'isLog':True,
                        'earth':[0.63, 1e-2, 3e-4]}

PLOTS_EVO["Crust"] = {'cols':["OCrust2"],
                      'ylabel':"Nitrogen content [ppm]",
                      'norm':[1.0e15], 'isLog':True, 'earth':[200]}

PLOTS_EVO["Mantle"] = {'cols':["UMantle2", "LMantle2"],
                       'ylabel':"Nitrogen content [ppm]",
                       'norm':[9.6e17, 2.5e18], 'isLog':True,
                       'earth':[3.5, 1.4]}

if ARGS.id:
    r = Report(ARGS.id, sim_dir=ARGS.folder)

    r.add_subplot(PLOTS_FLUXES)
    r.add_subplot(PLOTS_EVO)

    r.process()
    r.to_file(with_graph=False)
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
