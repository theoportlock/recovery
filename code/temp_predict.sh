
#!/bin/bash
# A tool for measuring the power of a model in capturing the importance of feature and feature interaction effects
# Theo Portlock

set +e

source venv/bin/activate
export PATH="code/:$PATH"
export PATH="metatoolkit/metatoolkit/:$PATH"

merge.py results/baseline/species.tsv \
	results/baseline/aa.tsv
	-o results/merged_aa_species.tsv

SCIPY_ARRAY_API=1 test_train_split.py \
	--input results/baseline/genetics.tsv \
	--y_file results/filtered/metaonehot.tsv \
	--y_col Recovery.Recovered \
	--output_dir results/dataset_split

random_forest.py \
	--input_dir results/genetics_rf/ \
	--task classification \
	--output_model results/dataset_rf.pkl

evaluate_model.py \
	--model results/dataset_rf.pkl \
	--input_dir results/dataset_split/ \
	--task regression \
	--report_file results/dataset_report_rf.tsv

shap_interpret.py \
	--model results/dataset_rf.pkl \
	--input_dir results/dataset_split/ \
	--shap_val \
	--shap_interact \
	--output_dir results/dataset_rf_shap 

merge.py \
	results/theoretical_variance/interaction_importance.tsv \
	results/dataset_rf_shap/mean_abs_shap_interaction_test.tsv \
	-a \
	--add-filename \
	-o results/merged_interactions.tsv

format_merged.py

plot.py

create_network.py \
	--edges results/format_merged_interactions.tsv \
	--output results/network.graphml

plot_network.py \
	results/network.graphml \
	--edge_color_attr mean_abs_shap_interaction_test.tsv \
	--layout shell \
	--cmap Reds \
	--figsize 4 4 \
	--output results/network2.svg

shap_plots.sh

arrange_svgs.py \
	results/shap_plots_test_data/* \
	--cols 2 \
	--output results/shap_plots_merged.svg

