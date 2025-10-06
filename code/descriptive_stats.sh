#!/bin/bash
source env.sh

#input=results/table1/work/all_data_merged.tsv
#output=results/table1/work/stats
input=$1
output=$2

rm -rf $output
mkdir -p $output

filter.py $input \
	--dtype bool \
	-o $output/categories.tsv

filter.py $input \
	--dtype number \
	-o $output/numbers.tsv

corr.py \
	$output/numbers.tsv \
	-o $output/corr.tsv

mannwhitneyu.py \
	$output/numbers.tsv \
	$output/categories.tsv \
	-o $output/mwu.tsv

fisher.py \
	$output/categories.tsv \
	-o $output/fisher.tsv

merge.py \
	$output/corr.tsv \
	$output/mwu.tsv \
	$output/fisher.tsv \
	-a \
	--add-filename \
	--filename-format base \
	-o $output/merged_stats.tsv

filter.py \
	$output/merged_stats.tsv \
	-q 'p_value < 0.05' \
	-o $output/merged_stats_filtered.tsv

create_network.py \
	--edges $output/merged_stats_filtered.tsv \
	--output $output/merged_stats_filtered_network.graphml
