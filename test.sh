maaslin3.R \
  results/filtered/species.tsv \
  results/timemeta.tsv \
  results/maaslin/species_m3 \
  --fixed_effects "Recovery,Condition" \
  --reference "Recovery,No recovery;Condition,Well-nourished" \
  --random_effects "subjectID" \
  --min_prevalence 0.5 \
  --small_random_effects TRUE \
  --cores 10 \
  --normalization TSS \
  --transform LOG \
  --standardize TRUE \
  --plot_summary_plot FALSE \
  --plot_associations FALSE
