import argparse
from curses import meta
import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import json
import sys


def visualize_clustering(mat, linkage, out_path):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(200, 450))
    dendro = hierarchy.dendrogram(linkage, no_plot=False, ax=ax1)
    g = sns.heatmap(mat.iloc[dendro['leaves'],dendro['leaves']], cmap='Blues',
     square=True, xticklabels=False, yticklabels=False, cbar=False, ax=ax2)
    for l in ['left','right','top','bottom']:
        g.spines[l].set_visible(True)
        g.spines[l].set_color('k')
    
    plt.savefig(f"{out_path}.png")
    plt.close(fig)

mode = sys.argv[1]
input_matrix = f'/home/safronov/Projects/UDACHA/raw_data/merged_vcfs/{mode}_snps.clustering.king'
input_matrix_ids = f'/home/safronov/Projects/UDACHA/raw_data/merged_vcfs/{mode}_snps.clustering.king.id'
meta_path = f'/home/safronov/Projects/UDACHA/raw_data/tmp/meta_atac.txt'
outpath = f'/home/safronov/Projects/UDACHA/meta_info/advanced_badgroups/{mode}/'
    
new_meta_path = os.path.join(outpath, "metadata.clustered.tsv") 
indivs = np.loadtxt(input_matrix_ids, skiprows=0, dtype=str)
rel_mat = np.loadtxt(input_matrix)
mat = pd.DataFrame(rel_mat, index=indivs, columns=indivs)

mat[mat < 0.4] = 0
mat[np.isnan(mat)] = 0
linkage = hierarchy.linkage(mat, method='complete', metric='correlation')
cl = hierarchy.fcluster(linkage, 0.1, criterion='distance')
clusters = pd.DataFrame({'indiv_id': mat.index, 'genotype_cluster': cl}).sort_values(
    by='genotype_cluster')

#metadata = pd.read_table(meta_path, header=0, dtype={'indiv_id': str})
#metadata = clusters.sort_values(by='genotype_cluster')
#metadata.rename(columns={'indiv_id': 'old_indiv_id'}, inplace=True)
#metadata.rename(columns={'genotype_cluster': 'indiv_id'}, inplace=True)
#metadata['indiv_id'] = 'INDIV_' + metadata['indiv_id'].astype(str).str.zfill(4)
#metadata.to_csv(new_meta_path, header=True, index=False, sep='\t')
visualizations_path = os.path.join(outpath, 'clustering')
visualize_clustering(mat, linkage, out_path=visualizations_path)
################################################################################
exp_type = mode
d = {}
for x in clusters['genotype_cluster'].unique():
    als = clusters[clusters['genotype_cluster'].isin([x])]['indiv_id'].values
    d[f'cluster{x}'] = als
for key in d:
    value = d[key]
    sorted_value = sorted(list(value))
    d[key] = sorted_value

with open(f'/home/safronov/Projects/UDACHA/meta_info/badmaps_dicts/badmaps_dict_{mode}.json', "r") as read_file:
    bg = json.load(read_file)
revbg = {}
for key, value in bg.items():
    for i in value:
        revbg[i.split('/')[-1].split('.')[0]] = key 

gse_corrected = {}
cnt = 0
for key, value in d.items():
    for i in value:
        try:
            gse_corrected[f'{key}_{revbg[i]}'] = []
        except KeyError:
            print(i)
            cnt+=1
            gse_corrected[f'{key}_NoGSE'] = []

for key, value in d.items():
    for i in value:
        try:
            gse_corrected[f'{key}_{revbg[i]}'].append(i)
        except KeyError:
            print(i)
            cnt+=1
            gse_corrected[f'{key}_NoGSE'].append(i)
with open(f'/home/safronov/Projects/UDACHA/meta_info/advanced_badgroups/badmaps_dict_gse_corrrected_{mode}_check.json', "w") as write_file:
    json.dump(gse_corrected, write_file)