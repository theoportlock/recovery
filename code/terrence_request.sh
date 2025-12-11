#!/bin/bash
 
source env.sh

filter.py \
	results/figure2/maaslin/baseline/timemetaMAM_0_52tp_filled.tsv \
	-q 'timepoint == 52' \
	-o results/figure2/maaslin/baseline/timemetaMAM_52tp_filled.tsv

for f in $(cat conf/timedatasets.txt); do
  splitter.py \
    results/cleaned/${f}.tsv \
    -m results/figure2/maaslin/baseline/timemetaMAM_0tp_filled.tsv \
    -col Feed \
    --outdir results/feedbl \
    --reindex subjectID 
done

for f in $(cat conf/timedatasets.txt); do
  splitter.py \
    results/cleaned/${f}.tsv \
    -m results/figure2/maaslin/baseline/timemetaMAM_52tp_filled.tsv \
    -col Feed \
    --outdir results/feedyr2 \
    --reindex subjectID 
done
