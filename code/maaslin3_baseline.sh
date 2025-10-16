#!/usr/bin/env bash
set -euo pipefail
source env.sh

filter.py results/filtered/timemetaMAM_0_52tp_filled.tsv -q 'timepoint == 0' -o results/filtered/timemetaMAM_0tp_filled.tsv

maaslin3.R \
	results/filtered/anthro.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/anthro \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/vitamin.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/vitamin \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/wolkes.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/wolkes \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/genetics.tsv \
	results/filtered/meta_MAM.tsv \
	results/maaslin/baseline/genetics \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/pots.tsv \
	results/filtered/meta_MAM.tsv \
	results/maaslin/baseline/pots \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/surveillance.tsv \
	results/filtered/meta_MAM.tsv \
	results/maaslin/baseline/surveillance \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/aa.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/aa \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/alpha_diversity.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/alpha_diversity \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/fcis.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/fcis \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/glitter.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/glitter \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/head.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/head \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/lipids.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/lipids \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/pathways.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/pathways \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/pci.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/pci \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/pss.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/pss \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/sleep.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/sleep \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
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
	--cores 1

maaslin3.R \
	results/filtered/species.tsv \
	results/filtered/timemetaMAM_0tp_filled.tsv \
	results/maaslin/baseline/species \
	--formula "~ Recovery + Sex" \
	--reference "Recovery,No recovery;Sex,Male" \
	--max_significance 0.9 \
	--warn_prevalence False \
	--max_pngs 100 \
	--cores 1

