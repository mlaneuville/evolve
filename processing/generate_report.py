from Report import *

r = Report("")

r.add_timeseries("Impacts", ylabel="Production flux [kg N/yr]", isLog=True)
r.add_timeseries("AbioticFixation",  ylabel="Production flux [kg N/yr]", isLog=True)

r.add_timeseries("Global evolution", 
                 ["Oceans1", "Oceans2", "LMantle2", "UMantle2", "OCrust2", "Atmosphere0"],  
                 ylabel="Nitrogen content [kg N]", isLog=True, norm=1e21)

r.process()
r.to_file()
