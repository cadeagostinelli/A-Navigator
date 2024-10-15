This repository implements the A* algorithm, a pathfinding and graph traversal algorithm used to find the shortest
path between nodes in a weighted graph. The algorithm combines the strengths of Dijkstra's algorithm and 
Greedy Best-First Search by utilizing a heuristic function that estimates the cost to reach the goal from
the current node. This allows A* to efficiently prioritize paths that are likely to lead to the goal, 
making it suitable for applications in navigation systems, AI, and robotics.

The algorithm operates on a city graph represented as an adjacency list, where each node corresponds to an 
intersection, and edges represent the connections between them with associated costs. A graphical interface
built with Pygame visualizes the search process, displaying the explored paths and the final route from the
starting point to the destination. This implementation provides a clear demonstration of how the A* algorithm
navigates through a graph and constructs the optimal path based on the defined heuristic.
