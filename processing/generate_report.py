import argparse
from Report import *

parser = argparse.ArgumentParser()
parser.add_argument('id', type=str, help='Case ID, useful if there is more than one in folder')

args = parser.parse_args()

r = Report(args.id)

r.add_timeseries("Impacts", ylabel="Production flux [kg N/yr]", isLog=True)
r.add_timeseries("CometDelivery", ylabel="Production flux [kg N/yr]", isLog=True)
r.add_timeseries("AbioticFixation", ylabel="Production flux [kg N/yr]")
r.add_timeseries("Henry", ylabel="Production flux [kg N/yr]")
r.add_timeseries("FreundlichAdsorption", ylabel="Production flux [kg N/yr]")
r.add_timeseries("HydrothermalCirculation", ylabel="Production flux [kg N/yr]")
r.add_timeseries("Subduction", ylabel="Production flux [kg N/yr]")
r.add_timeseries("Convection", ylabel="Production flux [kg N/yr]")
r.add_timeseries("Volcanism", ylabel="Production flux [kg N/yr]")


r.add_timeseries("Atmosphere evolution", ["Atmosphere0"],  
                 ylabel="Nitrogen content [PAL]", norm=[2e19])

r.add_timeseries("Ocean evolution", ["Oceans0", "Oceans1", "Oceans2"],  
                 ylabel="Nitrogen content [umol/L]", isLog=True, norm=[1.8e13])

r.add_timeseries("Crust evolution", ["OCrust2"],  
                 ylabel="Nitrogen content [ppm]", norm=[1.0e15])

r.add_timeseries("Mantle evolution", ["UMantle2", "LMantle2"],  
                  ylabel="Nitrogen content [ppm]", norm=[8.2e17, 2.2e18])

r.process()
r.to_file()
