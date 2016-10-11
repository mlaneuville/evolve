'''
Module to generate a series of initial conditions in a given folder. If
varchange is set (optional), volcanism/oxidizing is set to varchange/100.
'''

from random import randint, choice
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
    '''Generate a sequence of 7 integers which sum is 20.  '''
    res = np.zeros(7, dtype=int)
    test = range(len(res))
    size = 20
    orig_size = size

    while len(test) >= 1 and size > 0:
        amount = randint(0, size)
        if len(test) == 1:
            amount = size

        idx = choice(test)
        res[idx] += amount
        size -= amount

    assert sum(res) == orig_size
    return res


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
        cfg["Volcanism"]["oxidizing"] = varchange

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
