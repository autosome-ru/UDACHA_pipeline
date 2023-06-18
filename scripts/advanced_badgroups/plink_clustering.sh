#!/bin/bash

mode=$1
merged_path='/home/safronov/Projects/UDACHA/raw_data/merged_vcfs/'
outdir='/home/safronov/Projects/UDACHA/meta_info/advanced_badgroups/'
meta_file="/home/safronov/Projects/UDACHA/raw_data/tmp/meta_${mode}.txt"

/home/safronov/tools/plink2 --allow-extra-chr --threads 20 --make-king square --out ${merged_path}${mode}_snps.clustering --vcf ${merged_path}merged_${mode}.vcf.gz