
#!/usr/bin/env python3
"""
Pathfinding Algorithm Comparison Tool

This script runs performance comparisons between different pathfinding algorithms
on various map types and generates performance analysis charts.

Usage:
    python main.py

Output:
    - CSV files with detailed performance metrics in output/ directory
    - Performance comparison chart as PNG image
"""

from pathlib import Path
from src.experiment import batch
from src.plots import bar_performance


def main():
    """Main function to run pathfinding algorithm comparison experiments."""
    base = Path(__file__).parent
    
    # Create output directory if it doesn't exist
    output_dir = base / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Find all PNG map files
    maps = list((base / 'maps').glob('*.png'))
    
    if not maps:
        print("No map files found in maps/ directory!")
        print("Please add PNG image files to the maps/ directory.")
        return
    
    print(f"Found {len(maps)} map(s) to process:")
    for map_file in maps:
        print(f"  - {map_file.name}")
    print()
    
    # Run experiments on each map
    csvs = []
    for map_file in maps:
        print(f"Processing {map_file.name}...")
        out_csv = output_dir / f'{map_file.stem}.csv'
        batch(str(map_file), str(out_csv))
        csvs.append(str(out_csv))
        print(f"  ✓ Results saved to {out_csv.name}")
    
    # Generate performance comparison chart
    if csvs:
        chart_path = output_dir / 'performance_comparison.png'
        print(f"\nGenerating performance comparison chart...")
        try:
            bar_performance(csvs, str(chart_path))
            print(f"  ✓ Chart saved to {chart_path.name}")
        except Exception as e:
            print(f"  ✗ Error generating chart: {e}")
            print("  → Make sure all required packages are installed (pip install -r requirements.txt)")
    
    print(f"\n🎉 All done! Check the output/ directory for results.")


if __name__ == "__main__":
    main()
