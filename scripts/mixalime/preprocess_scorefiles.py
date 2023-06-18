from collections import defaultdict
from tqdm import tqdm
import datatable as dt
import numpy as np
import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--out', type=str, default='fit')
parser.add_argument('-f', '--file', type=str, default=str())
parser.add_argument('-I','--inputs', type=str, nargs='+', action='append')
parser = parser.parse_args()
assert parser.out or parser.inputs
print(parser)
ptrn = re.compile(r'(?<!\-)([\w+\.\/]+)\s*')



if parser.file:
    with open(parser.file, 'r') as f:
        files = ptrn.findall(f.read())
else:
    files_tmp = parser.inputs
    files = list()
    for fs in files_tmp:
        if type(fs) is list:
            for f in fs:
                files.append(f)

print(files)
counts = defaultdict(lambda: defaultdict(int))

for file in tqdm(files):
    df = dt.fread(file)[:, ['REF_COUNTS', 'ALT_COUNTS', 'BAD']]
    for bad in np.unique(df['BAD'].to_numpy().flatten().astype(float)):
        bad_name = f'BAD{bad:.2f}'
        for t in df[dt.f.BAD == bad, df.names[:-1]].to_tuples():
            counts[bad_name][t] += 1

for bad, cnt in counts.items():
    folder = os.path.join(parser.out, bad)
    os.makedirs(folder, exist_ok=True)
    lt = list()
    for t in sorted(cnt):
        lt.append(list(t) + [cnt[t]])
    np.savetxt(os.path.join(folder, 'stats.tsv'), np.array(lt), delimiter='\t', fmt='%i')