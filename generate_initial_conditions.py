from random import randint, choice
import numpy as np
import yaml
import os
import sys
import argparse

MAP = {0: ["Atmosphere", 0], 
       1: ["Oceans", 0], 
       2: ["Oceans", 1], 
       3: ["Oceans", 2], 
       4: ["OCrust", 2], 
       5: ["UMantle", 2], 
       6: ["LMantle", 2] }

def get_random_sequence():
    res = np.zeros(7, dtype=int)
    test = range(len(res))
    size = 20
    s0 = size
    
    while len(test) >= 1 and size > 0:
        amount = randint(0, size)
        if len(test) == 1:
            amount = size
    
        idx = choice(test)
        res[idx] += amount
        size -= amount
    
    assert sum(res) == s0
    return res 


def get_default_config():
    stream = open("config.yaml", "r")
    config = yaml.load(stream)
    stream.close()

    return config


def create_config(folder):
    cfg = get_default_config()
    random_seq = get_random_sequence()

    for res, val in enumerate(random_seq):
        cfg["Reservoirs"][MAP[res][0]]["InitMasses"][MAP[res][1]] = "%.e" % (val*1e18)
    cfg["OutFolder"] = folder

    fname = "config"
    for val in random_seq:
        fname += "_" + str(val)

    stream = open(folder+"/"+fname+".yaml", "w")
    yaml.dump(cfg, stream, default_flow_style=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', default=1, type=int, 
                        help='number of config to generate') 
    parser.add_argument('-f', '--folder', default='output') 
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        os.mkdir(args.folder)

    for i in range(args.num):
        create_config(args.folder)
