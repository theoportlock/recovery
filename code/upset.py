import pandas as pd
from upsetplot import UpSet, from_indicators
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

# Get file path from user
file_path = '../results/allrecd.tsv'

# Read and process data
df = pd.read_csv(file_path, sep="\t")
for col in df.columns[1:]:  # Convert all columns except ID to boolean
    df[col] = df[col].astype(bool)

# Generate sorted upset data with top 20 interactions
upset_data = from_indicators(df.columns[1:], df)

# Generate and show plot
plt.figure(figsize=(12, 7))
UpSet(
    upset_data,
    sort_by="cardinality",
    show_percentages=True,
    min_subset_size=1
).plot()
plt.title("Top 20 Co-Recovery Combinations")
plt.show()

