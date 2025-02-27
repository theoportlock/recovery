#!/bin/bash
####################################
# RECOVERY OF MALNUTRITION
####################################

# Format Raw Data
yes | rm -r ../results/*
ls format* | parallel python {}

# Encode metadata
calculate.py onehot meta

# Create full timemeta
tsv-join -H -a '*' -k 'ID' -f ../results/meta.tsv ../results/timemeta.tsv > ../results/fulltimemeta.tsv

# See all data
python ./alldata.py 

# Format microbiome diversity
./calculate_diversity.sh taxo

# Calculate overall recovery for each refeed
data='bayley fcis fnirs head micro pathways pci psd pss sleep taxo vep wolkes'
#printf "$data" | parallel -d ' ' python overall_recovery.py {}
parallel python overall_recovery.py {} < ../conf/datasets.txt
#cat ../conf/datasets.txt | parallel -d ' ' python overall_recovery.py {}
tsv-append -H ../results/*recovery.tsv > ../results/allrecover.tsv

# Individual recovery for each dataset
#printf "$data" | parallel -d ' ' distance.py {}
parallel distance.py {} < ../conf/datasets.txt
#printf "$data" | parallel -d ' ' ./individual_recovery.py {}Dist
parallel python individual_recovery.py {}Dist < ../conf/datasets.txt
merge.py -j outer ../results/*recovered.tsv -o allrecd

# Explain recovery from baseline
tsv-join -H -a '*' -k 'ID' -f ../results/allrecd.tsv ../results/timemeta.tsv > ../results/fullrectimemeta.tsv	
filter.py -q 'timepoint == 0' fullrectimemeta

predict.py 

