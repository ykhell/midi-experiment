#!/usr/bin/env python3
import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (600, 600)
CIRCLE_RADIUS = 200
NUM_POINTS = 12
FONT_SIZE = 36
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Function to draw text at a given position
def draw_text(text, position, color=BLACK):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

# Function to calculate the position of points around a circle
def calculate_circle_points(center, radius, num_points):
    circle_points = []
    for i in range(num_points):
        angle = math.radians(360 / num_points * i)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        circle_points.append((x, y))
    return circle_points

# Initialize the screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Circular GUI")

# Main loop
running = True
selected_points = set()  # To keep track of selected points
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                # Check if the mouse click is inside any circle
                for i, point in enumerate(circle_points):
                    if math.hypot(mouse_pos[0] - point[0], mouse_pos[1] - point[1]) <= 40:
                        if i in selected_points:
                            selected_points.remove(i)
                        else:
                            selected_points.add(i)

    # Clear the screen
    screen.fill(WHITE)

    # Calculate the positions of points around a circle
    center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)
    circle_points = calculate_circle_points(center, CIRCLE_RADIUS, NUM_POINTS)

    # Draw circles and numbers
    for i, point in enumerate(circle_points):
        color = GREEN if i in selected_points else GRAY
        pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), 40)
        draw_text(str(i+1), point, BLACK)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
