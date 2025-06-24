
"""
Visualization and Plotting Functions

This module contains functions for creating performance comparison charts
and visualizing pathfinding algorithm results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style('whitegrid')

def bar_performance(csv_paths, out_png='performance_bar.png'):
    """
    Create a bar chart showing performance comparison of pathfinding algorithms.
    
    Args:
        csv_paths: List of paths to CSV files containing performance data
        out_png: Output path for the generated chart image
    """
    df = pd.concat([pd.read_csv(p).assign(map=Path(p).stem) for p in csv_paths])
    agg = df.groupby(['map', 'alg'])['time_ms'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=agg, x='map', y='time_ms', hue='alg')
    plt.title('Pathfinding Algorithm Performance Comparison')
    plt.xlabel('Map Type')
    plt.ylabel('Average Search Time (ms)')
    plt.legend(title='Algorithm')
    plt.tight_layout()
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Performance chart saved to: {out_png}")
