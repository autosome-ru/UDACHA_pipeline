import os 
import subprocess

mode = 'dnase'
release_name = 'release_IceKing_check'

#Filtering
subprocess.run([f'bash scripts/make_filtered_{mode}.sh'], shell=True)
if mode == 'dnase':
    daligns = [x[:13] for x in os.listdir('raw_data/filtered_vcfs/dnase/')]
    duplicated = [x for x in daligns if daligns.count(x) > 1]
    for dalign in duplicated:
        if os.path.isfile(f'raw_data/filtered_vcfs/dnase/{dalign}.bed'):
            os.remove(f'raw_data/filtered_vcfs/dnase/{dalign}.bed')

#Clustering
subprocess.run([f'bash scripts/advanced_badgroups/fix_sample_names_{mode}.sh'], shell=True)
if mode == 'dnase':
    for dalign in duplicated:
        if os.path.isfile(f'raw_data/merged_vcfs/dnase/{dalign}.vcf'):
            os.remove(f'raw_data/merged_vcfs/dnase/{dalign}.vcf')
            os.remove(f'raw_data/merged_vcfs/dnase/{dalign}.vcf.gz')
            os.remove(f'raw_data/merged_vcfs/dnase/{dalign}.vcf.gz.csi')
    subprocess.run([f'bcftools merge -l raw_data/tmp/merge_dnase.txt -Oz -o raw_data/merged_vcfs/merged_dnase.vcf.gz'], shell=True)
            
subprocess.run([f'bash scripts/advanced_badgroups/plink_clustering.sh {mode}'], shell=True)

#Badgroups
subprocess.run([f'python3 make_initial_dicts.py'], shell=True)
subprocess.run([f'python3 scripts/advanced_badgroups/make_advanced_badgroups.py'], shell=True)
subprocess.run([f'python3 scripts/badmaps/make_badmaps.py {mode}'], shell=True)

#Mixalime
subprocess.run([f'python3 scripts/Validation/make_combfiles.py {mode}'], shell=True)
subprocess.run([f'bash scripts/mixalime/make_release.sh {mode} {release_name}'], shell=True)