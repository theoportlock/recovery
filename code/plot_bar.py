#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def parse_args():
    parser = argparse.ArgumentParser(description='Horizontal bar plot from coefficients.')
    parser.add_argument('input', help='Input TSV file with columns coef and filename')
    parser.add_argument('-o', '--output', required=True, help='Output path for the SVG file')
    return parser.parse_args()

def plot_horizontal_bar(df, output_path):
    # Sort by coef
    df = df.sort_values('coef', ascending=True)

    # Set up the figure
    plt.figure(figsize=(6, max(4, len(df) * 0.15)))  # dynamic height
    ax = sns.barplot(
        x='coef',
        y=df.index,
        hue='filename',
        data=df,
        dodge=False,
        palette='tab10',
        orient='h'
    )

    ax.set_xscale('symlog')  # <-- Symmetric log scale on x-axis

    plt.xlabel('Coefficient (symlog scale)')
    plt.ylabel('Entry')
    plt.title('Horizontal Barplot of Coefficients by Filename')
    plt.legend(title='Filename', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Make sure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the plot as SVG
    plt.savefig(output_path, format='svg')
    plt.close()
    print(f"Plot saved to {output_path}")

def main():
    args = parse_args()
    
    # Load data
    df = pd.read_csv(args.input, sep='\t', index_col=0)

    # Call the plotting function
    plot_horizontal_bar(df, args.output)

if __name__ == '__main__':
    main()
