#!/bin/bash

rm -rf results/table1
mkdir -p results/table1/work/{selected,formatted,descriptive}

fillna.py \
	-i results/filtered/meta.tsv \
	-v 'Well-nourished (C)' \
	-c 'Feed' \
	-o results/table1/work/meta.tsv

# Demographics
select_features.py \
	results/table1/work/meta.tsv \
	-c 'Sex,Delivery_Mode' \
	-o results/table1/work/selected/Demographics.tsv

onehot.py \
	results/table1/work/selected/Demographics.tsv \
	--drop-onehot-values 'Male,Vaginal' \
	--prefix-sep ', ' \
	--dtype bool \
	-o results/table1/work/formatted/Demographics.tsv

# Parental Education and Economics
select_features.py \
	results/filtered/education.tsv \
	-c 'Years_of_fathers_education,Years_of_mothers_education' \
	-o results/table1/work/selected/Parental_Education.tsv

select_features.py \
	results/filtered/economics.tsv \
	-c 'Mothers_income,Fathers_income,Total_monthly_income,Monthly_total_expenditure' \
	-o results/table1/work/selected/Economics.tsv

merge.py \
	results/table1/work/selected/Parental_Education.tsv \
	results/table1/work/selected/Economics.tsv \
	-o results/table1/work/formatted/Parental_Education_and_Economics.tsv

# Family Structure
select_features.py \
	results/filtered/family.tsv \
	-c 'Number_of_living_children,Number_of_children_under_five_years,Family_type.Nuclear' \
	-o results/table1/work/formatted/Family_Structure.tsv

# Household Characterics
select_features.py \
	results/filtered/household.tsv \
	-c '
		Members_in_household
		Number_of_years_lived_in_current_household
		Number_of_rooms_in_current_household
		Cooking_gas.Yes	
		Working_TV.Yes	
		Household_food_availability.Sometimes deficit' \
	-o results/table1/work/formatted/Household_characteristics.tsv

# Other Characteristics
select_features.py \
	results/table1/work/meta.tsv \
	-c 'BF,PoB' \
	-o results/table1/work/selected/Other.tsv

onehot.py \
	results/table1/work/selected/Other.tsv \
	--drop-onehot-values 'Clinic' \
	--prefix-sep ', ' \
	-o results/table1/work/formatted/Other.tsv

# Anthropometrics
select_features.py \
	results/timepoints/0/anthro.tsv \
	-c 'WLZ_WHZ,Weight,MUAC,HC' \
	-o results/table1/work/formatted/Anthro.tsv

# Descriptive
for file in results/table1/work/formatted/{Demographics,Parental_Education_and_Economics,Family_Structure,Household_characteristics,Other,Anthro}.tsv; do
    descriptive.py \
        -i "$file" \
        --meta results/table1/work/meta.tsv \
        -g 'Feed' \
        -o "results/table1/work/descriptive/$(basename "$file")"
done

# Stats
# Add condition and feed
select_features.py \
	results/filtered/meta.tsv \
	-c 'Condition,Feed' \
	-o results/table1/work/meta.tsv

onehot.py \
	results/table1/work/meta.tsv \
	--drop-onehot-values 'Well-nourished,Local RUSF (A)' \
	--prefix-sep ', ' \
	--dtype bool \
	-o results/table1/work/meta_oh.tsv

merge.py \
	results/table1/work/formatted/Demographics.tsv \
	results/table1/work/formatted/Parental_Education_and_Economics.tsv \
	results/table1/work/formatted/Family_Structure.tsv \
	results/table1/work/formatted/Household_characteristics.tsv \
	results/table1/work/formatted/Other.tsv \
	results/table1/work/formatted/Anthro.tsv \
	-o results/table1/work/data.tsv

merge.py \
	results/table1/work/meta_oh.tsv \
	results/table1/work/data.tsv \
	-o results/table1/work/all_data_merged.tsv
	
descriptive_stats.sh \
	results/table1/work/all_data_merged.tsv \
	results/table1/work/all_stats

filter.py \
	results/table1/work/all_stats/merged_stats.tsv \
	-q 'source == "Condition, MAM"' \
	-o results/table1/work/all_stats/merged_stats_MAMstats.tsv

rename_regex.py \
	results/table1/work/all_stats/merged_stats_MAMstats.tsv \
	--match 'p_value' \
	--replace 'pval_mam' \
	--o results/table1/work/all_stats/merged_stats_MAMstats_rename.tsv

select_features.py \
	results/table1/work/all_stats/merged_stats_MAMstats_rename.tsv \
	-c 'target,pval_mam' \
	--drop-index \
	-o results/table1/work/all_stats/merged_stats_MAMstats_vals.tsv

# Just Feed stats
filter.py \
	results/table1/work/meta_oh.tsv \
	-q '`Condition, MAM` == True' \
	-o results/table1/work/meta_oh_MAM.tsv

merge.py \
	results/table1/work/meta_oh_MAM.tsv \
	results/table1/work/data.tsv \
	-o results/table1/work/MAM_data_merged.tsv

descriptive_stats.sh \
	results/table1/work/MAM_data_merged.tsv \
	results/table1/work/MAM_stats

filter.py \
	results/table1/work/MAM_stats/merged_stats.tsv \
	-q 'source == "Feed, ERUSF (B)"' \
	-o results/table1/work/MAM_stats/merged_stats_Feedstats.tsv

rename_regex.py \
	results/table1/work/MAM_stats/merged_stats_Feedstats.tsv \
	--match 'p_value' \
	--replace 'pval_feed' \
	--o results/table1/work/MAM_stats/merged_stats_Feedstats_rename.tsv
	
select_features.py \
	results/table1/work/MAM_stats/merged_stats_Feedstats_rename.tsv \
	-c 'target,pval_feed' \
	--drop-index \
	-o results/table1/work/MAM_stats/merged_stats_Feedstats_vals.tsv

# Merge
merge.py \
	results/table1/work/descriptive/Demographics.tsv \
	results/table1/work/descriptive/Parental_Education_and_Economics.tsv \
	results/table1/work/descriptive/Family_Structure.tsv \
	results/table1/work/descriptive/Household_characteristics.tsv \
	results/table1/work/descriptive/Other.tsv \
	results/table1/work/descriptive/Anthro.tsv \
	-a \
	--add-filename \
	--filename-format base \
	-o results/table1/work/merged.tsv

merge.py \
	results/table1/work/merged.tsv \
	results/table1/work/MAM_stats/merged_stats_Feedstats_vals.tsv \
	results/table1/work/all_stats/merged_stats_MAMstats_vals.tsv \
	-o results/table1/work/merged_stats.tsv

fdr.py \
	results/table1/work/merged_stats.tsv \
	-p pval_feed \
	--replace \
	-o results/table1/work/merged_stats_fdr.tsv

fdr.py \
	results/table1/work/merged_stats_fdr.tsv \
	-p pval_mam \
	--replace \
	-o results/table1/work/merged_stats_fdr_2.tsv
