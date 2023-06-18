import requests
import json
import pandas as pd
import os
import string
import numpy as np


master_list_header = '#EXP	TF_UNIPROT_ID	ANTIBODY	TREATMENT	SPECIE	CELL_ID	CELLS	EXP_TYPE	CONTROL	' \
                     'READS	ALIGNS	PEAKS	GEO	ENCODE	WG_ENCODE	READS_ALIGNED	DOWNLOAD_PATH	TF_UNIPROT_ID'

dtype_dict = {name: str if name != 'READS_ALIGNED' else np.float_ for name in master_list_header.split('\t')}


def find_lab(enc):
    r = requests.get('https://www.encodeproject.org/experiments/{}/?format=json'.format(enc))
    lab = json.loads(r.text)['lab']['@id']
    biosample = json.loads(r.text)['replicates'][0]['library']['biosample']['@id']
    ret = lab + "_" + biosample
    return remove_punctuation(ret)


def add_to_dict(d, key, value):
    el = d.get(key, None)
    if el:
        d[key] = el | {value}
    else:
        d[key] = {value}


def add_record(d, row, exp_type):
    path = create_path_from_master_list_df(row, exp_type=exp_type)
    if not pd.isna(row['ENCODE']):
        Lab = find_lab(row['ENCODE'])
        if Lab:
            key = '{}@{}'.format(row['CELLS'], Lab)
            add_to_dict(d, key, path)
            return
        else:
            raise AssertionError('Lab not found')
    elif not pd.isna(row['GEO']):
        key = '{}@{}'.format(row['CELLS'], row['GEO'])
        add_to_dict(d, key, path)
        return
    elif not pd.isna(row['WG_ENCODE']):
        key = '{}@{}'.format(row['CELLS'], row['WG_ENCODE'])
        add_to_dict(d, key, path)
        return
    raise AssertionError('{} has no ENCODE ID, GEO GSE and wgEncode id'.format(row['#EXP']))
    
def remove_punctuation(x):
    table = str.maketrans({key: "_" for key in string.punctuation if key not in {'-', '+'}})
    return x.translate(table).replace(" ", "_")

def create_path_from_master_list_df(row, exp_type):
    exp = row['#EXP']
    align = row['ALIGNS']
    if exp_type == 'atac':
        return f'/home/abramov/AlignmentsAtac/{exp}/{align}.vcf.gz'
    elif exp_type == 'dnase':
        return row['path']
    elif exp_type == 'faire':
        return f'/home/abramov/AlignmentsFaire/{align}.vcf'

def dnase_master(master_list):
    dnase_path = pd.read_csv('/home/abramov/dnase_vcfs.tsv', sep='\t')
    dnase_path.index = dnase_path['#EXP'] + dnase_path['ALIGNS']
    dnase_path.dropna(inplace=True)
    
    master = pd.read_table(master_list, dtype=dtype_dict)
    master.index = master['#EXP'] + master['ALIGNS']
    master = master.loc[dnase_path.index] 
    master['path'] = dnase_path['VCF']
    master.index = range(len(master))
    return master

def make_dict(master_list, exp_type):      
    if exp_type == 'dnase':
        master = dnase_master(master_list)
    else:
        master = pd.read_table(master_list, dtype=dtype_dict)
        
    master['CELLS'] = master['CELLS'].apply(remove_punctuation)
    list_len = len(master.index)
    d = {}
    for index, row in master.iterrows():
        if list_len > 10 and index % (list_len // 10) == 0:
            print("Made {} Experiments out of {}".format(index, list_len))
        add_record(d, row, exp_type)

    print("Saving Dictionary")
    for key in d:
        value = d[key]
        sorted_value = sorted(list(value))
        d[key] = sorted_value
    with open(f'/home/safronov/Projects/UDACHA/meta_info/badmaps_dicts/badmaps_dict_{exp_type}.json', "w") as write_file:
        json.dump(d, write_file)
    print("Dictionary Saved")

make_dict('/home/abramov/Configs/master-atac.txt', 'atac')
make_dict('/home/abramov/Configs/master-faire.tsv', 'faire')
make_dict('/home/safronov/Projects/UDACHA/meta_info/master-dnase_corrected.txt', 'dnase')