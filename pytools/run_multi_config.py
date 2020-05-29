'''
Run all yaml files from a given folder if the corresponding out file doesn't
already exist. Four parallel threads are used by default.
'''

from glob import glob
import argparse
import logging
import threading
import os
import time
import subprocess

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s (%(threadName)-2s) %(message)s")

FNULL = open(os.devnull, "w")

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-f', '--folder', default='output')
ARGS = PARSER.parse_args()

to_pop = []
CONFIG = glob(ARGS.folder+"/*.yaml")
for i, yaml in enumerate(CONFIG):
    idx = yaml.split("config_")
    fname = "out_%s.txt" % (idx[1][:-5])
    fullname = os.getcwd()+"/"+ARGS.folder+"/"+fname
    if os.path.isfile(fullname):
        to_pop.append(i)

for i in to_pop[::-1]:
    CONFIG.pop(i)

print(CONFIG)

def worker(sema_, conf_):
    '''Define worker's work.'''
    name = threading.currentThread().getName()
    logging.debug("Worker %02d waiting to join the pool", int(name))
    with sema_:
        logging.debug("%s starting", conf_)
        subprocess.call(["./evolve", conf_], stdout=FNULL)
        logging.debug("%s is done!", conf_)

SEMA = threading.Semaphore(4)
for i, conf in enumerate(CONFIG):
    t = threading.Thread(target=worker, name=str(i), args=(SEMA, conf,))
    time.sleep(0.2)
    t.start()
