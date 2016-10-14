'''
Module to generate a series of initial conditions in a given folder. If
varchange is set (optional), oxidizing is set to varchange/100.
'''

import random
import yaml
import os
import argparse
import numpy as np

MAP = {0: ["Atmosphere", 0],
       1: ["Oceans", 0],
       2: ["Oceans", 1],
       3: ["Oceans", 2],
       4: ["OCrust", 2],
       5: ["UMantle", 2],
       6: ["LMantle", 2]}

def get_random_sequence():
    '''Generate a sequence of 7 integers which sum is 20. The way to do this is
       to generate 6 random integers, add 0 and 20 to the list, order them and
       take the differences. The reason this works is that it corresponds to
       taking a rope and cutting it an random places and putting it back
       together.'''

    random.seed()
    reservoirs = []
    while len(reservoirs) < 6: # we want 6 numbers
        reservoirs.append(random.randint(0, 20))

    reservoirs.append(0)
    reservoirs.append(20)
    reservoirs = sorted(reservoirs)

    return np.diff(reservoirs)

def get_default_config():
    '''Read config.yaml from main directory to be used as default.'''
    stream = open("config.yaml", "r")
    config = yaml.load(stream)
    stream.close()

    return config


def create_config(folder, varchange):
    '''Generate the new configuration based of the default config and the random
       sequence.'''
    cfg = get_default_config()
    random_seq = get_random_sequence()

    for res, val in enumerate(random_seq):
        cfg["Reservoirs"][MAP[res][0]]["InitMasses"][MAP[res][1]] = "%.1e" % (val*1e18)
    cfg["OutFolder"] = folder

    if varchange != '':
        varchange = float(varchange)/100
        cfg["man_ox"] = varchange

    fname = "config"
    for val in random_seq:
        fname += "_" + str(val)

    fullname = os.getcwd()+"/"+ARGS.folder+"/"+fname+".yaml"
    print(fullname)
    if os.path.isfile(fullname):
        create_config(folder, varchange)

    stream = open(folder+"/"+fname+".yaml", "w")
    yaml.dump(cfg, stream, default_flow_style=True)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-n', '--num', default=1, type=int,
                        help='number of config to generate')
    PARSER.add_argument('-f', '--folder', default='output')
    PARSER.add_argument('-v', '--varchange', type=str, default='')
    ARGS = PARSER.parse_args()

    print(ARGS.folder)
    if not os.path.isdir(ARGS.folder):
        os.mkdir(ARGS.folder)

    for i in range(ARGS.num):
        create_config(ARGS.folder, ARGS.varchange)
