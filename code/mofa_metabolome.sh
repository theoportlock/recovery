#!/bin/bash
set -euo pipefail
source env.sh

data_dir=results/filtered
output_dir=results/mofa_metabolome

scale.py CLR $data_dir/lipids.tsv --output $output_dir/data/untargetted_CLR.tsv

scale.py CLR $data_dir/vitamin.tsv --output $output_dir/data/vitamin_CLR.tsv
scale.py CLR $data_dir/aa.tsv --output $output_dir/data/aa_CLR.tsv
merge.py $output_dir/data/{aa,vitamin}_CLR.tsv -o $output_dir/data/targetted_CLR.tsv

for f in targetted untargetted; do
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
	--model $output_dir/mofa_model.hdf5 \
	--outdir $output_dir/extract

