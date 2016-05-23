from Report import *

r = Report("")

r.add_timeseries("Impacts", ylabel="Production flux [kg N/yr]", isLog=True)
r.add_timeseries("AbioticFixation",  ylabel="Production flux [kg N/yr]", isLog=True)

r.add_timeseries("Test", ["Impacts", "AbioticFixation"],  
                 ylabel="Production flux [kg N/yr]", isLog=True)

r.process()
r.to_file()
