#!/bin/bash

filtered_path='/home/safronov/Projects/UDACHA/raw_data/merged_vcfs/atac/'
tmp='/home/safronov/Projects/UDACHA/raw_data/tmp'

rm $tmp/merge_atac.txt
for i in /home/abramov/AlignmentsAtac/*/*.vcf.gz; do
    base=$(basename $i)
    pref=${base%.*}
    exp_name=${pref%.*}
    filtered="$filtered_path$exp_name.vcf.gz"
    
    echo $exp_name > $tmp/rename_atac.txt
    echo $filtered >> $tmp/merge_atac.txt
    bcftools view $i | bcftools reheader --samples $tmp/rename_atac.txt | bcftools norm -m- -c x | bcftools view --threads 10 -Oz -o $filtered
    done
    
for i in $filtered_path/*.vcf.gz; do
    bcftools index $i
    done
    
bcftools merge -l $tmp/merge_atac.txt -Oz -o /home/safronov/Projects/UDACHA/raw_data/merged_vcfs/merged_atac.vcf.gz
#    rm $filtered_path/*
rm $tmp/rename_atac.txt