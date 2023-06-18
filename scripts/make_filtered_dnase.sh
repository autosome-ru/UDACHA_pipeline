#!/bin/bash

filtered_path='/home/safronov/Projects/UDACHA/raw_data/filtered_vcfs/dnase/'
tmp0='/home/safronov/Projects/UDACHA/raw_data/tmp/tmp0mfd.vcf'
tmp='/home/safronov/Projects/UDACHA/raw_data/tmp/tmpmfd.vcf'

for i in /home/abramov/AlignmentsDnase/*.vcf; do
    base=$(basename $i)
    exp_name=${base%.*}
    filtered="$filtered_path$exp_name.bed"
    echo $i
    grep -E 'rs|#' $i > $tmp
    babachi filter $tmp -O $filtered
    done
    
for i in /home/abramov/AlignmentsDnase/*/*.vcf.gz; do
    base=$(basename $i)
    pref=${base%.*}
    exp_name=${pref%.*}
    filtered="$filtered_path$exp_name.bed"
    gunzip -c $i > $tmp0
    grep -E 'rs|#' $tmp0 > $tmp
    babachi filter $tmp -O $filtered
    done