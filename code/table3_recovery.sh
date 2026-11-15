#!/bin/bash

source env.sh
set -e

rm -rf $WORK/table3
mkdir -p $WORK/table3/work/{selected,formatted,descriptive}

select_features.py \
	$WORK/filtered/recovery_status_1sd.tsv \
	-c Recovered \
	-o $WORK/table3/work/recovery.tsv

onehot.py \
	$WORK/table3/work/recovery.tsv \
	--dtype bool \
	-o $WORK/table3/work/formatted/recovery.tsv

for file in $WORK/characteristics/work/formatted/{Demographics,Parental_Education_and_Economics,Family_Structure,Household_characteristics,Other}.tsv; do
    descriptive.py \
        -i "$file" \
        --meta $WORK/table3/work/recovery.tsv \
        -g 'Recovered' \
        -o "$WORK/table3/work/descriptive/$(basename "$file")"
done

merge.py \
	$WORK/table3/work/descriptive/* \
	-a \
	--add-filename \
	--filename-format base \
	-o $WORK/table3/work/merged.tsv

# For the stats
merge.py \
	$WORK/characteristics/work/MAM_data_merged.tsv \
	$WORK/table3/work/formatted/recovery.tsv \
	-o $WORK/table3/work/MAM_data_merged_recovery.tsv

descriptive_stats.sh \
	$WORK/table3/work/MAM_data_merged_recovery.tsv \
	$WORK/table3/work/MAM_recovery_stats
	
#filter.py \
#	$WORK/table3/work/MAM_recovery_stats/merged_stats.tsv \
#	-q 'source == "Recovered.Recovered"' \
#	--drop \
#	-o $WORK/table3/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv
filter.py \
	$WORK/table3/work/MAM_recovery_stats/merged_stats.tsv \
	-q 'source == "Recovered.Recovered"' \
	-o $WORK/table3/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv
	
select_features.py \
	$WORK/table3/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv \
	-c 'target,p_value' \
	--drop-index \
	-o $WORK/table3/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv

# Merge
merge.py \
	$WORK/table3/work/merged.tsv \
	$WORK/table3/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o $WORK/table3/work/merged_stats.tsv
