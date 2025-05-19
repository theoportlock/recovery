#!/bin/bash
# This script is used to run the commands for the analysis pipeline.
# It is assumed that the commands are run in the order they are listed.
# The script is not intended to be run as a standalone script, but rather as a template for running the commands in the pipeline.

export PATH="code/:$PATH"
export PATH="metatoolkit/metatoolkit/:$PATH"

# Setup
format_bfpob.py
format_lipids.py
format_anthro.py
format_fnirs.py
format_pots.py
format_bayley.py
format_vitamin.py
format_deliverysupp.py
format_micro.py
format_psd.py
format_microbiome_samplesheet.py
format_glitter.py
format_head.py
format_kneaddata.py
format_humann.py
format_aa.py
format_vep.py
format_pss.py
format_surveillance.py
format_genetics.py
format_metaphlan.py
format_wolkes.py
format_ses.py
format_sleep.py
format_pci.py
calculate_diversity.sh results/metaphlan.tsv
extract_species.py
format_feedsandrecovery.py
format_fcis.py
merge.py premeta feedandrecovery deliverysupp bfpob -j outer -o meta
parallel -j1 remove_3yr_control.py results/{}.tsv -o results/filtered/{}.tsv < conf/all_datasets.txt
create_mapping.py -d results/filtered/ -i conf/timedatasets.txt
join.py mapping results/filtered/meta.tsv --on subjectID -o timemeta

# Time to recovery figure
anthrotime.py

# Explained variance
# T1
filter.py timemeta -q 'timepoint == 0 and Condition == "MAM" and (Recovery == "No recovery" or Recovery == "Recovered")' -o timemeta_baseline
parallel -j1 onehot.py results/filtered/{}.tsv -o results/baseline/{}.tsv < conf/notimedatasets.txt
parallel -j1 stratify.py results/filtered/{}.tsv subjectID --df2 timemeta_baseline -o results/baseline/{}.tsv < conf/timedatasets.txt
mv results/baseline/meta.tsv results/meta_baseline.tsv
explain_variance.py results/baseline/* --df_cats results/meta_baseline.tsv --explainor Recovery.Recovered
format_explain_var.py
box.py results/baseline/household.tsv --meta results/meta_baseline.tsv -x 'Recovery.Recovered' -y 'Number_of_years_lived_in_current_household'

# T2
filter.py timemeta -q 'timepoint == 52 and Condition == "MAM" and (Recovery == "No recovery" or Recovery == "Recovered")' -o timemeta_1yr
parallel -j1 onehot.py results/filtered/{}.tsv -o results/1yr/{}.tsv < conf/notimedatasets.txt
parallel -j1 stratify.py results/filtered/{}.tsv subjectID --df2 timemeta_1yr -o results/1yr/{}.tsv < conf/timedatasets.txt
mv results/1yr/meta.tsv results/meta_1yr.tsv
explain_variance.py results/1yr/* --df_cats results/meta_1yr.tsv --explainor Recovery.Recovered
format_explain_var.py
box.py results/1yr/household.tsv --meta results/meta_1yr.tsv -x 'Recovery.Recovered' -y 'Number_of_years_lived_in_current_household'

# Compare Refeeds
parallel overall_recovery.py {} < conf/timedatasets.txt
tsv-append -H results/*recovery.tsv > results/allrecover.tsv
plot_recover.py

# Maaslin2
filter.py timemeta -q 'Condition == "MAM" and (Recovery == "No recovery" or Recovery == "Recovered")' -o timemeta_MAM
mkdir -p results/maaslin
parallel -j1 'Maaslin2.R results/filtered/{}.tsv results/timemeta_MAM.tsv results/maaslin/{}change -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"' < conf/timedatasets.txt
mkdir -p results/change; parallel -j1 cp results/maaslin/{}change/all_results.tsv results/change/{} < conf/timedatasets.txt
merge.py results/change/* -o allchange --append --add-filename
filter.py allchange -q 'metadata=="Feed" & qval < 0.25'
filter.py allchange -q 'qval < 0.25 & metadata != "timepoint"' -o sigchange
volcano.py allchangefilter

# PCoAs
parallel -j1 distance.py results/filtered/{}.tsv -o results/distance/{}.tsv< conf/timedatasets.txt
parallel -j1 pcoa.py -i results/distance/{}.tsv -o results/pcoa/{}.tsv < conf/timedatasets.txt
spindle.py

# Delta network
parallel -j1 deltas.py -m results/timemeta.tsv -i results/filtered/{}.tsv -o results/deltas/{}.tsv < conf/timedatasets.txt
merge.py results/deltas/*.tsv $(sed "s|^|results/filtered/|" conf/notimedatasets.txt) -o mergedall -j outer
filter.py -dt 'number' mergedall -o numbers
filter.py -m 50 numbers
kruskal.py numbersfilter categories
filter.py -dt 'object' mergedall -o categories
chisquared.py categories -o categories_chisq
python simplecorr.py
python merge_stats.py
filter.py edges -q 'qval < 0.05'
create_network.py --edges results/edgesfilter.tsv --output results/network.graphml
plot_network.py results/network.graphml

# Plots from Delta network
box.py mergedall -x 'Recovery' -y 'WLZ_WHZ' -o results/recover_WLZ_box.svg
box.py results/mergedall.tsv -x 'Feed' -y 'fail_no.failure'
box.py mergedall -x 'Recovery' -y 'tg_46:1' -o results/recover_tg46_box.svg
box.py results/mergedall.tsv -x 'Sex' -y 'days_to_recovery'
box.py mergedall -x 'Recovery' -y 'Weight'

# Supp tables
heatmap_alltimedata.py -d conf/timedatasets.txt
heatmap_allnontimedata.py -d conf/notimedatasets.txt
