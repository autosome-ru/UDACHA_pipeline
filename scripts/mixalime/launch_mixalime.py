import os
import pandas as pd 
import re
import os
import json
import subprocess
from tqdm.notebook import tqdm
import shutil
import multiprocessing
import sys

def make_stop_list(mode):
    with open(f'/home/safronov/Projects/UDACHA/meta_info/advanced_badgroups/badmaps_dict_gse_corrrected_{mode}.json', "r") as read_file:
        badgroups = json.load(read_file)
    snps_dct = {}
    for f in os.listdir(f'../../raw_data/filtered_vcfs/{mode}/'):
        num_lines = sum(1 for line in open(f'../../raw_data/filtered_vcfs/{mode}/{f}', 'r'))
        snps_dct[f[:-4]] = num_lines

    snps_badgroups = {}
    for key, value in badgroups.items():
        snps_badgroups[key] = sum(snps_dct[x] for x in value)

    bad = []
    good = []
    for key, value in snps_badgroups.items():
        if value < 1000:
            bad += badgroups[key]
        else:
            good += badgroups[key]
    print(len(good))
    return bad

def launch_mixalime(combfile):       
    path = f'../../raw_data/mapped/{mode}/'
    tmp = f'../../raw_data/tmp/mixalime_v3/{mode}_{fit}/{combfile[:-8]}'
    out_path = f'../../pval_tables/{mode}_{fit}/'
          
    subprocess.run([f'mixalime create {tmp} /home/safronov/Projects/UDACHA/scripts/Validation/{mode}/{combfile} --no-snp-bad-check > ../../meta_info/Mixalime_logs/create_{params_name}.txt 2> ../../meta_info/Mixalime_logs/create_err_{params_name}.txt'], shell=True)
    subprocess.run([f'mixalime test --fit {fitpath}.fit.lzma {tmp} --correction single > ../../meta_info/Mixalime_logs/test_{params_name}.txt 2> ../../meta_info/Mixalime_logs/test_err_{params_name}.txt'], shell=True)
    subprocess.run([f'mixalime combine {tmp} > ../../meta_info/Mixalime_logs/comball_{params_name}.txt 2> ../../meta_info/Mixalime_logs/comball_err_{params_name}.txt'], shell=True)
    subprocess.run([f'mixalime export all {tmp} {out_path}{combfile[:-8]} > ../../meta_info/Mixalime_logs/export_{params_name}.txt 2> ../../meta_info/Mixalime_logs/export_err_{params_name}.txt'], shell=True)

fits = ['MCNB','BetaNB']

mode = sys.argv[1]
with open(f'/home/safronov/Projects/UDACHA/meta_info/advanced_badgroups/badmaps_dict_gse_corrrected_{mode}.json', "r") as read_file:
    badgroups = json.load(read_file)
for fit in fits:
    fitpath = f'../../raw_data/tmp/mixalime_v3/fit_{mode}_{fit}'   
    path = f'/home/safronov/Projects/UDACHA/raw_data/mapped/{mode}/'   
    fit_comm = f'mixalime fit --n-jobs 10 {fitpath} {fit}'

    stop_list = make_stop_list(mode)
    params_name = f'mixalime_v3_{mode}'

    comblist = []
    for f in os.listdir(f'../Validation/{mode}'):
        if ('combine' in f) and (os.stat(f'../Validation/{mode}/{f}').st_size != 0):
            comblist.append(f'{f}')    

    inplist = []
    for key, value in tqdm(badgroups.items()):
        badmap = f'/home/safronov/Projects/UDACHA/raw_data/badmaps/{mode}/{key}'
        if os.path.isfile(badmap) == True:
            for exp in value:
                al = exp.split('/')[-1].split('.')[0]
                mappedfile = path + al + '.mapped'
                if os.path.isfile(mappedfile):               
                    df = pd.read_csv(mappedfile, sep='\t')
                    bias = sum(df['REF_COUNTS'] > df['ALT_COUNTS']) / sum(df['ALT_COUNTS'] > df['REF_COUNTS'])
                    if bias > 0.5 and bias < 1.5 and not (al in stop_list):# and exp in exp.split('_')[0] in bad:   # k562 !!!!
                        inplist.append(mappedfile)

    with open(f'/home/safronov/Projects/UDACHA/raw_data/tmp/{mode}_mixalime.txt', 'w') as f:
        for file in inplist:
            f.write(file + '\n')        
    subprocess.run([f'mixalime create {fitpath} ../../raw_data/tmp/{mode}_mixalime.txt --no-snp-bad-check > ../../meta_info/Mixalime_logs/create_{params_name}.txt 2> ../../meta_info/Mixalime_logs/create_err_{params_name}.txt'], shell=True)
    subprocess.run([fit_comm + f'> ../../meta_info/Mixalime_logs/fit_{params_name}.txt 2> ../../meta_info/Mixalime_logs/fit_err_{params_name}.txt'], shell=True)
    if not os.path.isdir(f'../../raw_data/tmp/mixalime_v3/{mode}_{fit}'):
        os.mkdir(f'../../raw_data/tmp/mixalime_v3/{mode}_{fit}')

    with multiprocessing.Pool(30) as p:
            p.map(launch_mixalime, comblist)
            p.close()
            p.join()
