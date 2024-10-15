import pygame
from a_star_navigator import a_star

# Use a graph to represent our city, and the connected nodes that are our intersections
# Example graph representation using an adjacency list
city_graph = {
    'A': {'B': 1, 'C': 4, 'H': 2},
    'B': {'A': 1, 'C': 2, 'D': 5, 'I': 2},
    'C': {'A': 4, 'B': 2, 'D': 1, 'F': 2},
    'D': {'B': 5, 'C': 1, 'E': 3, 'J': 4},
    'E': {'D': 3, 'F': 2, 'G': 1},
    'F': {'C': 2, 'E': 2, 'G': 3},
    'G': {'F': 3, 'E': 1},
    'H': {'A': 2, 'B': 3},
    'I': {'B': 2, 'J': 3},
    'J': {'D': 4, 'I': 3}
}

# Sample positions for intersections (x, y coordinates)
positions = {
    'A': (100, 100),
    'B': (200, 100),
    'C': (300, 100),
    'D': (200, 200),
    'E': (300, 200),
    'F': (300, 300),
    'G': (200, 300),
    'H': (100, 150),
    'I': (200, 250),
    'J': (300, 250)
}

# Function to draw the graph and path on the Pygame window
def draw_graph(graph, start=None, goal=None, path=None):
    screen.fill(WHITE)
    
    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = positions[node]
        for neighbor, weight in neighbors.items():
            x2, y2 = positions[neighbor]
            pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2), 2)

    # Draw nodes
    for node, pos in positions.items():
        color = GREEN if node == start else RED if node == goal else BLUE
        pygame.draw.circle(screen, color, pos, 20)
        text = font.render(node, True, WHITE)
        screen.blit(text, (pos[0] - 10, pos[1] - 10))

    # Draw path if exists
    if path:
        for i in range(len(path) - 1):
            x1, y1 = positions[path[i]]
            x2, y2 = positions[path[i + 1]]
            pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x2, y2), 5)

    pygame.display.flip()

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('A* Traffic Navigator')
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Main loop
font = pygame.font.Font(None, 36)
start_node = 'A'
goal_node = 'E'
path = a_star(start_node, goal_node, city_graph, positions)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_graph(city_graph, start=start_node, goal=goal_node, path=path)
    clock.tick(60)

pygame.quit()
