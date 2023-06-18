#!/bin/bash
#Launch /home/safronov/Projects/UDACHA/scripts/Cleaning after use !!!!!!!!!!!!!!!!!!!!!!!!

filtered_path='/home/safronov/Projects/UDACHA/raw_data/merged_vcfs/dnase/'
tmp='/home/safronov/Projects/UDACHA/raw_data/tmp/'

rm $tmp/merge_dnase.txt
for i in /home/abramov/AlignmentsDnase/*.vcf; do
    base=$(basename $i)
    exp_name=${base%.*}
    filtered="$filtered_path$exp_name.vcf.gz"
    
    echo $exp_name > $tmp/rename_dnase.txt
    echo $filtered >> $tmp/merge_dnase.txt
    bcftools reheader --samples $tmp/rename_dnase.txt $i | bcftools view -Oz -o $filtered
    done
    
for i in /home/abramov/AlignmentsDnase/*/*.vcf.gz; do
    base=$(basename $i)
    pref=${base%.*}
    exp_name=${pref%.*}
    filtered="$filtered_path$exp_name.vcf.gz"
     
    echo $exp_name > $tmp/rename_dnase.txt
    echo $filtered >> $tmp/merge_dnase.txt
    bcftools view $i | bcftools reheader --samples $tmp/rename_dnase.txt | bcftools norm -m- -c x | bcftools view --threads 10 -Oz -o $filtered
    done
    
for i in $filtered_path/*.vcf.gz; do
    bcftools index $i
    done
    
#    bcftools merge -l $tmp/merge_dnase.txt -Oz -o /home/safronov/Projects/UDACHA/raw_data/merged_vcfs/merged_dnase.vcf.gz

#    rm $filtered_path/*
    rm $tmp/rename_dnase.txt