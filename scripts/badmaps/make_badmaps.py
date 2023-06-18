import re
import os
import json
import subprocess
import multiprocessing
import time
from itertools import islice
import sys

def launch_babachi(key, value):
    n_proc = multiprocessing.current_process().name
    print(multiprocessing.current_process().name)
    bed_list = []
    for exp in value:
        bed_file = path + exp.split('/')[-1].split('.')[0] + '.bed'
        bed_list.append(bed_file)   
    babachi_inp = ' '.join(bed_list)
    print(key, babachi_inp, mode, n_proc)
    result = subprocess.run([f"/home/safronov/Projects/UDACHA/scripts/badmaps/get_BAD.sh {key} '{babachi_inp}' {mode} {n_proc}"], shell=True)
    
if __name__ == '__main__':
    
    mode = sys.argv[1]
    with open(f'/home/safronov/Projects/UDACHA/meta_info/advanced_badgroups/badmaps_dict_{mode}.json', "r") as read_file:
        badgroups = json.load(read_file)
    path = f'/home/safronov/Projects/UDACHA/raw_data/filtered_vcfs/{mode}/'

    start = time.time()
    args = []
    
    with multiprocessing.Pool(20) as p:
        p.starmap(launch_babachi, badgroups.items())
        p.close()
        p.join()

    end = time.time()