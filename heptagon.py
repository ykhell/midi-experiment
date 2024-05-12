#!/usr/bin/env python3
import pygame
import pygame.midi
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (600, 800)
NUM_KEYS = 12
NUM_NOTES = 7
CIRCLE_RADIUS = 20
CIRCLE_GAP = 10
FONT_SIZE = 18
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

# Function to calculate the position of circles in a grid
def calculate_circle_positions(start_x, start_y, num_rows, num_columns, radius, gap):
    circle_positions = []
    for row in range(num_rows):
        for col in range(num_columns):
            x = start_x + col * (2 * radius + gap)
            y = start_y + row * (2 * radius + gap)
            circle_positions.append((x, y))
    return circle_positions

# Initialize Pygame MIDI
pygame.midi.init()

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
pygame.display.set_caption("Grid of Circles with MIDI")

# Main loop
running = True
selected_notes = set()  # To keep track of selected notes
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Calculate the positions of circles in a grid
    circle_positions = calculate_circle_positions(50, 50, NUM_KEYS, NUM_NOTES, CIRCLE_RADIUS, CIRCLE_GAP)

    # Draw circles and numbers
    for key in range(NUM_KEYS):
        for note in range(NUM_NOTES):
            idx = key * NUM_NOTES + note
            position = circle_positions[idx]
            color = GREEN if idx in selected_notes else GRAY
            pygame.draw.circle(screen, color, position, CIRCLE_RADIUS)
            draw_text(str(note + 1), position, BLACK)

    # Check for MIDI input
    if midi_input.poll():
        midi_events = midi_input.read(10)  # Read up to 10 MIDI events at once
        for midi_event in midi_events:
            status, note, velocity, _ = midi_event[0]
            note_name = (note - 24) % 12
            if status & 0xF0 == 0x90:  # Note On event
                if note_name in selected_notes:
                    print(f"Note {note_name} played with velocity {velocity}")
            elif status & 0xF0 == 0x80:  # Note Off event
                if note_name in selected_notes:
                    print(f"Note {note_name} released")

    # Update the display
    pygame.display.flip()

# Close MIDI input
midi_input.close()

# Quit Pygame MIDI
pygame.midi.quit()

# Quit Pygame
pygame.quit()
