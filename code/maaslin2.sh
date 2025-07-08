#!/bin/bash

export PATH="code/:$PATH"
export PATH="metatoolkit/metatoolkit/:$PATH"
export PATH="Maaslin2/R/:$PATH"

# Maaslin2
mkdir -p results/maaslin results/change

#Maaslin2.R results/filtered/wolkes.tsv results/timemeta_MAM.tsv results/maaslin/wolkes -f "timepoint,Recovery,Feed,Sex,Delivery_Mode" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
Maaslin2.R results/filtered/bayley.tsv results/timemeta_MAM.tsv results/maaslin/bayley -f "timepoint,Recovery,Feed,Sex,Delivery_Mode" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/vitamin.tsv results/timemeta_MAM.tsv results/maaslin/vitamin -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/vep.tsv results/timemeta_MAM.tsv results/maaslin/vep -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/species.tsv results/timemeta_MAM.tsv results/maaslin/species -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/sleep.tsv results/timemeta_MAM.tsv results/maaslin/sleep -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/pss.tsv results/timemeta_MAM.tsv results/maaslin/pss -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/psd.tsv results/timemeta_MAM.tsv results/maaslin/psd -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/pci.tsv results/timemeta_MAM.tsv results/maaslin/pci -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/pathways.tsv results/timemeta_MAM.tsv results/maaslin/pathways -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/micro.tsv results/timemeta_MAM.tsv results/maaslin/micro -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/lipids.tsv results/timemeta_MAM.tsv results/maaslin/lipids -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/head.tsv results/timemeta_MAM.tsv results/maaslin/head -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/glitter.tsv results/timemeta_MAM.tsv results/maaslin/glitter -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/fnirs.tsv results/timemeta_MAM.tsv results/maaslin/fnirs -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/fcis.tsv results/timemeta_MAM.tsv results/maaslin/fcis -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/anthro.tsv results/timemeta_MAM.tsv results/maaslin/anthro -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/alpha_diversity.tsv results/timemeta_MAM.tsv results/maaslin/alpha_diversity -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"
#Maaslin2.R results/filtered/aa.tsv results/timemeta_MAM.tsv results/maaslin/aa -f "timepoint,Recovery,Feed" -r "subjectID" -d "Recovery,No recovery;Feed,Local RUSF (A)"





#parallel -j1 cp results/maaslin/{}/all_results.tsv results/change/{} < conf/all_datasets.txt

#merge.py results/change/* -o allchange --append --add-filename
#filter.py allchange -q 'metadata=="Feed" & qval < 0.25'
#filter.py allchange -q 'qval < 0.25 & metadata != "timepoint"' -o sigchange
#volcano.py allchangefilter

