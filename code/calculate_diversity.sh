#!/bin/bash
# Biobakery's calculate diversity functions in their github/utils directory

set -e

export PATH="metaphlan/metaphlan/utils/:$PATH"
export PATH="metatoolkit/metatoolkit/:$PATH"

metaphlan_file=$1

mkdir -p results/mbiome_alpha

transpose.py ${metaphlan_file} -o results/mbiome_alpha/samplesascols.tsv

faith_pd.py ${metaphlan_file} conf/mpa_vOct22_CHOCOPhlAnSGB_202212.nwk -o results/mbiome_alpha/faiths_pd.tsv

# For alpha diversity measures
for metric in gini shannon richness simpson
do
Rscript metaphlan/metaphlan/utils/calculate_diversity.R \
	-f results/mbiome_alpha/samplesascols.tsv \
	-t conf/mpa_vOct22_CHOCOPhlAnSGB_202212.nwk \
	-d alpha \
	-p alpha \
	-m $metric \
	-s t__ \
	-o results/mbiome_alpha
done

rm results/mbiome_alpha/samplesascols.tsv

# Combine alpha diversity metrics and cleanup
merge.py results/mbiome_alpha/* -o results/alpha_diversity.tsv &&
rm -r results/mbiome_alpha
