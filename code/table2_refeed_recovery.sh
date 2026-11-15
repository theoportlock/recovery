#!/bin/bash

source env.sh

rm -rf $WORK/table2
mkdir -p $WORK/table2/work/{selected,formatted,descriptive}

onehot.py \
	$WORK/filtered/recovery_status.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o $WORK/table2/work/formatted/recovery_status_oh.tsv

select_features.py \
	$WORK/filtered/surveillance.tsv \
	-c 'days_of_catchup,fail_no.failure' \
	-o $WORK/table2/work/formatted/surveillance.tsv

select_features.py \
	$WORK/filtered/covmeta_MAM.tsv \
	-c 'Feed' \
	-o $WORK/table2/work/selected/meta_MAM.tsv

onehot.py \
	$WORK/table2/work/selected/meta_MAM.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o $WORK/table2/work/formatted/meta_MAM_oh.tsv

for file in $WORK/table2/work/formatted/{meta_MAM_oh,recovery_status_oh,surveillance}.tsv; do
    descriptive.py \
        -i "$file" \
        --meta $WORK/filtered/meta.tsv \
        -g 'Feed' \
        -o "$WORK/table2/work/descriptive/$(basename "$file")"
done

merge.py \
	$WORK/table2/work/descriptive/recovery_status_oh.tsv \
	$WORK/table2/work/descriptive/surveillance_fixed.tsv \
	-a \
	--add-filename \
	--filename-format base \
	-o $WORK/table2/work/merged.tsv

# Stats
merge.py \
	$WORK/table2/work/formatted/recovery_status_oh.tsv \
	$WORK/table2/work/formatted/meta_MAM_oh.tsv \
	$WORK/table2/work/formatted/surveillance.tsv \
	-o $WORK/table2/work/data_merged.tsv

descriptive_stats.sh \
	$WORK/table2/work/data_merged.tsv \
	$WORK/table2/work/MAM_recovery_stats

filter.py \
	$WORK/table2/work/MAM_recovery_stats/merged_stats.tsv \
	-q 'source == "Feed, ERUSF (B)"' \
	-o $WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv

select_features.py \
	$WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv \
	-c 'target,p_value' \
	--drop-index \
	-o $WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv

merge.py \
	$WORK/table1/work/merged.tsv \
	$WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o $WORK/table2/work/merged_stats.tsv


# Merge
# Fix formatting
rename_regex.py \
	$WORK/table2/work/descriptive/surveillance.tsv \
	--match 77 --replace 79 \
	--output $WORK/table2/work/descriptive/surveillance_fixed.tsv
rename_regex.py \
	$WORK/table2/work/descriptive/surveillance_fixed.tsv \
	--match 74 --replace 80 \
	--output $WORK/table2/work/descriptive/surveillance_fixed.tsv

merge.py \
	$WORK/table2/work/merged.tsv \
	$WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o $WORK/table2/work/merged_stats.tsv
