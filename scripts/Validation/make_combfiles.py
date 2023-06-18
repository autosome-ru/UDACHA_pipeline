import string
import sys
import pandas as pd
import os
import subprocess
import json

def get_nsnps_ud(x):
    if os.path.isfile(f'raw_data/mapped/dnase/{x}.mapped'):
        result = subprocess.run([f'wc -l raw_data/mapped/dnase/{x}.mapped'], shell=True, capture_output=True, text=True)        
        return int(result.stdout.split(' ')[0]) - 1
    else:
        return 0

def remove_punctuation(x):
    table = str.maketrans({key: "_" for key in string.punctuation if key not in {'-', '+'}})
    return x.translate(table).replace(" ", "_")

def dnase_master(master_list):
    dnase_path = pd.read_csv('/home/abramov/dnase_vcfs.tsv', sep='\t')
    dnase_path.index = dnase_path['#EXP'] + dnase_path['ALIGNS']
    dnase_path.dropna(inplace=True)
    
    master = pd.read_table(master_list)
    master.index = master['#EXP'] + master['ALIGNS']
    master = master.loc[dnase_path.index] 
    master['path'] = dnase_path['VCF']
    master.index = range(len(master))
    master['ALIGNS'] = master['path'].str.split('/').apply(lambda x : x[-1].split('.')[0])
    return master

def make_stop_list(mode):
    with open(f'/home/safronov/Projects/UDACHA/meta_info/advanced_badgroups/badmaps_dict_gse_corrrected_{mode}.json', "r") as read_file:
        badgroups = json.load(read_file)
    snps_dct = {}
    for f in os.listdir(f'raw_data/filtered_vcfs/{mode}/'):
        num_lines = sum(1 for line in open(f'raw_data/filtered_vcfs/{mode}/{f}', 'r'))
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

mode = sys.argv[1]
if mode == 'dnase':
    master = dnase_master('/home/abramov/Configs/master-dnase.txt')
elif mode == 'atac':
    master = pd.read_csv(f'/home/abramov/Configs/master-{mode}.txt', sep='\t')
elif mode == 'faire':
    master = pd.read_csv(f'/home/abramov/Configs/master-{mode}.tsv', sep='\t')
master['nsnp_udach'] = master['ALIGNS'].apply(get_nsnps_ud)


path = f'/home/safronov/Projects/UDACHA/raw_data/mapped/{mode}/'
combpath = f'/home/safronov/Projects/UDACHA/scripts/Validation/{mode}'
stop_list = make_stop_list(mode)

master['CELLS_COR'] = master['CELLS'].apply(lambda x : remove_punctuation(x)) 

for name in master['CELLS_COR'].unique():
    with open(f'{combpath}/{name}.combine', 'w') as f:
        for align in master[master['CELLS_COR'] == name]['ALIGNS']:
            al = align
            if os.path.isfile(f'{path}{al}.mapped'):               
                df = pd.read_csv(f'{path}{al}.mapped', sep='\t')
                bias = sum(df['REF_COUNTS'] > df['ALT_COUNTS']) / sum(df['ALT_COUNTS'] > df['REF_COUNTS'])
                if bias > 0.5 and bias < 1.5 and not (al in stop_list):
                    f.write(f'{path}{al}.mapped\n')
    if os.stat(f'{combpath}/{name}.combine').st_size == 0:
        os.remove(f'{combpath}/{name}.combine')