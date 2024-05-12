#!/usr/bin/env python3

import pygame
import pygame.midi
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (600, 600)
CIRCLE_RADIUS = 200
# NUM_POINTS = 7
NUM_POINTS = 12
FONT_SIZE = 36
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
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

# Initialize Pygame MIDI
pygame.midi.init()

c_major = [0,2,4,5,7,9,11]

# Print MIDI input devices
print("Available MIDI input devices:")
for i in range(pygame.midi.get_count()):
    device_info = pygame.midi.get_device_info(i)
    if device_info[2] == 1:  # Check if it's an input device
        print(f"Input Device {i}: {device_info[1].decode()}")

# Open MIDI input device
input_device_id = 0  # Change this to the appropriate device ID based on your MIDI keyboard
midi_input = pygame.midi.Input(input_device_id)

# Initialize the screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Test")

# Main loop
running = True
selected_points = set()  # To keep track of selected points
while running:
    if midi_input.poll():
        midi_events = midi_input.read(10)  # Read up to 10 MIDI events at once
        for midi_event in midi_events:
            status, note, velocity, _ = midi_event[0]
            note_name = (note - 24)% 12
            # if note_name in c_major:
            #     note_name = c_major.index(note_name)
            # else:
            #     continue

            if status & 0xF0 == 0x90:  # Note On event
                if velocity == 0:
                    print(f"Note {note_name} released")
                    if note_name not in selected_points:
                        continue
                    selected_points.remove(note_name)
                else:
                    print(f"Note {note_name} played with velocity {velocity}")
                    if note_name in selected_points:
                        continue
                    selected_points.add(note_name)
            elif status & 0xF0 == 0x80: # Note Off event
                print(f"Note {note_name} released")
                if note_name not in selected_points:
                    continue
                selected_points.remove(note_name)

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
                            print(f"selected {i}")
                            selected_points.remove(i)
                        else:
                            print(f"unselected {i}")
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

# Close MIDI input
midi_input.close()

# Quit Pygame MIDI
pygame.midi.quit()

# Quit Pygame
pygame.quit()
