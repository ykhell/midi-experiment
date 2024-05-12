#!/usr/bin/env python3

import pygame
import pygame.midi
import math
from enum import Enum

# Initialize Pygame
pygame.init()

# UI Constants
WINDOW_SIZE = (1200, 1200)
CIRCLE_RADIUS = 46
SMALL_CIRCLE_RADIUS = 20
NUM_POINTS = 7
NUM_CIRCLES = 12
FONT_SIZE = 24
BACKGROUND = (22, 22, 24)
FOREGROUND = (255, 255, 255)
MID = (50, 50, 50)
HIGHLIGHT = (0, 200, 30)
CIRCLE_MARGIN = 60

# Notes
C  = [0, "C"]
Cs = [1, "C#"]
Db = [1, "Db"]
D  = [2, "D"]
Ds = [3, "D#"]
Eb = [3, "Eb"]
E  = [4, "E"]
Es  = [5, "E#"]
F  = [5, "F"]
Fs = [6, "F#"]
Gb = [6, "Gb"]
G  = [7, "G"]
Gs = [8, "G#"]
Ab = [8, "Ab"]
A  = [9, "A"]
As = [10, "A#"]
Bb = [10, "Bb"]
B  = [11, "B"]
Cb  = [11, "Cb"]
Bs  = [0, "B#"]

## Major Scales
c_major  = [C, D, E, F, G, A, B]
cs_major = [Cs, Ds, Es, Fs, Gs, As, Bs]
d_major  = [D, E, Fs, G, A, B, Cs]
eb_major = [Eb, F, G, Ab, Bb, C, D]
e_major  = [E, Fs, Gs, A, B, Cs, Ds]
f_major  = [F, G, A, Bb, C, D, E]
fs_major = [Fs, Gs, As, B, Cs, Ds, Es]
g_major  = [G, A, B, C, D, E, Fs]
ab_major = [Ab, Bb, C, Db, Eb, F, G]
a_major  = [A, B, Cs, D, E, Fs, Gs]
bb_major = [Bb, C, D, Eb, F, G, A]
b_major  = [B, Cs, Ds, E, Fs, Gs, As]

## Minor Scales
c_minor  = [C, D, Eb, F, G, Ab, Bb]
cs_minor = [Cs, Ds, E, Fs, Gs, A, B]
d_minor  = [D, E, F, G, A, Bb, C]
eb_minor = [Eb, F, Gb, Ab, Bb, Cb, Db]
e_minor  = [E, Fs, G, A, B, C, D]
f_minor  = [F, G, Ab, Bb, C, Db, Eb]
fs_minor = [Fs, Gs, A, B, Cs, D, E]
g_minor  = [G, A, Bb, C, D, Eb, F]
gs_minor = [Gs, As, B, Cs, Ds, E, Fs]
a_minor  = [A, B, C, D, E, F, G]
b_minor  = [Bb, C, Db, Eb, F, Gb, Ab]
b_minor  = [B, Cs, D, E, Fs, G, A]

scales = [c_major, cs_major, d_major, eb_major, e_major, f_major, fs_major, g_major, ab_major, a_major, bb_major, b_major, c_minor, cs_minor, d_minor, eb_minor, e_minor, f_minor, fs_minor, g_minor, gs_minor, a_minor, b_minor, b_minor]
# minor_scales = [c_minor, cs_minor, d_minor, eb_minor, e_minor, f_minor, fs_minor, g_minor, gs_minor, a_minor, b_minor, b_minor]

# UI Functions
# Function to draw text at a given position
def draw_text(text, position, color=FOREGROUND):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

# Function to calculate the position of points around a circle
# def calculate_circle_points(center, radius, num_points):
#     circle_points = []
#     for i in range(num_points):
#         angle = math.radians(360 / num_points * i)
#         x = center[0] + radius * math.cos(angle)
#         y = center[1] + radius * math.sin(angle)
#         circle_points.append((x, y))
#     return circle_points

# def calculate_circle_points(num_points, index, total_circles, window_width, window_height):
#     num_circles_per_row = int(math.sqrt(total_circles))
#     num_rows = total_circles // num_circles_per_row + (total_circles % num_circles_per_row != 0)

#     # Calculate circle radius to fit circles within the window
#     min_dimension = min(window_width, window_height)
#     max_circles_per_row = min_dimension // (2 * CIRCLE_MARGIN)
#     circle_radius = min_dimension / (2 * max_circles_per_row)

#     circle_index_x = index % num_circles_per_row
#     circle_index_y = index // num_circles_per_row
#     circle_center_x = (2 * circle_radius + CIRCLE_MARGIN) * circle_index_x + circle_radius
#     circle_center_y = (2 * circle_radius + CIRCLE_MARGIN) * circle_index_y + circle_radius

#     circle_points = []
#     for i in range(num_points):
#         angle = math.radians(360 / num_points * i)
#         x = circle_center_x + circle_radius * math.cos(angle)
#         y = circle_center_y + circle_radius * math.sin(angle)
#         circle_points.append((x, y))
#     return circle_points


def calculate_circle_points(num_points, index, total_circles, window_width, window_height):
    # Calculate the number of rows and columns needed to fit all circles
    num_columns = int(math.sqrt(total_circles))
    num_rows = total_circles // num_columns + (total_circles % num_columns != 0)

    # Calculate the dimensions of each circle based on the available space
    circle_width = window_width / (2 * num_columns)
    circle_height = window_height / (2 * num_rows)
    circle_radius = min(circle_width, circle_height) / 2

    # Calculate the gap between circles
    circle_margin_x = (window_width - 2 * num_columns * circle_radius) / (2 * num_columns)
    circle_margin_y = (window_height - 2 * num_rows * circle_radius) / (2 * num_rows)

    # Calculate the position of the current circle
    circle_row = index // num_columns
    circle_col = index % num_columns
    circle_center_x = circle_margin_x + circle_radius + circle_col * (2 * circle_radius + circle_margin_x)
    circle_center_y = circle_margin_y + circle_radius + circle_row * (2 * circle_radius + circle_margin_y)

    # Calculate the points within the circle
    circle_points = []
    for i in range(num_points):
        angle = math.radians(360 / num_points * i)
        x = circle_center_x + circle_radius * math.cos(angle)
        y = circle_center_y + circle_radius * math.sin(angle)
        circle_points.append((x, y))

    return circle_points





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
    screen.fill(BACKGROUND)

    for i, scale in enumerate(scales):
        # Calculate the positions of points around a circle
        center = (WINDOW_SIZE[0] // NUM_CIRCLES + 10, WINDOW_SIZE[1] // NUM_CIRCLES + 10)
        circle_points = calculate_circle_points(NUM_POINTS, i, NUM_CIRCLES, 1200, 1200)

        # Draw circles and numbers
        for i, point in enumerate(circle_points):
            color = HIGHLIGHT if i in selected_points else MID
            pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), SMALL_CIRCLE_RADIUS)
            draw_text(scale[i][1], point, FOREGROUND)

    # Update the display
    pygame.display.flip()

# Close MIDI input
midi_input.close()

# Quit Pygame MIDI
pygame.midi.quit()

# Quit Pygame
pygame.quit()
