#!/usr/bin/env bash
set -euo pipefail
source env.sh

filter.py \
    results/filtered/timemeta.tsv \
    -q 'timepoint == 0 or timepoint == 52' \
    -o results/filtered/timemeta_0_52tp.tsv

fillna.py \
    -i results/filtered/timemeta_0_52tp.tsv \
    -c Feed,Recovery \
    -v 'Well-nourished' \
    -o results/filtered/timemeta_0_52tp_filled.tsv

# Test first here
maaslin3.R \
    results/filtered/species.tsv \
    results/filtered/timemeta_0_52tp_filled.tsv \
    results/maaslin/time/species \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Well-nourished;Recovery,Well-nourished;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.2 \
    --max_significance 0.1 \
    --normalization TSS \
    --transform LOG \
    --warn_prevalence False \
    --small_random_effects True \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/aa.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/aa \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/alpha_diversity.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/alpha_diversity \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/anthro.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/anthro \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/fcis.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/fcis \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/glitter.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/glitter \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/head.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/head \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/lipids.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/lipids \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/pathways.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/pathways \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization TSS \
    --transform LOG \
    --warn_prevalence False \
    --small_random_effects True \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/pci.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/pci \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/pss.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/pss \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/sleep.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/sleep \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 100 \
    --cores 1

maaslin3.R \
    results/filtered/species.tsv \
    results/filtered/timemeta_MAM_0_52tp.tsv \
    results/maaslin/species \
    --formula "~ timepoint*(Feed + Recovery) + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);Recovery,No recovery;timepoint,yr1" \
    --min_abundance 0 \
    --min_prevalence 0.2 \
    --max_significance 0.1 \
    --normalization TSS \
    --transform LOG \
    --warn_prevalence False \
    --small_random_effects True \
    --max_pngs 100 \
    --cores 1

