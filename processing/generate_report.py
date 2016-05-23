from Report import *

r = Report("")

r.plot_timeseries("Impacts", ylabel="Production flux [kg N/yr]", isLog=True)
r.plot_timeseries("AbioticFixation", ylabel="Production flux [kg N/yr]", isLog=True)
