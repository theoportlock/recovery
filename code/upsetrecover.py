import pandas as pd
import metatoolkit.functions as f
import upsetplot
import matplotlib.pyplot as plt
from upsetplot import UpSet
import numpy as np

# Load data
df = f.load('allrecd')

# Set up the plot
f.setupplot(figsize=(4, 4))

# Calculate counts and percentages
counts = df.sum(axis=1).value_counts().sort_index()
total = counts.sum()
percentages = counts / total * 100

# Plot the histogram
fig, ax = plt.subplots()
counts.plot.barh(ax=ax)

# Add the secondary x-axis for percentages
ax_percent = ax.twiny()
ax_percent.set_xlim(ax.get_xlim())

# Define interval and labels for the top axis
interval = 9
top_ticks = np.arange(0, counts.max() + 1, interval)
top_labels = [f"{(tick / total) * 100:.1f}%" for tick in top_ticks]

# Set the ticks and labels on the secondary x-axis
ax_percent.set_xticks(top_ticks)
ax_percent.set_xticklabels(top_labels)

# Label the axes
ax.set_xlabel('Count')
ax_percent.set_xlabel('Percentage of Participants Recovered')

# Save the figure
f.savefig('recoverhist')

'''
df = f.load('allrecd')

# Convert the relevant columns to boolean for presence/absence analysis, ignoring NaN values
# Replace NaN with False, as we are focusing only on actual counts of True values
df_bool = df.fillna(False).set_index('ID').astype(bool)

# Compute the count of each unique combination of categories
# The sum for each combination will provide the input for the UpSet plot
combinations_count = df_bool.groupby(list(df_bool.columns)).size()

# Plot the UpSet plot for shared counts
upset_plot = UpSet(combinations_count, subset_size='count')
upset_plot.plot()

# Show plot
plt.show()
'''
