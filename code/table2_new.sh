#!/bin/bash

source env.sh

rm -rf results/table2
mkdir -p results/table2/work/{selected,formatted,descriptive}

# One-hot recovery
onehot.py \
	results/filtered/recovery_status.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o results/table2/work/formatted/recovery_status_oh.tsv

# Surveillance
select_features.py \
	results/filtered/surveillance.tsv \
	-c 'days_of_catchup,fail_no.failure' \
	-o results/table2/work/formatted/surveillance.tsv

# Metadata
select_features.py \
	results/filtered/covmeta_MAM.tsv \
	-c 'Feed' \
	-o results/table2/work/selected/meta_MAM.tsv

onehot.py \
	results/table2/work/selected/meta_MAM.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o results/table2/work/formatted/meta_MAM_oh.tsv


# Fix formatting first
rename_regex.py \
	results/table2/work/formatted/surveillance.tsv \
	--match 77 --replace 79 \
	--output results/table2/work/formatted/surveillance_fixed.tsv

rename_regex.py \
	results/table2/work/formatted/surveillance_fixed.tsv \
	--match 74 --replace 80 \
	--output results/table2/work/formatted/surveillance_fixed.tsv


# Descriptive tables
for file in results/table2/work/formatted/{meta_MAM_oh,recovery_status_oh,surveillance_fixed}.tsv; do
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


# =================
# Stats
# =================

merge.py \
	results/table2/work/formatted/recovery_status_oh.tsv \
	results/table2/work/formatted/meta_MAM_oh.tsv \
	results/table2/work/formatted/surveillance_fixed.tsv \
	-o results/table2/work/data_merged.tsv


descriptive_stats.sh \
	results/table2/work/data_merged.tsv \
	results/table2/work/MAM_recovery_stats


filter.py \
	results/table2/work/MAM_recovery_stats/merged_stats.tsv \
	-q 'source == "Feed, ERUSF (B)"' \
	-o results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv


rename_regex.py \
	results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv \
	--match 'p_value' \
	--replace 'pval_feed' \
	--o results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_rename.tsv


select_features.py \
	results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_rename.tsv \
	-c 'target,pval_feed' \
	--drop-index \
	-o results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv


# Merge descriptive + stats
merge.py \
	results/table2/work/merged.tsv \
	results/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o results/table2/work/merged_stats.tsv


# =================
# FDR correction (same as Table 1)
# =================

fdr.py \
	results/table2/work/merged_stats.tsv \
	-p pval_feed \
	--colname qval_feed \
	-o results/table2/work/merged_stats_fdr.tsv
