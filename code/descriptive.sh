#!/bin/bash

source env.sh

rm -rf results/table1
mkdir -p results/table1/work/{selected,formatted,descriptive}

fillna.py \
	-i results/filtered/meta.tsv \
	-v 'Well-nourished (C)' \
	-c 'Feed' \
	-o results/table1/work/meta.tsv

# Demographics
select.py \
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
select.py \
	results/filtered/education.tsv \
	-c 'Years_of_fathers_education,Years_of_mothers_education' \
	-o results/table1/work/selected/Parental_Education.tsv

select.py \
	results/filtered/economics.tsv \
	-c 'Mothers_income,Fathers_income,Total_monthly_income,Monthly_total_expenditure' \
	-o results/table1/work/selected/Economics.tsv

merge.py \
	results/table1/work/selected/Parental_Education.tsv \
	results/table1/work/selected/Economics.tsv \
	-o results/table1/work/formatted/Parental_Education_and_Economics.tsv

# Family Structure
select.py \
	results/filtered/family.tsv \
	-c 'Number_of_living_children,Number_of_children_under_five_years,Family_type.Nuclear' \
	-o results/table1/work/formatted/Family_Structure.tsv

# Household Characterics
select.py \
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
select.py \
	results/table1/work/meta.tsv \
	-c 'BF,PoB' \
	-o results/table1/work/selected/Other.tsv

onehot.py \
	results/table1/work/selected/Other.tsv \
	--drop-onehot-values 'Clinic' \
	--prefix-sep ', ' \
	-o results/table1/work/formatted/Other.tsv

for file in results/table1/work/formatted/{Demographics,Parental_Education_and_Economics,Family_Structure,Household_characteristics,Other}.tsv; do
    descriptive.py \
        -i "$file" \
        --meta results/table1/work/meta.tsv \
        -g 'Feed' \
        -o "results/table1/work/descriptive/$(basename "$file")"
done

# Stats
merge.py \
	results/table1/work/formatted/Demographics.tsv \
	results/table1/work/formatted/Parental_Education_and_Economics.tsv \
	results/table1/work/formatted/Family_Structure.tsv \
	results/table1/work/formatted/Household_characteristics.tsv \
	results/table1/work/formatted/Other.tsv \
	-o results/table1/work/all_data_merged.tsv

# TODO
descriptive_stats.sh \
	results/table1/work/all_data_merged.tsv \
	results/table1/work/stats

# Merge
merge.py \
	results/table1/work/descriptive/Demographics.tsv \
	results/table1/work/descriptive/Parental_Education_and_Economics.tsv \
	results/table1/work/descriptive/Family_Structure.tsv \
	results/table1/work/descriptive/Household_characteristics.tsv \
	results/table1/work/descriptive/Other.tsv \
	-a \
	--add-filename \
	--filename-format base \
	-o results/table1/work/merged.tsv
