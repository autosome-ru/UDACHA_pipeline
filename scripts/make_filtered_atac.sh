#!/bin/bash

filtered_path='/home/safronov/Projects/UDACHA/raw_data/filtered_vcfs/atac/'
tmp0='/home/safronov/Projects/UDACHA/raw_data/tmp/tmp0mfa.vcf'
tmp='/home/safronov/Projects/UDACHA/raw_data/tmp/tmpmfa.vcf'

for i in /home/abramov/AlignmentsAtac/*/*.vcf.gz; do
    base=$(basename $i)
    pref=${base%.*}
    exp_name=${pref%.*}
    filtered="$filtered_path$exp_name.bed"
    gunzip -c $i > $tmp0
    grep -E 'rs|#' $tmp0 > $tmp
    babachi filter $tmp -O $filtered
    done