'''
Module to generate a series of initial conditions in a given folder. If
varchange is set (optional), oxidizing is set to varchange/100.
'''

import random
import yaml
import os
import sys
import argparse
import numpy as np
from copy import deepcopy

TOTAL_BUDGET = 339 # 1e17 kg

MAP = {0: ["Atmosphere", 0],
       1: ["Oceans", 0],
       2: ["Oceans", 1],
       3: ["Oceans", 2],
       4: ["OCrust", 2],
       5: ["UMantle", 2],
       6: ["LMantle", 2],
       7: ["CCrust", 2]}

METHODS = {}
METHODS['man-ox'] = {'name':{'man_ox':0}, 'scale':1}
METHODS['atm-ox'] = {'name':{'atm_ox':0}, 'scale':1}
METHODS['man-mix'] = {'name':{"Convection": {"F0":0, "F1":0}}, 'scale':1}
METHODS['oce-mix'] = {'name':{"HydrothermalCirculation": {"F0":0, "F1":0}}, 'scale':1}
METHODS['subrate'] = {'name':{"Subduction": {"tau":100e6}}, 'scale':1}
METHODS['biotic'] = {'name':{"BioticContribution": {"E6i":0}}, 'scale':1}
METHODS['ocvol'] = {'name':{"Henry": {"change":1}}, 'scale':0.01}

def get_random_sequence():
    '''Generate a sequence of 8 integers which sum is TOTAL_BUDGET. The way to
       do this is to generate 7 random integers, add 0 and 20 to the list, order
       them and take the differences. The reason this works is that it
       corresponds to taking a rope and cutting it an random places and putting
       it back together.'''

    random.seed()
    reservoirs = []
    while len(reservoirs) < 7: # we want 7 numbers
        reservoirs.append(random.randint(0, TOTAL_BUDGET))

    reservoirs.append(0)
    reservoirs.append(TOTAL_BUDGET)
    reservoirs = sorted(reservoirs)

    return np.diff(reservoirs)

def get_constrained_sequence(d):
    '''Generate a sequence of 8 integers which sum is TOTAL_BUDGET, under constraints from
    d, a dict which is for instance {0:5, 3:4}.'''

    d_ = deepcopy(d)
    
    constrained = len(d_.keys())
    if constrained == 8:
        return list(d_.values())

    sum_constrained = sum(list(d_.values()))
    reservoirs = []
    while len(reservoirs) < 7 - constrained:
        reservoirs.append(random.randint(0, TOTAL_BUDGET-sum_constrained))

    reservoirs.append(0)
    reservoirs.append(TOTAL_BUDGET-sum_constrained)
    reservoirs = sorted(reservoirs)
    reservoirs = list(np.diff(reservoirs))

    for i in range(8):
        if i not in d_.keys():
            d_[i] = reservoirs.pop()

    return list(d_.values())

def get_default_config(fname):
    '''Read config.yaml from main directory to be used as default.'''
    stream = open(fname, "r")
    config = yaml.load(stream)
    stream.close()

    return config

def create_config(folder, varchange, method, fname, constraints={}):
    '''Generate the new configuration based of the default config and the random
       sequence.'''
    cfg = get_default_config(fname)
    random_seq = get_random_sequence()

    if len(constraints.keys()) != 0:
        random_seq = get_constrained_sequence(constraints)

    for res, val in enumerate(random_seq):
        cfg["Reservoirs"][MAP[res][0]]["InitMasses"][MAP[res][1]] = "%.1e" % (val*1e17)
    cfg["OutFolder"] = folder

    parameters = deepcopy(METHODS[method]['name'])
    scale = METHODS[method]['scale']

    plist = ''
    for i in parameters.keys():
        if type(parameters[i]) is dict:
            if len(varchange) != len(parameters[i].keys()):
                print("provide multiple values")
                sys.exit()
            for j,k in enumerate(sorted(parameters[i].keys())):
                parameters[i][k] = '%.2e' % (float(varchange[j])*scale)
                plist += '_'+k+'_'+varchange[j]
            for k in cfg[i].keys():
                if k not in parameters[i].keys():
                    parameters[i][k] = cfg[i][k]
        else:
            parameters[i] = float(varchange[0])*scale
            plist += '_'+i+'_'+varchange[0]
        cfg.update(parameters)

    fname = "config"
    if constraints:
        fname += plist
    else:
        for val in random_seq:
            fname += "_" + str(val)

    fullname = os.getcwd()+"/"+ARGS.folder+"/"+fname+".yaml"
    if os.path.isfile(fullname):
        print("%s already exists" % fullname)
        return

    stream = open(folder+"/"+fname+".yaml", "w")
    yaml.dump(cfg, stream, default_flow_style=True)

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-n', '--num', default=1, type=int,
                        help='number of config to generate')
    PARSER.add_argument('-f', '--folder', default='output')
    PARSER.add_argument('-v', '--varchange', action='append', type=str, default=[])
    PARSER.add_argument('-m', '--method', type=str, required=True)
    PARSER.add_argument('-c', '--config', default="config.yaml", help="base config", type=str)

    ARGS = PARSER.parse_args()

    if not os.path.isdir(ARGS.folder):
        os.mkdir(ARGS.folder)

    constraints = {}
    for i in range(ARGS.num):
        create_config(ARGS.folder, ARGS.varchange, ARGS.method, ARGS.config, constraints=constraints)
