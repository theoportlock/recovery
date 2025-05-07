import pandas as pd
import seaborn as sns
from metatoolkit.change import change

# Read the data
df = pd.read_csv('../results/filtered/surveillance.tsv', sep='\t', index_col=0)
meta = pd.read_csv('../results/filtered/meta.tsv', sep='\t', index_col=0)

# Filter out rows where no days_to_recovery is available
df.dropna(inplace=True)

joined = df.join(meta)

chan = change(df, meta.select_dtypes(include=[object]))
joined.corr
