#!/bin/bash

source env.sh

rm -rf results/table3
mkdir -p results/table3/work/{selected,formatted,descriptive}

select.py \
	results/filtered/recovery_status.tsv \
	-c Recovered \
	-o results/table3/work/recovery.tsv

onehot.py \
	results/table3/work/recovery.tsv \
	--dtype bool \
	-o results/table3/work/formatted/recovery.tsv

for file in results/table1/work/formatted/{Demographics,Parental_Education_and_Economics,Family_Structure,Household_characteristics,Other}.tsv; do
    descriptive.py \
        -i "$file" \
        --meta results/table3/work/recovery.tsv \
        -g 'Recovered' \
        -o "results/table3/work/descriptive/$(basename "$file")"
done

merge.py \
	results/table3/work/descriptive/* \
	-a \
	--add-filename \
	--filename-format base \
	-o results/table3/work/merged.tsv

# For the stats
merge.py \
	results/table1/work/MAM_data_merged.tsv \
	results/table3/work/formatted/recovery.tsv \
	-o results/table3/work/MAM_data_merged_recovery.tsv

descriptive_stats.sh \
	results/table3/work/MAM_data_merged_recovery.tsv \
	results/table3/work/MAM_recovery_stats

filter.py \
	results/table3/work/MAM_recovery_stats/merged_stats.tsv \
	-q 'source == "Recovered.Recovered"' \
	--drop \
	-o results/table3/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv
	
select.py \
	results/table3/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv \
	-c 'target,p_value' \
	--drop-index \
	-o results/table3/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv

# Merge
merge.py \
	results/table3/work/merged.tsv \
	results/table3/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o results/table3/work/merged_stats.tsv
