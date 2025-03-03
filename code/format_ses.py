import pandas as pd
from ast import literal_eval

# Load data
df = pd.read_excel("../data/05.LEAP_SES_CRF.xlsx", sheet_name='LEAP-SES')
labels = pd.read_csv("../conf/05.LEAP_SES_CRF_MAPPING_TP.tsv", sep='\t', index_col=0)

# Drop dates
df = df.drop(['DOB', 'DOI'], axis=1)

# Create mappings
categories = labels.dropna()['Mapping']
mapping = categories.apply(lambda x: literal_eval('{' + x + '}'))

# Apply mappings
for maps in mapping.index:
    df[maps] = df[maps].replace(mapping[maps])

# Rename columns to new descriptions
df = df.rename(columns=labels.Description)
df = df.set_index('Subject identification number')

# Remove erroneous financial stratifications
df = df.loc[:, ~df.columns.str.startswith('House rent')]

# Remove all unchanging variables
df = df.loc[:, df.nunique() != 1]

df.loc[(df.index.astype(str).str[0] == '1') | (df.index.astype(str).str[0] == '3'), 'Condition'] = 'MAM'
df.loc[df.index.astype(str).str[0] == '2', 'Condition'] = 'Well-nourished'

# Standardize subject ID
df.index = 'LCC' + df.index.astype(str)
df.index.name = 'subjectID'

# Add underscores
df.columns = df.columns.str.replace(' ', '_')

# Define and extract sanitation-related columns
sanitcols = df.columns[df.columns.str.contains('Washing')].tolist() + [
    'Open_drain_beside_house',
    'Type_of_cooking_fuel',
    'Place_for_cooking_for_household',
    'Frequency_of_nail_cutting_of_mother',
    'Toilet_facility_shared_with_other_households',
    'Water_treatment_method',
    'Principal_type_of_toilet_facility_used_by_household_members',
    'Principal_source_of_household_drinking_water'
]
sdf = df.loc[:, sanitcols]
sdf.columns = sdf.columns.str.replace('Washing_-_', '')
sdf.to_csv('../results/sanitation.tsv', sep='\t')
df = df.loc[:, ~df.columns.isin(sanitcols)]

# Define and extract household-related columns
householdcols = df.columns[df.columns.str.contains('Household_-_')].tolist() + [
    'Members_in_household',
    'Number_of_years_lived_in_current_household',
    'Number_of_rooms_in_current_household',
    'Number_of_people_usually_sleeping_in_household',
    'Maid_working_in_household',
    'Household_food_availability'
]
hdf = df.loc[:, householdcols]
hdf.columns = hdf.columns.str.replace('Household_-_','')
hdf.columns = hdf.columns.str.replace('Table','Tabletop')
hdf.columns = hdf.columns.str.replace('/', '_')
hdf.to_csv('../results/household.tsv', sep='\t')
df = df.loc[:, ~df.columns.isin(householdcols)]

# Define and extract family-related columns
familycols = [
    'Number_of_living_children',
    'Birth_order_of_enrolled_child_among_live_births',
    'Number_of_siblings_under_five_years',
    'Family_type',
    'Language'
]
fdf = df.loc[:, familycols]
fdf.to_csv('../results/family.tsv', sep='\t')
df = df.loc[:, ~df.columns.isin(familycols)]

# Define and extract education-related columns
educationcols = [
    'Fathers_Educational_attainment',
    'Years_of_fathers_education',
    'Mothers_Educational_attainment',
    'Years_of_mothers_education',
    'Fathers_occupation',
    'Mothers_occupation',
    'Other_fathers_occupation',
    'Family_owns_the_home_they_live_in'
]
edf = df.loc[:, educationcols]
edf.to_csv('../results/education.tsv', sep='\t')
df = df.loc[:, ~df.columns.isin(educationcols)]

# Define and extract media consumption-related columns
mediacols = [
    'Number_of_mobile_phone_users_in_household',
    'Reads_the_newspaper',
    'Listens_to_or_watches_Radio_or_TV',
    'Uses_social_media'
]
mdf = df.loc[:, mediacols]
mdf.to_csv('../results/media_consumption.tsv', sep='\t')
df = df.loc[:, ~df.columns.isin(mediacols)]

# Define and extract economic columns
economiccols = df.columns[df.columns.str.contains('taka')].tolist()
ecdf = df.loc[:, economiccols]
ecdf.columns = ecdf.columns.str.replace('_(taka)','').str.replace('(','').str.replace(')','').str.replace(',','_')
ecdf.to_csv('../results/economics.tsv', sep='\t')
df = df.loc[:, ~df.columns.isin(economiccols)]

# Save meta
df.to_csv('../results/premeta.tsv', sep='\t')
