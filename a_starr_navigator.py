class Node:
  # Initialize our node with necessary attributes
  def __init__(self, name, g=0, h=0):
      # Name of the node (intersection)
      self.name = name  
      # Cost from start to current node
      self.g = g 
      # Heuristic cost from current node to goal 
      self.h = h  
      # Total cost
      self.f = g + h
      # To reconstruct the path  
      self.parent = None  

# This is where we can implement and test different heuristics that will
# be used in our A* algorithm
def heuristic(node_name, goal_name, positions):
  x1, y1 = positions[node_name]
  x2, y2 = positions[goal_name]
  # Using Manhattan distance
  return abs(x1 - x2) + abs(y1 - y2)

# A* algorithm implementation. This reflects the pseudocode given in slides,
# but is adapted to our city graph node layout
def a_star(start_name, goal_name, graph, positions):
  # Define the starting node and the goal node
  start_node = Node(start_name)
  goal_node = Node(goal_name)

  # Nodes to be evaluated
  open_list = []
  # Nodes already evaluated  
  closed_list = []  

  open_list.append(start_node)

  while open_list:
      # Get the node in open_list with the lowest cost (g + h)
      current_node = min(open_list, key=lambda o: o.f)

      # If the current node is the goal, reconstruct and return the path
      if current_node.name == goal_node.name:
          return reconstruct_path(current_node)

      # Remove current node from open list
      open_list.remove(current_node) 
      # Add current node to closed list 
      closed_list.append(current_node)  

      # Evaluate each neighbor of the current node
      for neighbor_name, weight in graph[current_node.name].items():
          # Skip neighbors that have already been evaluated
          if neighbor_name in [n.name for n in closed_list]:
              continue

          # Calculate the cost from the start node to this neighbor
          neighbor = Node(neighbor_name, current_node.g + weight)
          # Estimate the cost to reach the goal using our heuristic approach
          neighbor.h = heuristic(neighbor_name, goal_name, positions)
          # Total cost 
          neighbor.f = neighbor.g + neighbor.h 
          # Set the parent for path reconstruction
          neighbor.parent = current_node  

          # If the neighbor is not in the open list, add it for evaluation
          if neighbor not in open_list:
              open_list.append(neighbor)

  # If no path is found
  return None  

# Reconstruct path function to trace back path and return reversed list (our final path)
def reconstruct_path(node):
  path = []
  while node:
      path.append(node.name)
      node = node.parent
  # Return reversed path
  return path[::-1]
