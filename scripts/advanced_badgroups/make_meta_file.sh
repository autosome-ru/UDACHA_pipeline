#!/bin/bash

filtered_path='/home/safronov/Projects/UDACHA/raw_data/merged_vcfs/atac/'
tmp='/home/safronov/Projects/UDACHA/raw_data/tmp'

for i in /home/abramov/AlignmentsAtac/*/*.vcf.gz; do
    base=$(basename $i)
    pref=${base%.*}
    exp_name=${pref%.*}
    filtered="$filtered_path$exp_name.vcf.gz"
    
    echo $exp_name > $tmp/rename_atac.txt
    echo $exp_name >> $tmp/meta_atac.txt
    done