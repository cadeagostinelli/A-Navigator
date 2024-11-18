import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # Use software rendering to avoid driver issues

import pygame
import time
from a_starr_navigator import a_star

# Define the city graph and positions
city_graph = {
    'A': {'B': 2, 'C': 4, 'D': 7},
    'B': {'A': 2, 'E': 1, 'F': 5},
    'C': {'A': 4, 'G': 3, 'H': 8},
    'D': {'A': 7, 'I': 2, 'J': 6},
    'E': {'B': 1, 'K': 4},
    'F': {'B': 5, 'L': 3, 'M': 6},
    'G': {'C': 3, 'N': 7},
    'H': {'C': 8, 'O': 5},
    'I': {'D': 2, 'P': 4},
    'J': {'D': 6, 'Q': 3},
    'K': {'E': 4, 'R': 2},
    'L': {'F': 3, 'S': 6},
    'M': {'F': 6, 'T': 8},
    'N': {'G': 7, 'U': 5},
    'O': {'H': 5, 'V': 9},
    'P': {'I': 4, 'W': 3},
    'Q': {'J': 3, 'X': 2},
    'R': {'K': 2, 'Y': 1},
    'S': {'L': 6, 'Z': 4},
    'T': {'M': 8},
    'U': {'N': 5},
    'V': {'O': 9},
    'W': {'P': 3},
    'X': {'Q': 2},
    'Y': {'R': 1},
    'Z': {'S': 4}
}

positions = {
    'A': (50, 50), 'B': (150, 50), 'C': (250, 50), 'D': (350, 50),
    'E': (100, 150), 'F': (200, 150), 'G': (300, 150), 'H': (400, 150),
    'I': (450, 50), 'J': (550, 50),
    'K': (100, 250), 'L': (200, 250), 'M': (300, 250),
    'N': (350, 250), 'O': (450, 250),
    'P': (450, 150), 'Q': (550, 150),
    'R': (100, 350), 'S': (200, 350), 'T': (300, 350),
    'U': (350, 350), 'V': (450, 350),
    'W': (450, 250), 'X': (550, 250),
    'Y': (100, 450), 'Z': (200, 450)
}

# Dijkstra's algorithm implementation
def dijkstra(start_name, goal_name, graph):
    distances = {node: float('inf') for node in graph}
    distances[start_name] = 0
    previous_nodes = {node: None for node in graph}
    nodes = list(graph.keys())

    while nodes:
        current_node = min(nodes, key=lambda node: distances[node])
        if distances[current_node] == float('inf'):
            break

        for neighbor, weight in graph[current_node].items():
            alt = distances[current_node] + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous_nodes[neighbor] = current_node

        nodes.remove(current_node)

    path = []
    current = goal_name
    while previous_nodes[current]:
        path.insert(0, current)
        current = previous_nodes[current]
    if path:
        path.insert(0, start_name)

    return path

# Function to draw the graph and path on the Pygame window
def draw_graph(graph, positions, screen, offset_x, font, start=None, goal=None, path=None):
    screen.fill(WHITE, (offset_x, 0, 400, 700))

    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = positions[node]
        for neighbor, weight in neighbors.items():
            x2, y2 = positions[neighbor]
            pygame.draw.line(screen, BLUE, (x1 + offset_x, y1), (x2 + offset_x, y2), 2)

    # Draw nodes
    for node, pos in positions.items():
        x, y = pos
        color = GREEN if node == start else RED if node == goal else BLUE
        pygame.draw.circle(screen, color, (x + offset_x, y), 20)
        text = font.render(node, True, WHITE)
        screen.blit(text, (x + offset_x - 10, y - 10))

    # Draw path if exists
    if path:
        for i in range(len(path) - 1):
            x1, y1 = positions[path[i]]
            x2, y2 = positions[path[i + 1]]
            pygame.draw.line(screen, (255, 0, 0), (x1 + offset_x, y1), (x2 + offset_x, y2), 5)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((800, 900))  # Increased height for all text
pygame.display.set_caption('A* vs Dijkstra Pathfinding')
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Initialize font
font = pygame.font.Font(None, 36)

# Measure execution times
start_time = time.perf_counter()
path_a_star = a_star('A', 'Z', city_graph, positions)
time_a_star = time.perf_counter() - start_time
time_a_star_micro = time_a_star * 1_000_000  # Convert to microseconds

start_time = time.perf_counter()
path_dijkstra = dijkstra('A', 'Z', city_graph)
time_dijkstra = time.perf_counter() - start_time
time_dijkstra_micro = time_dijkstra * 1_000_000  # Convert to microseconds

# Calculate time difference
time_diff_micro = abs(time_a_star_micro - time_dijkstra_micro)
time_diff_seconds = abs(time_a_star - time_dijkstra)
relative_diff_percent = (time_diff_micro / max(time_a_star_micro, time_dijkstra_micro)) * 100

# Determine which is faster
faster_algorithm = "A*" if time_a_star < time_dijkstra else "Dijkstra"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw A* results (left half)
    draw_graph(city_graph, positions, screen, 0, font, start='A', goal='Z', path=path_a_star)

    # Draw Dijkstra results (right half)
    draw_graph(city_graph, positions, screen, 400, font, start='A', goal='Z', path=path_dijkstra)

    # Display times and results
    screen.fill(WHITE, (0, 700, 800, 200))  # Ensure the bottom section is white
    screen.blit(font.render(f"A*: {time_a_star:.10f} sec ({time_a_star_micro:.2f} μs)", True, BLACK), (50, 720))
    screen.blit(font.render(f"Dijkstra: {time_dijkstra:.10f} sec ({time_dijkstra_micro:.2f} μs)", True, BLACK), (50, 760))
    screen.blit(font.render(f"Difference: {time_diff_seconds:.10f} sec ({time_diff_micro:.2f} μs)", True, BLACK), (50, 800))
    screen.blit(font.render(f"Relative Difference: {relative_diff_percent:.2f}%", True, BLACK), (50, 840))
    screen.blit(font.render(f"Faster Algorithm: {faster_algorithm}", True, BLACK), (50, 880))

    pygame.display.flip()

    # Save the screen as an image
    pygame.image.save(screen, "output.png")
    running = False  # Exit the loop after saving the image
