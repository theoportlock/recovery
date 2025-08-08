
#!/bin/bash
# A tool for measuring the power of a model in capturing the importance of feature and feature interaction effects
# Theo Portlock

set +e

source venv/bin/activate
export PATH="code/:$PATH"
export PATH="metatoolkit/metatoolkit/:$PATH"

SCIPY_ARRAY_API=1 test_train_split.py \
	--input results/mofa/sample_factors.tsv \
	--y_file results/filtered/meta.tsv \
	--y_col Recovery \
	--output_dir results/dataset_split

random_forest.py \
	--input_dir results/dataset_split/ \
	--task classification \
	--output_model results/dataset_rf.pkl

evaluate_model.py \
	--model results/dataset_rf.pkl \
	--input_dir results/dataset_split/ \
	--task classification \
	--report_file results/dataset_report_rf.tsv

shap_interpret.py \
	--model results/dataset_rf.pkl \
	--input_dir results/dataset_split/ \
	--shap_val \
	--shap_interact \
	--output_dir results/dataset_rf_shap 

shap_plots.sh

arrange_svgs.py \
	results/shap_plots_test_data/* \
	--cols 2 \
	--output results/shap_plots_merged.svg

