#!/bin/bash

badgroup=$1
bed_files=($2)
mode=$3
n_proc=$4

tmp="/home/safronov/Projects/UDACHA/raw_data/tmp/babachi/${mode}_combined_${n_proc}.bed"
tmp2="/home/safronov/Projects/UDACHA/raw_data/tmp/babachi/${mode}_combined_sorted_${n_proc}.bed"
echo -e '#chr\tstart\tend\tid\tref\talt\tref_count\talt_count\tsample_id' > $tmp
for i in "${bed_files[@]}"; do
    grep -E 'rs' $i >> $tmp
done

~/tools/bedops/sort-bed $tmp > $tmp2
babachi $tmp2 -O "/home/safronov/Projects/UDACHA/raw_data/badmaps/$mode/$badgroup" --states "1,4/3,3/2,2,5/2,3,4,5,6" -p geometric -g 0.98
rm $tmp
rm $tmp2