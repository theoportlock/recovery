#!/bin/bash

source env.sh

output='results/table2_plus'
rm -rf $output
mkdir -p $output/work/{selected,formatted,descriptive}

onehot.py \
	results/filtered/recovery_status.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o $output/formatted/recovery_status_oh.tsv

select.py \
	results/filtered/surveillance.tsv \
	-c 'days_of_catchup,fail_no.failure' \
	-o $output/formatted/surveillance.tsv

select.py \
	results/filtered/meta_MAM.tsv \
	-c 'Feed' \
	-o $output/selected/meta_MAM.tsv

onehot.py \
	results/table2/work/selected/meta_MAM.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o $output/formatted/meta_MAM_oh.tsv

for file in $output/formatted/{meta_MAM_oh,recovery_status_oh,surveillance}.tsv; do
    descriptive.py \
        -i "$file" \
        --meta results/filtered/meta.tsv \
        -g 'Feed' \
        -o "$output/work/descriptive/$(basename "$file")"
done

merge.py \
	$output/work/descriptive/recovery_status_oh.tsv \
	$output/work/descriptive/surveillance_fixed.tsv \
	-a \
	--add-filename \
	--filename-format base \
	-o $output/merged.tsv

# Stats
merge.py \
	$output/formatted/recovery_status_oh.tsv \
	$output/formatted/meta_MAM_oh.tsv \
	$output/formatted/surveillance.tsv \
	-o $output/data_merged.tsv

descriptive_stats.sh \
	$output/data_merged.tsv \
	$output/MAM_recovery_stats

filter.py \
	$output/MAM_recovery_stats/merged_stats.tsv \
	-q 'source == "Feed, ERUSF (B)"' \
	-o $output/MAM_recovery_stats/merged_stats_Recoverstats.tsv

select.py \
	$output/MAM_recovery_stats/merged_stats_Recoverstats.tsv \
	-c 'target,p_value' \
	--drop-index \
	-o $output/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv

merge.py \
	$output/work/merged.tsv \
	$output/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o $output/merged_stats.tsv


# Merge
# Fix formatting
rename_regex.py \
	$output/descriptive/surveillance.tsv \
	--match 77 --replace 79 \
	--output $output/descriptive/surveillance_fixed.tsv
rename_regex.py \
	$output/descriptive/surveillance_fixed.tsv \
	--match 74 --replace 80 \
	--output $output/descriptive/surveillance_fixed.tsv

merge.py \
	$output/merged.tsv \
	$output/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o $output/merged_stats.tsv
