#!/bin/bash

source env.sh

rm -rf $WORK/table2
mkdir -p $WORK/table2/work/{selected,formatted,descriptive}

# One-hot recovery
onehot.py \
	$WORK/filtered/recovery_status.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o $WORK/table2/work/formatted/recovery_status_oh.tsv

# Surveillance
select_features.py \
	$WORK/filtered/surveillance.tsv \
	-c 'days_of_catchup,fail_no.failure' \
	-o $WORK/table2/work/formatted/surveillance.tsv

# Metadata
select_features.py \
	$WORK/filtered/covmeta_MAM.tsv \
	-c 'Feed' \
	-o $WORK/table2/work/selected/meta_MAM.tsv

onehot.py \
	$WORK/table2/work/selected/meta_MAM.tsv \
	--prefix-sep ', ' \
	--dtype bool \
	-o $WORK/table2/work/formatted/meta_MAM_oh.tsv


# Fix formatting first
rename_regex.py \
	$WORK/table2/work/formatted/surveillance.tsv \
	--match 77 --replace 79 \
	--output $WORK/table2/work/formatted/surveillance_fixed.tsv

rename_regex.py \
	$WORK/table2/work/formatted/surveillance_fixed.tsv \
	--match 74 --replace 80 \
	--output $WORK/table2/work/formatted/surveillance_fixed.tsv


# Descriptive tables
for file in $WORK/table2/work/formatted/{meta_MAM_oh,recovery_status_oh,surveillance_fixed}.tsv; do
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


# =================
# Stats
# =================

merge.py \
	$WORK/table2/work/formatted/recovery_status_oh.tsv \
	$WORK/table2/work/formatted/meta_MAM_oh.tsv \
	$WORK/table2/work/formatted/surveillance_fixed.tsv \
	-o $WORK/table2/work/data_merged.tsv


descriptive_stats.sh \
	$WORK/table2/work/data_merged.tsv \
	$WORK/table2/work/MAM_recovery_stats


filter.py \
	$WORK/table2/work/MAM_recovery_stats/merged_stats.tsv \
	-q 'source == "Feed, ERUSF (B)"' \
	-o $WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv


rename_regex.py \
	$WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats.tsv \
	--match 'p_value' \
	--replace 'pval_feed' \
	--o $WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_rename.tsv


select_features.py \
	$WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_rename.tsv \
	-c 'target,pval_feed' \
	--drop-index \
	-o $WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv


# Merge descriptive + stats
merge.py \
	$WORK/table2/work/merged.tsv \
	$WORK/table2/work/MAM_recovery_stats/merged_stats_Recoverstats_vals.tsv \
	-o $WORK/table2/work/merged_stats.tsv


# =================
# FDR correction (same as Table 1)
# =================

fdr.py \
	$WORK/table2/work/merged_stats.tsv \
	-p pval_feed \
	--colname qval_feed \
	-o $WORK/table2/work/merged_stats_fdr.tsv
