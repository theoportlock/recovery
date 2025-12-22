#!/usr/bin/env bash

set -euo pipefail
source env.sh

input=$1
timemeta=$2
output=$3
input=results/filtered/
timemeta=results/filtered/timemeta.tsv
output=results/figure3/maaslin/healthy

# Consider dropping Recovery category
rm -rf $output
mkdir $output

filter.py \
    $timemeta \
    -q 'timepoint == 0 or timepoint == 52' \
    -o $output/timemeta_0_52tp.tsv

fillna.py \
    -i $output/timemeta_0_52tp.tsv \
    -c Feed,Recovery \
    -v 'Well-nourished' \
    -o $output/timemeta_0_52tp_filled.tsv

replace.py \
    $output/timemeta_0_52tp_filled.tsv \
    --to_replace '{"timepoint": {"0": "yr1", "52": "yr2"}}' \
    --output $output/timemeta_0_52tp_filled_formatted.tsv

maaslin3.R \
    --formula "~ timepoint * Feed + (1|subjectID)" \
    --reference "Feed,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.2 \
    --max_significance 0.1 \
    --normalization TSS \
    --transform LOG \
    --warn_prevalence False \
    --small_random_effects True \
    --max_pngs 100 \
    --cores 1 \
    $input/species.tsv \
    $output/timemeta_0_52tp_filled_formatted.tsv \
    $output/species \

maaslin3.R \
    --formula "~ timepoint * Feed + (1|subjectID)" \
    --reference "Feed,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --median_comparison_abundance False \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1 \
    $input/alpha_diversity.tsv \
    $output/timemeta_0_52tp_filled_formatted.tsv \
    $output/alpha_diversity

maaslin3.R \
    --formula "~ timepoint * Feed + (1|subjectID)" \
    --reference "Feed,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1 \
    $input/anthro.tsv \
    $output/timemeta_0_52tp_filled_formatted.tsv \
    $output/anthro

maaslin3.R \
    --formula "~ timepoint * Feed + (1|subjectID)" \
    --reference "Feed,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1 \
    $input/head.tsv \
    $output/timemeta_0_52tp_filled_formatted.tsv \
    $output/head

maaslin3.R \
    --formula "~ timepoint * Feed + (1|subjectID)" \
    --reference "Feed,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization TSS \
    --transform LOG \
    --warn_prevalence False \
    --small_random_effects True \
    --max_pngs 100 \
    --cores 1 \
    $input/pathways.tsv \
    $output/timemeta_0_52tp_filled_formatted.tsv \
    $output/pathways

maaslin3.R \
    --formula "~ timepoint * Feed + (1|subjectID)" \
    --reference "Feed,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1 \
    $input/sleep.tsv \
    $output/timemeta_0_52tp_filled_formatted.tsv \
    $output/sleep

maaslin3.R \
    --formula "~ timepoint * Feed + (1|subjectID)" \
    --reference "Feed,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1 \
    $input/aa.tsv \
    $output/timemeta_0_52tp_filled_formatted.tsv \
    $output/aa

maaslin3.R \
    --formula "~ timepoint * Feed + (1|subjectID)" \
    --reference "Feed,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1 \
    $input/vitamin.tsv \
    $output/timemeta_0_52tp_filled_formatted.tsv \
    $output/vitamin
