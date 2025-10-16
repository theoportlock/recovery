#!/bin/bash

source env.sh

rm -rf results/table2
mkdir -p results/table2/work/{selected,formatted,descriptive}

onehot.py \
	results/filtered/recovery_status.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o results/table2/work/formatted/recovery_status_oh.tsv

select.py \
	results/filtered/surveillance.tsv \
	-c 'days_of_catchup,fail_no.failure' \
	-o results/table2/work/formatted/surveillance.tsv

select.py \
	results/filtered/meta_MAM.tsv \
	-c 'Feed' \
	-o results/table2/work/selected/meta_MAM.tsv

onehot.py \
	results/table2/work/selected/meta_MAM.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o results/table2/work/formatted/meta_MAM_oh.tsv

for file in results/table2/work/formatted/{meta_MAM_oh,recovery_status_oh,surveillance}.tsv; do
    descriptive.py \
        -i "$file" \
        --meta results/filtered/meta.tsv \
        -g 'Feed' \
        -o "results/table2/work/descriptive/$(basename "$file")"
done

merge.py \
	results/table2/work/descriptive/recovery_status_oh.tsv \
	results/table2/work/descriptive/surveillance_fixed.tsv \
	-a \
	--add-filename \
	--filename-format base \
	-o results/table2/work/merged.tsv

# Stats
merge.py \
	results/table2/work/formatted/recovery_status_oh.tsv \
	results/table2/work/formatted/meta_MAM_oh.tsv \
	results/table2/work/formatted/surveillance.tsv \
	-o results/table2/work/data_merged.tsv

descriptive_stats.sh \
	results/table2/work/data_merged.tsv \
	results/table2/work/MAM_recovery_stats

filter.py \
	results/table2/work/MAM_recovery_stats/merged_stats.tsv \
	-q 'source == "Feed, ERUSF (B)"' \
	--drop \
	-o results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv
	
select.py \
	results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv \
	-c 'target,p_value' \
	--drop-index \
	-o results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv

merge.py \
	results/table1/work/merged.tsv \
	results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o results/table2/work/merged_stats.tsv


# Merge
# Fix formatting
rename_regex.py \
	results/table2/work/descriptive/surveillance.tsv \
	--match 77 --replace 79 \
	--output results/table2/work/descriptive/surveillance_fixed.tsv
rename_regex.py \
	results/table2/work/descriptive/surveillance_fixed.tsv \
	--match 74 --replace 80 \
	--output results/table2/work/descriptive/surveillance_fixed.tsv

merge.py \
	results/table2/work/merged.tsv \
	results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o results/table2/work/merged_stats.tsv
