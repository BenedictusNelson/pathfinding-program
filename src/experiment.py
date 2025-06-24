
"""
Pathfinding Algorithm Experiment Runner

This module handles running pathfinding experiments, timing algorithms,
and generating performance data for analysis.
"""

import time
import csv
import numpy as np
import math
from pathlib import Path
from PIL import Image
from .algorithms import astar, uniform_clusters, region_grow, build_graph

def run_astar(grid, s, g):
    """Run A* algorithm and measure performance."""
    t0 = time.perf_counter()
    _, cost = astar(grid, s, g)
    return (time.perf_counter() - t0) * 1000, cost, math.nan

def run_hier(grid, s, g, clusters):
    """Run hierarchical pathfinding algorithm."""
    G, node_map, cl_of = build_graph(grid, clusters)
    if not node_map:
        return math.inf, math.inf, 0
    
    # Find nearest entrance points to start and goal
    s_ent = min(node_map, key=lambda c: abs(c[0]-s[0])+abs(c[1]-s[1]))
    g_ent = min(node_map, key=lambda c: abs(c[0]-g[0])+abs(c[1]-g[1]))
    
    # Run Dijkstra on the hierarchical graph
    import heapq
    pq = [(0, node_map[s_ent])]
    dist = {node_map[s_ent]: 0}
    
    while pq:
        d, u = heapq.heappop(pq)
        if u == node_map[g_ent]: 
            break
            
        # Get neighbors from networkx graph
        for v in G.neighbors(u):
            edge_data = G[u][v]
            nd = d + edge_data['w']
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    
    final_cost = dist.get(node_map[g_ent], math.inf)
    return final_cost, final_cost, G.number_of_nodes()

def batch(map_png, out_csv, n_pairs=50):
    """
    Run batch experiments on a map file.
    
    Args:
        map_png: Path to PNG map file
        out_csv: Path to output CSV file
        n_pairs: Number of start-goal pairs to test (default: 50)
    """
    grid = np.asarray(Image.open(map_png).convert("1"), dtype=bool)
    pts = np.argwhere(grid)
    np.random.shuffle(pts)
    pairs = [(tuple(pts[i]), tuple(pts[i+1])) for i in range(0, 2*n_pairs, 2)]
    uni = uniform_clusters(grid)
    ada = region_grow(grid)
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['alg', 'time_ms', 'nodes', 'cost'])
        for s, g in pairs:
            t, c, n = run_astar(grid, s, g)
            w.writerow(['A*', t, n, c])
            t, c, n = run_hier(grid, s, g, uni)
            w.writerow(['HPA*', t, n, c])
            t, c, n = run_hier(grid, s, g, ada)
            w.writerow(['AHPA*', t, n, c])
    print('Finished', map_png)
