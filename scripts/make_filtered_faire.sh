#!/bin/bash

filtered_path='/home/safronov/Projects/UDACHA/raw_data/filtered_vcfs/faire/'
tmp0='/home/safronov/Projects/UDACHA/raw_data/tmp/tmp0mff.vcf'
tmp='/home/safronov/Projects/UDACHA/raw_data/tmp/tmpmff.vcf'

for i in /home/abramov/AlignmentsFaire/*.vcf; do
    base=$(basename $i)
    pref=${base%.*}
    exp_name=${pref%.*}
    filtered="$filtered_path$exp_name.bed"
    grep -E 'rs|#' $i > $tmp
    babachi filter $tmp -O $filtered
    done