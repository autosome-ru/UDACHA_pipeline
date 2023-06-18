import os
import sys
import subprocess

mode = sys.argv[1]
release_name = sys.argv[2]

brokenpath = f'home/safronov/Projects/UDACHA/raw_data/mapped/{mode}'
raw_path = f'../../{release_name}/raw_{mode}'
if not os.path.isdir(raw_path):
    os.mkdir(raw_path)

for f in os.listdir(f'../Validation/{mode}/'):
    if not os.path.isdir(f'{raw_path}/{f[:-8]}'):
        os.mkdir(f'{raw_path}/{f[:-8]}')

    if sum(1 for line in f'../Validation/{mode}/{f}') >= 50:
        betapath = f'../../pval_tables/{mode}_BetaNB/{f[:-8]}/pvalues/raw'
        if os.path.isdir(f'{betapath}/home'):
            subprocess.run([f'cp -a {betapath}/{brokenpath}/. {raw_path}/{f[:-8]}'], shell=True)
        else:
            subprocess.run([f'cp -a {betapath}/. {raw_path}/{f[:-8]}'], shell=True)

    else:
        mcnbpath = f'../../pval_tables/{mode}_MCNB/{f[:-8]}/pvalues/raw'
        if os.path.isdir(f'{mcnbpath}/home'):
            subprocess.run([f'cp -a {mcnbpath}/{brokenpath}/. {raw_path}/{f[:-8]}'], shell=True)
        else:
            subprocess.run([f'cp -a {mcnbpath}/. {raw_path}/{f[:-8]}'], shell=True)
                