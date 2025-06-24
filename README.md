# Pathfinding Algorithms Comparison

A Python implementation comparing different pathfinding algorithms on various map types. This project benchmarks A*, Hierarchical Pathfinding A* (HPA*), and Adaptive Hierarchical Pathfinding A* (AHPA*) algorithms.

## Features

- **Multiple Pathfinding Algorithms:**
  - A* (A-star) - Classic pathfinding algorithm
  - HPA* - Hierarchical Pathfinding with uniform clustering
  - AHPA* - Adaptive Hierarchical Pathfinding with region growing

- **Map Types:**
  - Labyrinth/Maze maps
  - Mixed terrain maps
  - Open area maps

- **Performance Metrics:**
  - Execution time (milliseconds)
  - Path cost
  - Number of nodes explored

## Requirements

### With Full Dependencies (Recommended)
```
numpy>=1.20.0
pillow>=8.0.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
networkx>=2.6.0
```

### Minimal Dependencies (Fallback Mode)
The project includes stub implementations that allow it to run without external dependencies, though with limited functionality.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pathfinding-program
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or for minimal installation:
```bash
# The program will run with stub implementations if dependencies are not available
python main.py
```

## Usage

1. Place your map images (PNG format) in the `maps/` directory
2. Run the comparison:
```bash
python main.py
```

3. Results will be saved in the `output/` directory:
   - CSV files with detailed performance data
   - Performance summary (text or chart depending on available libraries)

## Project Structure

```
pathfinding-program/
├── main.py                 # Main execution script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── algorithms.py      # Pathfinding algorithm implementations
│   ├── experiment.py      # Experimental setup and benchmarking
│   └── plots.py          # Visualization and reporting
├── maps/                  # Input map images
│   ├── labyrinth.png
│   ├── mixed.png
│   └── open_area.png
└── output/               # Generated results
    ├── *.csv            # Performance data
    └── performance_*    # Summary charts/reports
```

## Map Format

Maps should be PNG images where:
- **White pixels** (255) represent walkable areas
- **Black pixels** (0) represent obstacles/walls

## Output

The program generates:
1. **CSV files** for each map with columns:
   - `alg`: Algorithm name
   - `time_ms`: Execution time in milliseconds
   - `nodes`: Number of nodes explored
   - `cost`: Path cost

2. **Performance summary** (chart if matplotlib available, text otherwise)

## Algorithms

### A* (A-star)
Classic pathfinding algorithm using Manhattan distance heuristic.

### HPA* (Hierarchical Pathfinding A*)
Divides the map into uniform clusters and creates a hierarchical graph for faster pathfinding on large maps.

### AHPA* (Adaptive Hierarchical Pathfinding A*)
Uses region growing to create adaptive clusters based on map topology.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Performance Notes

- A* is generally fastest for small to medium maps
- HPA* shows benefits on large, complex maps
- AHPA* is experimental and may need tuning for optimal performance

## Troubleshooting

If you encounter import errors, the program will automatically fall back to stub implementations. For full functionality, ensure all dependencies are installed.
