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

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder', default='output') 
args = parser.parse_args()

config = glob(args.folder+"/*.yaml")
print(config)

def worker(s, conf):
    name = threading.currentThread().getName()
    logging.debug("Worker %02d waiting to join the pool" % int(name))
    with s:
        subprocess.call(["./evolve", conf], stdout=FNULL)

s = threading.Semaphore(4)
for i, conf in enumerate(config):
    print(conf)
    t = threading.Thread(target=worker, name=str(i), args=(s, conf,))
    time.sleep(0.2)
    t.start()
