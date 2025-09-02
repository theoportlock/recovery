#!/bin/bash
# A tool for measuring the power of a model in capturing the importance of feature and feature interaction effects
# Theo Portlock

set +e

source env.sh

data=results/merged_dataset.tsv
meta=results/timepoints/yr2/anthro.tsv
output=results/prediction

test_train_split.py \
	--input $data \
	--y_col WLZ_WHZ \
	--y_file results/timepoints/yr2/anthro.tsv \
	--scaler none \
	--output_dir $output/dataset_split

random_forest.py \
	--input_dir $output/dataset_split/ \
	--task regression \
	--output_model $output/dataset_rf.pkl

evaluate_model.py \
	--model $output/dataset_rf.pkl \
	--input_dir $output/dataset_split/ \
	--task regression \
	--report_file $output/dataset_report_rf.tsv

shap_interpret.py \
	--model $output/dataset_rf.pkl \
	--input_dir $output/dataset_split/ \
	--shap_val \
	--shap_interact \
	--output_dir $output/dataset_rf_shap 

create_network.py \
	--edges $output/dataset_rf_shap/mean_abs_shap_interaction_train.tsv \
	--output $output/network.graphml

plot_network.py \
	$output/network.graphml \
	--edge_color_attr mean_abs_shap_interaction_test.tsv \
	--layout shell \
	--cmap Reds \
	--figsize 4 4 \
	--output $output/network2.svg

shap_plots.sh

arrange_svgs.py \
	$output/shap_plots_test_data/* \
	--cols 2 \
	--output $output/shap_plots_merged.svg

