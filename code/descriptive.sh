#!/bin/bash
#

source env.sh

rm -rf results/table1
mkdir -p results/table1/work

filter.py 
onehot.py \
	results/filtered/meta.tsv \
	--include-cols 'Sex,Delivery_Mode' \
	-o results/table1/work/Demographics.tsv


