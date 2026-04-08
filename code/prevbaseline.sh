#!/usr/bin/env bash

set -euo pipefail
source env.sh

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/timepoints/0/anthro.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/anthro | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/timepoints/0/vitamin.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/vitamin | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/filtered/genetics.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/genetics | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/filtered/surveillance_minus_catchup.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/surveillance | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/timepoints/0/aa.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/aa | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/timepoints/0/alpha_diversity.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/alpha_diversity | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/timepoints/0/head.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/head | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/timepoints/0/lipids.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/lipids | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--min_abundance -100 \
	--min_variance 0 \
	--zero-threshold -100 \
	--min_prevalence 0 \
	--normalization NONE \
	--transform NONE \
	--warn_prevalence False \
	--evaluate_only abundance \
	--max_pngs 0 \
	results/timepoints/0/sleep.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/sleep | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--warn_prevalence False \
	--max_pngs 0 \
	results/timepoints/0/pathways.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/pathways | tail

maaslin3.R \
	--formula " Recovery + Sex + baseline_WLZ + Delivery_Mode + BF" \
	--reference "Recovery,No recovery;Sex,Male;Delivery_Mode;Vaginal" \
	--warn_prevalence False \
	--max_pngs 0 \
	results/timepoints/0/species.tsv \
	results/filtered/meta_MAM.tsv \
	results/baseline_change/maaslin/baseline/species | tail

