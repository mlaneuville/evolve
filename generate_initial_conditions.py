'''
Module to generate a series of initial conditions in a given folder. If
varchange is set (optional), oxidizing is set to varchange/100.
'''

import random
import yaml
import os
import argparse
import numpy as np
from copy import deepcopy

TOTAL_BUDGET = 93 # 1e17 kg

MAP = {0: ["Atmosphere", 0],
       1: ["Oceans", 0],
       2: ["Oceans", 1],
       3: ["Oceans", 2],
       4: ["OCrust", 2],
       5: ["UMantle", 2],
       6: ["LMantle", 2]}

METHODS = {}
METHODS['redox-mantle'] = {'name':{'man_ox':0}, 'scale':0.01}
METHODS['redox-atmosphere'] = {'name':{'atm_ox':0}, 'scale':0.01}
METHODS['comp-conv'] = {'name':{"Convection": {"F0":0, "F1":0}}, 'scale':1e-9}
METHODS['comp-hydro'] = {'name':{"HydrothermalCirculation": {"F0":0, "F1":0}}, 'scale':1e-8}

def get_random_sequence():
    '''Generate a sequence of 7 integers which sum is 20. The way to do this is
       to generate 6 random integers, add 0 and 20 to the list, order them and
       take the differences. The reason this works is that it corresponds to
       taking a rope and cutting it an random places and putting it back
       together.'''

    random.seed()
    reservoirs = []
    while len(reservoirs) < 6: # we want 6 numbers
        reservoirs.append(random.randint(0, TOTAL_BUDGET))

    reservoirs.append(0)
    reservoirs.append(TOTAL_BUDGET)
    reservoirs = sorted(reservoirs)

    return np.diff(reservoirs)

def get_constrained_sequence(d):
    '''Generate a sequence of 7 integers which sum is 20, under constraints from
    d, a dict which is for instance {0:5, 3:4}.'''

    d_ = deepcopy(d)
    random.seed()
    constrained = len(d_.keys())
    if constrained == 7:
        return list(d_.values())

    sum_constrained = sum(list(d_.values()))
    reservoirs = []
    while len(reservoirs) < 6 - constrained:
        reservoirs.append(random.randint(0, TOTAL_BUDGET-sum_constrained))

    reservoirs.append(0)
    reservoirs.append(TOTAL_BUDGET-sum_constrained)
    reservoirs = sorted(reservoirs)
    reservoirs = list(np.diff(reservoirs))

    for i in range(7):
        if i not in d_.keys():
            d_[i] = reservoirs.pop()

    return list(d_.values())

def get_default_config():
    '''Read config.yaml from main directory to be used as default.'''
    stream = open("config.yaml", "r")
    config = yaml.load(stream)
    stream.close()

    return config


def create_config(folder, varchange, method, constraints={}):
    '''Generate the new configuration based of the default config and the random
       sequence.'''
    cfg = get_default_config()
    random_seq = get_random_sequence()

    if len(constraints.keys()) != 0:
        random_seq = get_constrained_sequence(constraints)

    for res, val in enumerate(random_seq):
        cfg["Reservoirs"][MAP[res][0]]["InitMasses"][MAP[res][1]] = "%.1e" % (val*1e17)
    cfg["OutFolder"] = folder

    parameters = deepcopy(METHODS[method]['name'])
    scale = METHODS[method]['scale']

    if varchange != '':
        varchange = float(varchange)*scale
        
        for i in parameters.keys():
            if type(parameters[i]) is dict:
                for k in parameters[i].keys():
                    parameters[i][k] = varchange
                for k in cfg[i].keys():
                    if k not in parameters[i].keys():
                        parameters[i][k] = cfg[i][k]
            else:
                parameters[i] = varchange        
            cfg.update(parameters)

    fname = "config"
    for val in random_seq:
        fname += "_" + str(val)

    fullname = os.getcwd()+"/"+ARGS.folder+"/"+fname+".yaml"
    print(fullname)
    if os.path.isfile(fullname):
        create_config(folder, varchange, method)

    stream = open(folder+"/"+fname+".yaml", "w")
    yaml.dump(cfg, stream, default_flow_style=True)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-n', '--num', default=1, type=int,
                        help='number of config to generate')
    PARSER.add_argument('-f', '--folder', default='output')
    PARSER.add_argument('-v', '--varchange', type=str, default='')
    PARSER.add_argument('-m', '--method', type=str, default='redox-mantle')

    ARGS = PARSER.parse_args()

    print(ARGS.folder)
    if not os.path.isdir(ARGS.folder):
        os.mkdir(ARGS.folder)

    constraints = {}
    for i in range(ARGS.num):
        #constraints[0] = i+1
        #for j in range(20-i):
        #    constraints[6] = max(0, 20-i-j-1)
        create_config(ARGS.folder, ARGS.varchange, ARGS.method)
