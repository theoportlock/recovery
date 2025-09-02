#!/bin/bash
set -euo pipefail
source env.sh

data_dir=results/filtered/
output_dir=results/mofa_mbiome

scale.py CLR $data_dir/species.tsv --output results/mofa_mbiome/data/species_CLR.tsv
scale.py CLR $data_dir/pathways.tsv --output results/mofa_mbiome/data/pathways_CLR.tsv

for f in $(cat conf/mbiomdatasets.txt); do
    splitter.py \
        "$output_dir/data/${f}_CLR.tsv" \
        -m $data_dir/timemeta_0_52tp.tsv \
        -col timepoint \
        --outdir "$output_dir/timepoints" \
        --reindex subjectID
done

mofa_load_data.py \
	--t1-dir $output_dir/timepoints/0 \
	--meta-file $data_dir/meta.tsv \
	--output $output_dir/mdata.h5mu

mofa_run.py \
	--input $output_dir/mdata.h5mu \
	--factors 20 \
	--output $output_dir/mofa_model.hdf5

mofa_export.R \
	--model results/mofa_mbiome/mofa_model.hdf5 \
	--outdir results/mofa_mbiome/extract

