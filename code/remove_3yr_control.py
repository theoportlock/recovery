#!/usr/bin/env python

import pandas as pd
import sys
from pathlib import Path

# Read input
input_file = Path(sys.argv[1])
df = pd.read_csv(input_file, index_col=0, sep='\t')

# Filter
df = df.loc[df.index.str[3] != '3']

# Prepare output path
output_dir = input_file.parent
output_file = output_dir / f"{input_file.stem}noyr3.tsv"

# Save
df.to_csv(output_file, sep="\t", index=True)
