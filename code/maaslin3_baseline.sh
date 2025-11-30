#!/usr/bin/env bash

set -euo pipefail
source env.sh

input=results/filtered
timemeta=results/filtered/timemeta_MAM_0_52tp.tsv
output=results/figure2/maaslin/baseline
#input=$1
#timemeta=$2
#output=$3

rm -rf $output
mkdir $output

fillna.py \
	-i $timemeta \
	-c Feed,Recovery \
	-v 'Well-nourished (C)' \
	-o $output/timemetaMAM_0_52tp_filled.tsv

filter.py \
	$output/timemetaMAM_0_52tp_filled.tsv \
	-q 'timepoint == 0' \
	-o $output/timemetaMAM_0tp_filled.tsv

cp \
	$input/meta_MAM.tsv \
	$output/meta_MAM.tsv

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/anthro.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/anthro

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/vitamin.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/vitamin

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/genetics.tsv \
	$output/meta_MAM.tsv \
	$output/genetics

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 0.1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/surveillance_minus_catchup.tsv \
	$output/meta_MAM.tsv \
	$output/surveillance

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/aa.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/aa

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/alpha_diversity.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/alpha_diversity

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/head.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/head

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/lipids.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/lipids

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/pathways.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/pathways

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--max_significance 1 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 100 \
	--cores 1 \
	$input/sleep.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/sleep

maaslin3.R \
	--formula "~ Recovery" \
	--reference "Recovery,No recovery" \
	--max_significance 1\
	--warn_prevalence False \
	--max_pngs 100 \
	--cores 1 \
	$input/species.tsv \
	$output/timemetaMAM_0tp_filled.tsv \
	$output/species

