maaslin3.R \
    --formula "~ timepoint * Feed + Sex + baseline_WLZ + Delivery_Mode + BF + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);timepoint,yr1;Sex,Male;Delivery_Mode;Vaginal" \
    --warn_prevalence False \
    --small_random_effects True \
    --max_pngs 0 \
    --cores 1 \
    results/filtered/species.tsv \
    results/filtered/timemeta_MAM_yr1_yr2.tsv \
    results/healthy_change/maaslin/healthy/species

maaslin3.R \
    --formula "~ timepoint * Feed + Sex + baseline_WLZ + Delivery_Mode + BF + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);timepoint,yr1;Sex,Male;Delivery_Mode;Vaginal" \
    --min_abundance 0 \
    --min_prevalence 0.2 \
    --max_significance 0.1 \
    --normalization TSS \
    --transform LOG \
    --warn_prevalence False \
    --small_random_effects True \
    --max_pngs 0 \
    --cores 1 \
    results/filtered/pathways.tsv \
    results/filtered/timemeta_MAM_yr1_yr2.tsv \
    results/healthy_change/maaslin/healthy/pathways

maaslin3.R \
    --formula "~ timepoint * Feed + Sex + baseline_WLZ + Delivery_Mode + BF + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);timepoint,yr1;Sex,Male;Delivery_Mode;Vaginal" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --median_comparison_abundance False \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 0 \
    --cores 1 \
    results/filtered/alpha_diversity.tsv \
    results/filtered/timemeta_MAM_yr1_yr2.tsv \
    results/healthy_change/maaslin/healthy/alpha_diversity

maaslin3.R \
    --formula "~ timepoint * Feed + Sex + baseline_WLZ + Delivery_Mode + BF + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);timepoint,yr1;Sex,Male;Delivery_Mode;Vaginal" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 0 \
    --cores 1 \
    results/filtered/anthro.tsv \
    results/filtered/timemeta_MAM_yr1_yr2.tsv \
    results/healthy_change/maaslin/healthy/anthro

maaslin3.R \
    --formula "~ timepoint * Feed + Sex + baseline_WLZ + Delivery_Mode + BF + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);timepoint,yr1;Sex,Male;Delivery_Mode;Vaginal" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 0 \
    --cores 1 \
    results/filtered/head.tsv \
    results/filtered/timemeta_MAM_yr1_yr2.tsv \
    results/healthy_change/maaslin/healthy/head

maaslin3.R \
    --formula "~ timepoint * Feed + Sex + baseline_WLZ + Delivery_Mode + BF + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);timepoint,yr1;Sex,Male;Delivery_Mode;Vaginal" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 0 \
    --cores 1 \
    results/filtered/sleep.tsv \
    results/filtered/timemeta_MAM_yr1_yr2.tsv \
    results/healthy_change/maaslin/healthy/sleep

maaslin3.R \
    --formula "~ timepoint * Feed + Sex + baseline_WLZ + Delivery_Mode + BF + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);timepoint,yr1;Sex,Male;Delivery_Mode;Vaginal" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 0 \
    --cores 1 \
    results/filtered/aa.tsv \
    results/filtered/timemeta_MAM_yr1_yr2.tsv \
    results/healthy_change/maaslin/healthy/aa

maaslin3.R \
    --formula "~ timepoint * Feed + Sex + baseline_WLZ + Delivery_Mode + BF + (1|subjectID)" \
    --reference "Feed,Local RUSF (A);timepoint,yr1;Sex,Male;Delivery_Mode;Vaginal" \
    --min_abundance 0 \
    --min_prevalence 0.0 \
    --max_significance 0.1 \
    --normalization NONE \
    --transform NONE \
    --warn_prevalence False \
    --small_random_effects True \
    --evaluate_only abundance \
    --max_pngs 0 \
    --cores 1 \
    results/filtered/vitamin.tsv \
    results/filtered/timemeta_MAM_yr1_yr2.tsv \
    results/healthy_change/maaslin/healthy/vitamin
