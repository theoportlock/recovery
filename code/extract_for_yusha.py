import pandas as pd

# Load data
df = pd.read_csv("../results/anthro.tsv", sep='\t', index_col=0)

# Dictionary where keys are indices, values are lists of timepoints
extract = {
    'LCC1008': [0, 52],
    'LCC1049': [0, 52],
    'LCC2038': [0, 52],
    'LCC2042': [0, 52],
}

# Initialize an empty list to collect results
filtered_rows = []

# Loop over extract dictionary
for index, timepoints in extract.items():
    # Filter rows where index matches and 'timepoint' column matches any of the specified values
    filtered_rows.append(df.loc[index][df.loc[index, 'timepoint'].isin(timepoints)])

# Concatenate filtered rows into a DataFrame
output = pd.concat(filtered_rows)

# Print or save output
print(output)

