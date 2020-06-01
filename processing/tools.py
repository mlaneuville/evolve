import pandas as pd

class Axis:
    def __init__(self, norm, ylabel, earthscale=1):
        self.norm = norm
        self.ylabel = ylabel
        self.earthscale = earthscale

class Parameters:
    # TODO: define a default set of values when an unknown category is accessed
    def __init__(self):
        PARAMS = {}
        PARAMS['default'] = Axis(1, 'undefined axis')

        PARAMS['Atmosphere0'] = Axis(4e18, 'pN$_2$ [PAL]')
        PARAMS['Oceans0'] = Axis(3.8e16, 'N content [mM]', earthscale=0.63)
        PARAMS['Oceans1'] = Axis(5.1e16, 'NO$_x$ [mM]', earthscale=1e-2)
        PARAMS['Oceans2'] = Axis(2.4e16, 'NH$_x$ [mM]', earthscale=3e-4)
        PARAMS['LMantle2'] = Axis(2.5e18, 'NH$_x$ [ppm]', earthscale=1.4)
        PARAMS['UMantle2'] = Axis(9.6e17, 'NH$_x$ [ppm]', earthscale=3.5)
        PARAMS['OCrust2'] = Axis(1e15, 'NH$_x$ [ppm]', earthscale=200)
        PARAMS['CCrust2'] = Axis(4e18, 'NH$_x$ [PAL]', earthscale=0.35)

        PARAMS['Volcanism0'] = Axis(1, 'Volcanic flux as N$_2$ [kg/yr]', earthscale=1)
        PARAMS['Volcanism1'] = Axis(1, 'Volcanic flux as NH$_x$ [kg/yr]', earthscale=1)
        PARAMS['Volcanism2'] = Axis(1, 'Volcanic flux as NH$_x$ [kg/yr]', earthscale=1)
        PARAMS['Subduction0'] = Axis(1, 'Subduction flux as NH$_x$ [kg/yr]', earthscale=1)
        PARAMS['Convection0'] = Axis(1, 'Convection flux as NH$_x$ [kg/yr]', earthscale=1)
        PARAMS['Henry0'] = Axis(1, 'Ocean-Atmosphere equilibration flux [kg/yr]', earthscale=1)
        PARAMS['AbioticFixation0'] = Axis(1, 'Abiotic fixation to NO$_x$ [kg/yr]', earthscale=1)
        PARAMS['AbioticFixation1'] = Axis(1, 'Abiotic fixation to NH$_x$ [kg/yr]', earthscale=1)
        PARAMS['HydrothermalCirculation0'] = Axis(1e10, 'HT. circulation from NO$_x$ [1e10 kg/yr]', earthscale=1)
        PARAMS['HydrothermalCirculation1'] = Axis(1e6, 'HT. circulation from N$_2$ [1e6 kg/yr]', earthscale=1)
        PARAMS['FreundlichAdsorption0'] = Axis(1e10, 'Freundlich adsorption [1e10 kg/yr]', earthscale=1)
        PARAMS['Erosion0'] = Axis(1e10, 'Erosion rate [1e10 kg/yr]', earthscale=1)
        PARAMS['Erosion1'] = Axis(1, 'Relative continental area', earthscale=0.35)

#        PARAMS['Atmosphere2'] = {'norm':1, 'ylabel':'N-content [kg]', 'isLog':True, 'Earth':1e15}
#        PARAMS['BioticContribution0'] = {'norm':1, 'ylabel':'N-content [kg]', 'isLog':True, 'Earth':1}
#        PARAMS['BioticContribution1'] = {'norm':1, 'ylabel':'Synthesis pathway', 'isLog':False, 'Earth':1}
#        PARAMS['BioticContribution2'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':False, 'Earth':1}
#        PARAMS['CometDelivery0'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':True, 'Earth':1}
#        PARAMS['Impacts0'] = {'norm':1, 'ylabel':'Assimil. pathway', 'isLog':True, 'Earth':1}

        self.params = PARAMS

def loadfile(fname, columns, PARAMS, xaxis='time'):
    if type(columns) != list:
        columns = [columns]

    try:
        data = pd.read_csv(fname)
    except:
        data = pd.DataFrame()

    if not sum([x in data.columns for x in columns]):
        print("File doesn't seem to be an output file, skipping", fname)
        return None, None

    xa = data[xaxis].values[1:]
    if xaxis != 'time':
        xa/= PARAMS[columns[0]].norm

    ya = []
    for col in columns:
        y = data[col].values[1:]
        y /= PARAMS[col].norm
        ya.append(y)

    print(fname)
    return xa, ya
