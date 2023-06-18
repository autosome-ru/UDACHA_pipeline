#!/bin/bash

filtered_path='/home/safronov/Projects/UDACHA/raw_data/merged_vcfs/faire/'
tmp='/home/safronov/Projects/UDACHA/raw_data/tmp/'

rm {$tmp}merge_faire.txt
for i in /home/abramov/AlignmentsFaire/*.vcf; do
    base=$(basename $i)
    exp_name=${base%.*}
    filtered="$filtered_path$exp_name.vcf.gz"
    
    echo $exp_name > $tmp/rename_faire.txt
    echo $filtered >> $tmp/merge_faire.txt
    bcftools reheader --samples $tmp/rename_faire.txt $i | bcftools view -Oz -o $filtered
    done
    
for i in $filtered_path/*.vcf.gz; do
    bcftools index $i
    done
    
    bcftools merge -l $tmp/merge_faire.txt -Oz -o /home/safronov/Projects/UDACHA/raw_data/merged_vcfs/merged_faire.vcf.gz

#    rm $filtered_path/*
    rm $tmp/rename_faire.txt