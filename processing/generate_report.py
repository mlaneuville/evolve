from Report import *

r = Report("")

r.add_timeseries("Impacts", ylabel="Production flux [kg N/yr]", isLog=True)
r.add_timeseries("AbioticFixation",  ylabel="Production flux [kg N/yr]", isLog=True)

r.add_timeseries("Test", ["Oceans1", "UMantle2", "Atmosphere0"],  
                 ylabel="Nitrogen content [kg N]", isLog=True)

r.process()
r.to_file()
