"""
Pathfinding Algorithms Implementation

This module contains implementations of various pathfinding algorithms:
- A* (A-star) algorithm
- Hierarchical pathfinding with clustering
- Utility functions for grid processing and graph building
"""

"""
Pathfinding Algorithms Implementation

This module contains implementations of various pathfinding algorithms:
- A* (A-star) algorithm
- Hierarchical pathfinding with clustering
- Utility functions for grid processing and graph building
"""

import heapq
import math
import numpy as np
import networkx as nx

DIRS_4 = [(0,1), (1,0), (0,-1), (-1,0)]
DIRS_8 = DIRS_4 + [(1,1),(-1,1),(1,-1),(-1,-1)]

def manhattan(a, b):
    """Calculate Manhattan distance between two points."""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal, heur=manhattan):
    """
    A* pathfinding algorithm implementation.
    
    Args:
        grid: 2D numpy array where True represents walkable cells
        start: Tuple (x, y) representing start coordinates
        goal: Tuple (x, y) representing goal coordinates
        heur: Heuristic function (default: Manhattan distance)
    
    Returns:
        Tuple (path, cost) where path is list of coordinates and cost is total path cost
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    g = {start: 0}
    came = {}
    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur == goal:
            break
        for dx, dy in DIRS_4:
            nx_, ny_ = cur[0] + dx, cur[1] + dy
            if 0 <= nx_ < grid.shape[0] and 0 <= ny_ < grid.shape[1] and grid[nx_, ny_]:
                ng = g[cur] + 1
                if ng < g.get((nx_, ny_), math.inf):
                    g[(nx_, ny_)] = ng
                    f = ng + heur((nx_, ny_), goal)
                    heapq.heappush(open_set, (f, (nx_, ny_)))
                    came[(nx_, ny_)] = cur
    # reconstruct
    if goal not in came and goal not in g:
        # Goal not reachable
        return [], math.inf
    
    path = [goal]
    while path[-1] != start and path[-1] in came:
        path.append(came[path[-1]])
    
    if path[-1] != start:
        # Could not reach start from goal
        return [], math.inf
        
    path.reverse()
    return path, g.get(goal, math.inf)

def region_grow(grid):
    """
    Region growing algorithm for clustering connected walkable areas.
    
    Args:
        grid: 2D numpy array where True represents walkable cells
    
    Returns:
        List of clusters, where each cluster is a list of (x, y) coordinates
    """
    h, w = grid.shape
    visited = np.zeros_like(grid, bool)
    clusters = []
    for x in range(h):
        for y in range(w):
            if grid[x, y] and not visited[x, y]:
                q = [(x, y)]
                visited[x, y] = True
                current = []
                while q:
                    cx, cy = q.pop()
                    current.append((cx, cy))
                    for dx, dy in DIRS_4:
                        nx_, ny_ = cx + dx, cy + dy
                        if 0 <= nx_ < h and 0 <= ny_ < w and grid[nx_, ny_] and not visited[nx_, ny_]:
                            visited[nx_, ny_] = True
                            q.append((nx_, ny_))
                clusters.append(current)
    return clusters

def uniform_clusters(grid, size=15):
    """
    Create uniform grid-based clusters for hierarchical pathfinding.
    
    Args:
        grid: 2D numpy array where True represents walkable cells
        size: Size of each cluster (default: 15x15)
    
    Returns:
        List of clusters, where each cluster is a list of (x, y) coordinates
    """
    h, w = grid.shape
    clusters = []
    for i in range(0, h, size):
        for j in range(0, w, size):
            cells = [(x, y) for x in range(i, min(i+size, h))
                           for y in range(j, min(j+size, w)) if grid[x, y]]
            if cells:
                clusters.append(cells)
    return clusters

def entrances(grid, cluster_set):
    cell_set = set(cluster_set)
    H, W = grid.shape
    ent = []
    for x, y in cluster_set:
        for dx, dy in DIRS_4:
            nx_, ny_ = x + dx, y + dy
            if 0 <= nx_ < H and 0 <= ny_ < W and grid[nx_, ny_] and (nx_, ny_) not in cell_set:
                ent.append((x, y))
                break
    return ent

def build_graph(grid, clusters):
    G = nx.DiGraph()
    cluster_of = {}
    for idx, c in enumerate(clusters):
        for cell in c:
            cluster_of[cell] = idx
    node_map = {}
    # nodes
    for idx, c in enumerate(clusters):
        for e in entrances(grid, c):
            node_map[e] = len(node_map)
            G.add_node(node_map[e], cell=e, clu=idx)
    # intra edges
    for idx, c in enumerate(clusters):
        epoints = [e for e in entrances(grid, c)]
        for i in range(len(epoints)):
            for j in range(i+1, len(epoints)):
                p1, p2 = epoints[i], epoints[j]
                _, cost = astar(grid, p1, p2)
                G.add_edge(node_map[p1], node_map[p2], w=cost)
                G.add_edge(node_map[p2], node_map[p1], w=cost)
    # inter edges
    for (x, y), nid in node_map.items():
        for dx, dy in DIRS_4:
            nx_, ny_ = x + dx, y + dy
            if (nx_, ny_) in node_map and cluster_of[(x, y)] != cluster_of[(nx_, ny_)]:
                G.add_edge(nid, node_map[(nx_, ny_)], w=1)
    return G, node_map, cluster_of
