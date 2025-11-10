#!/bin/bash
# A tool for measuring the power of a model in capturing the importance of feature and feature interaction effects
# Theo Portlock

set -e
source env.sh

#input=results/merged_dataset.tsv
#output=results/prediction
input=$1
output=$2

rm -rf $output
mkdir -p $output

test_train_split.py \
	--input $input \
	--y_col WLZ_WHZ \
	--y_file results/timepoints/yr2/anthro.tsv \
	--scaler none \
	--keepna \
	--output_dir $output/dataset_split

#xgboost_model.py \
random_forest.py \
	--input_dir $output/dataset_split/ \
	--task regression \
	--output_model $output/model.pkl

evaluate_model.py \
	--model $output/model.pkl \
	--input_dir $output/dataset_split/ \
	--task regression \
	--report_file $output/model_report.tsv

shap_interpret.py \
	--model $output/model.pkl \
	--input_dir $output/dataset_split/ \
	--shap_val \
	--shap_interact \
	--output_dir $output/model_shap 

create_network.py \
	--edges $output/model_shap/mean_abs_shap_interaction_train.tsv \
	--output $output/network.graphml

plot_network.py \
	$output/network.graphml \
	--edge_color_attr mean_abs_shap_interaction_test.tsv \
	--layout shell \
	--cmap Reds \
	--figsize 4 4 \
	--output $output/network2.svg

shap_plots.sh \
	$output/model_shap/shap_values_test.joblib \
	$output/plots

plot_regression_residuals.py \
	--model $output/model.pkl \
	--input $output/dataset_split \
	--output $output/plots

arrange_svgs.py \
	$output/plots/* \
	--cols 2 \
	--output $output/shap_plots_merged.svg

