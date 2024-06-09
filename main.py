#!/usr/bin/env python3

import pygame
import time
import pygame.midi
import math
import copy

# Initialize Pygame
pygame.init()

# UI Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
CIRCLE_RADIUS = 46
SMALL_CIRCLE_RADIUS = 13
NUM_POINTS = 7
NUM_CIRCLES = 12
FONT_SIZE = 24
BACKGROUND = (0, 0, 0)
FOREGROUND = (180, 180, 180)
MID = (50, 50, 50)
HIGHLIGHTS = [
    (255, 244, 0),    #d0f400
    # (208, 238, 17), #d0ee11
    # (201, 229, 47), #c9e52f
    (166, 215, 91),   #a6d75b
    (118, 198, 143),  #76c68f
    (72, 181, 196),   #48b5c4
    (34, 167, 240),   #22a7f0
    (25, 132, 197),   #1984c5
    (17, 95, 154),    #115f9a
    (17, 70, 120),    #115f9a
    (17, 50, 80)      #115f9a
]


HIGHLIGHT_0 = (199, 245, 238)
HIGHLIGHT_1 = (0, 204, 195)  # Slightly less bright cyan
HIGHLIGHT_2 = (0, 153, 120)  # Medium cyan
HIGHLIGHT_3 = (0, 102, 80)  # Less bright cyan
HIGHLIGHT_4 = (80, 100, 200)    # Darker cyan
HIGHLIGHT_5 = (80, 100, 170)    # Darkest cyan
HIGHLIGHT_6 = (60, 70, 140)    # Darkest cyan
HIGHLIGHT_7 = (50, 50, 100)    # Darkest cyan

CIRCLE_MARGIN = 160
LARGE_CIRCLE_RADIUS = 240  # Adjust the 50 to provide some margin

# Notes
C  = [0, "C", 0]
Cs = [1, "C#", 0]
Db = [1, "Db", 0]
D  = [2, "D", 0]
Ds = [3, "D#", 0]
Eb = [3, "Eb", 0]
E  = [4, "E", 0]
Fb  = [4, "Fb", 0]
Es  = [5, "E#", 0]
F  = [5, "F", 0]
Fs = [6, "F#", 0]
Gb = [6, "Gb", 0]
G  = [7, "G", 0]
Gs = [8, "G#", 0]
Ab = [8, "Ab", 0]
A  = [9, "A", 0]
As = [10, "A#", 0]
Bb = [10, "Bb", 0]
B  = [11, "B", 0]
Cb  = [11, "Cb", 0]
Bs  = [0, "B#", 0]


# Major
c_major  = [copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(B)]
cs_major = [copy.deepcopy(Cs), copy.deepcopy(Ds), copy.deepcopy(Es), copy.deepcopy(Fs), copy.deepcopy(Gs), copy.deepcopy(As), copy.deepcopy(Bs)]
d_major  = [copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(Cs)]
eb_major = [copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(Ab), copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(D)]
e_major  = [copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(Gs), copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(Cs), copy.deepcopy(Ds)]
f_major  = [copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(E)]
fs_major = [copy.deepcopy(Fs), copy.deepcopy(Gs), copy.deepcopy(As), copy.deepcopy(B), copy.deepcopy(Cs), copy.deepcopy(Ds), copy.deepcopy(Es)]
g_major  = [copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(Fs)]
ab_major = [copy.deepcopy(Ab), copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(Db), copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(G)]
a_major  = [copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(Cs), copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(Gs)]
bb_major = [copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(A)]
b_major  = [copy.deepcopy(B), copy.deepcopy(Cs), copy.deepcopy(Ds), copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(Gs), copy.deepcopy(As)]

# Minor
c_minor  = [copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(Ab), copy.deepcopy(Bb)]
cs_minor = [copy.deepcopy(Cs), copy.deepcopy(Ds), copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(Gs), copy.deepcopy(A), copy.deepcopy(B)]
d_minor  = [copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(Bb), copy.deepcopy(C)]
eb_minor = [copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(Gb), copy.deepcopy(Ab), copy.deepcopy(Bb), copy.deepcopy(Cb), copy.deepcopy(Db)]
e_minor  = [copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(C), copy.deepcopy(D)]
f_minor  = [copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(Ab), copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(Db), copy.deepcopy(Eb)]
fs_minor = [copy.deepcopy(Fs), copy.deepcopy(Gs), copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(Cs), copy.deepcopy(D), copy.deepcopy(E)]
g_minor  = [copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(Eb), copy.deepcopy(F)]
ab_minor = [copy.deepcopy(Ab), copy.deepcopy(Bb), copy.deepcopy(Cb), copy.deepcopy(Db), copy.deepcopy(Eb), copy.deepcopy(Fb), copy.deepcopy(Gb)]
a_minor  = [copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(F), copy.deepcopy(G)]
bb_minor = [copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(Db), copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(Gb), copy.deepcopy(Ab)]
b_minor  = [copy.deepcopy(B), copy.deepcopy(Cs), copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(G), copy.deepcopy(A)]

# Harmonic minor
c_harmonic  = [copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(Ab), copy.deepcopy(B)]
cs_harmonic = [copy.deepcopy(Cs), copy.deepcopy(Ds), copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(Gs), copy.deepcopy(A), copy.deepcopy(Bs)]
d_harmonic  = [copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(Bb), copy.deepcopy(Cs)]
eb_harmonic = [copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(Gb), copy.deepcopy(Ab), copy.deepcopy(Bb), copy.deepcopy(Cb), copy.deepcopy(D)]
e_harmonic  = [copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(C), copy.deepcopy(Ds)]
f_harmonic  = [copy.deepcopy(F), copy.deepcopy(G), copy.deepcopy(Ab), copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(Db), copy.deepcopy(E)]
fs_harmonic = [copy.deepcopy(Fs), copy.deepcopy(Gs), copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(Cs), copy.deepcopy(D), copy.deepcopy(Es)]
g_harmonic  = [copy.deepcopy(G), copy.deepcopy(A), copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(Eb), copy.deepcopy(Fs)]
ab_harmonic = [copy.deepcopy(Ab), copy.deepcopy(Bb), copy.deepcopy(Cb), copy.deepcopy(Db), copy.deepcopy(Eb), copy.deepcopy(Fb), copy.deepcopy(G)]
a_harmonic  = [copy.deepcopy(A), copy.deepcopy(B), copy.deepcopy(C), copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(F), copy.deepcopy(Gs)]
bb_harmonic = [copy.deepcopy(Bb), copy.deepcopy(C), copy.deepcopy(Db), copy.deepcopy(Eb), copy.deepcopy(F), copy.deepcopy(Gb), copy.deepcopy(A)]
b_harmonic  = [copy.deepcopy(B), copy.deepcopy(Cs), copy.deepcopy(D), copy.deepcopy(E), copy.deepcopy(Fs), copy.deepcopy(G), copy.deepcopy(As)]

# ## Major Scales
# c_major  = [C, D, E, F, G, A, B]
# cs_major = [Cs, Ds, Es, Fs, Gs, As, Bs]
# d_major  = [D, E, Fs, G, A, B, Cs]
# eb_major = [Eb, F, G, Ab, Bb, C, D]
# e_major  = [E, Fs, Gs, A, B, Cs, Ds]
# f_major  = [F, G, A, Bb, C, D, E]
# fs_major = [Fs, Gs, As, B, Cs, Ds, Es]
# g_major  = [G, A, B, C, D, E, Fs]
# ab_major = [Ab, Bb, C, Db, Eb, F, G]
# a_major  = [A, B, Cs, D, E, Fs, Gs]
# bb_major = [Bb, C, D, Eb, F, G, A]
# b_major  = [B, Cs, Ds, E, Fs, Gs, As]

# ## Minor Scales
# c_minor  = [C, D, Eb, F, G, Ab, Bb]
# cs_minor = [Cs, Ds, E, Fs, Gs, A, B]
# d_minor  = [D, E, F, G, A, Bb, C]
# eb_minor = [Eb, F, Gb, Ab, Bb, Cb, Db]
# e_minor  = [E, Fs, G, A, B, C, D]
# f_minor  = [F, G, Ab, Bb, C, Db, Eb]
# fs_minor = [Fs, Gs, A, B, Cs, D, E]
# g_minor  = [G, A, Bb, C, D, Eb, F]
# gs_minor = [Gs, As, B, Cs, Ds, E, Fs]
# a_minor  = [A, B, C, D, E, F, G]
# bb_minor  = [Bb, C, Db, Eb, F, Gb, Ab]
# b_minor  = [B, Cs, D, E, Fs, G, A]

absolute_notes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# scales = [c_major, cs_major, d_major, eb_major, e_major, f_major, fs_major, g_major, ab_major, a_major, bb_major, b_major]#, c_minor, cs_minor, d_minor, eb_minor, e_minor, f_minor, fs_minor, g_minor, gs_minor, a_minor, b_minor, b_minor]
majors = [[c_major,  "C - Am", 0],
          [g_major,  "G - Em", 0],
          [d_major,  "D - Bm", 0],
          [a_major,  "A - F#m", 0],
          [e_major,  "E - C#m", 0],
          [b_major,  "B - Abm", 0],
          [fs_major, "F# - Ebm", 0],
          [cs_major, "C# - Bbm", 0],
          [ab_major, "Ab - Fm", 0],
          [eb_major, "Eb - Cm", 0],
          [bb_major, "Bb - Gm", 0],
          [f_major,  "F - Dm", 0]]

harmonics = [[a_harmonic, "Am H", 0],
             [e_harmonic, "Em H", 0],
             [b_harmonic, "Bm H", 0],
             [fs_harmonic, "F#m H", 0],
             [cs_harmonic, "C#m H", 0],
             [ab_harmonic, "Abm H", 0],
             [eb_harmonic, "Ebm H", 0],
             [bb_harmonic, "Bbm H", 0],
             [f_harmonic, "Fm H", 0],
             [c_harmonic, "Cm H", 0],
             [g_harmonic, "Gm H", 0],
             [d_harmonic, "Dm H", 0]]

scales = majors + harmonics

def play(i):
    # note_name = (i - 24)% 12
    absolute_notes[(i - 24)% 12] += 1
    for scale in scales:
        for note in scale[0]:
            if note[0] == (i - 24)% 12:
                note[2] += 1
                print(f"{note[1]} played {note[2]} times")
                scale[2] += 1

def release(i):
    absolute_notes[(i - 24)% 12] -= 1
    for scale in scales:
        for note in scale[0]:
            if note[0] == (i - 24)% 12 and note[2] >= 0:
                note[2] -= 1

def get_color(scale, i):
    strength = 0
    for note in scale[0]:
        strength += note[2]
    number = 0
    for note in absolute_notes:
        number += note
    if number - strength in range(0,8):
        return HIGHLIGHTS[number - strength]
    else:
        return BACKGROUND

# UI Functions
# Function to draw text at a given position
def draw_text(text, position, color=FOREGROUND):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

# def calculate_circle_center(num_points, index, total_circles, window_width, window_height):
#     # Calculate the number of rows and columns needed to fit all circles
#     num_columns = 4 #int(math.sqrt(total_circles))
#     num_rows = total_circles // num_columns + (total_circles % num_columns != 0)

#     # Calculate the dimensions of each circle based on the available space
#     circle_width = window_width / (2 * num_columns)
#     circle_height = window_height / (2 * num_rows)
#     circle_radius = min(circle_width, circle_height) / 2

#     # Calculate the gap between circles
#     circle_margin_x = (window_width - 2 * num_columns * circle_radius) / (2 * num_columns)
#     circle_margin_y = (window_height - 2 * num_rows * circle_radius) / (2 * num_rows)

#     # Calculate the position of the current circle
#     circle_row = index // num_columns
#     circle_col = index % num_columns
#     circle_center_x = circle_margin_x + circle_radius + circle_col * (2 * circle_radius + circle_margin_x)
#     circle_center_y = circle_margin_y + circle_radius + circle_row * (2 * circle_radius + circle_margin_y)

#     return (circle_center_x, circle_center_y)

def calculate_circle_center(num_points, index, total_circles, window_width, window_height, harmonic = False):
    # Calculate the center and radius of the large circle
    large_circle_center_x = window_width / 2
    large_circle_center_y = window_height / 2

    # Calculate the angle between each circle in the large circle
    angle_between_circles = 360 / total_circles

    # Calculate the position of the current circle in the large circle
    angle = math.radians(270 + angle_between_circles * index)

    circle_center_x = large_circle_center_x + LARGE_CIRCLE_RADIUS * math.cos(angle)
    circle_center_y = large_circle_center_y + LARGE_CIRCLE_RADIUS * math.sin(angle)

    if harmonic:
        circle_center_x = large_circle_center_x + (LARGE_CIRCLE_RADIUS + CIRCLE_RADIUS * 2 + SMALL_CIRCLE_RADIUS * 2) * math.cos(angle)
        circle_center_y = large_circle_center_y + (LARGE_CIRCLE_RADIUS + CIRCLE_RADIUS * 2 + SMALL_CIRCLE_RADIUS * 2) * math.sin(angle)

    return (circle_center_x, circle_center_y)


def calculate_circle_points(num_points, index, total_circles, window_width, window_height, harmonic = False):
    center = list(calculate_circle_center(num_points, index, total_circles, window_width, window_height, harmonic))

    # Calculate the points within the small circle
    circle_points = []
    for i in range(num_points):
        angle = math.radians(270 + 360 / num_points * i)
        x = center[0] + CIRCLE_RADIUS * math.cos(angle)
        y = center[1] + CIRCLE_RADIUS * math.sin(angle)
        circle_points.append((x, y))

    return circle_points



# def calculate_circle_points(num_points, index, total_circles, window_width, window_height):
#     # Calculate the number of rows and columns needed to fit all circles
#     num_columns = 4 #int(math.sqrt(total_circles))
#     num_rows = total_circles // num_columns + (total_circles % num_columns != 0)

#     # Calculate the dimensions of each circle based on the available space
#     circle_width = window_width / (2 * num_columns)
#     circle_height = window_height / (2 * num_rows)
#     circle_radius = min(circle_width, circle_height) / 2

#     # Calculate the gap between circles
#     circle_margin_x = (window_width - 2 * num_columns * circle_radius) / (2 * num_columns)
#     circle_margin_y = (window_height - 2 * num_rows * circle_radius) / (2 * num_rows)

#     # Calculate the position of the current circle
#     circle_row = index // num_columns
#     circle_col = index % num_columns
#     circle_center_x = circle_margin_x + circle_radius + circle_col * (2 * circle_radius + circle_margin_x)
#     circle_center_y = circle_margin_y + circle_radius + circle_row * (2 * circle_radius + circle_margin_y)

#     # Calculate the points within the circle
#     circle_points = []
#     for i in range(num_points):
#         angle = math.radians(360 / num_points * i)
#         x = circle_center_x + circle_radius * math.cos(angle)
#         y = circle_center_y + circle_radius * math.sin(angle)
#         circle_points.append((x, y))

#     return circle_points

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
    time.sleep(0.05)
    if midi_input.poll():
        midi_events = midi_input.read(10)  # Read up to 10 MIDI events at once
        for midi_event in midi_events:
            status, note, velocity, _ = midi_event[0]
            note_name = (note - 24)% 12
            # if note_name in c_major:
            #     note_name = c_major.index(note_name)
            # else:
            #     continue

            if status & 0xF0 == 0x90 :  # Note On event
                if velocity == 0:
                    # print(f"Note {note_name} released")
                    release(note)
                    # if note_name not in selected_points:
                    #     continue
                    # selected_points.remove(note_name)
                else:
                    play(note)
                    # print(f"Note {note_name} played with velocity {velocity}")
                    # if note_name in selected_points:
                    #     continue
                    # selected_points.add(note_name)
            elif status & 0xF0 == 0x80: # Note Off event
                release(note)
                # print(f"Note {note_name} released")
                # if note_name not in selected_points:
                #     continue
                # selected_points.remove(note_name)

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
    draw_text(f"{absolute_notes}", (200,40), FOREGROUND)

    center = (WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2)
    for i, note in enumerate(absolute_notes):
        angle = math.radians(270 + 360 / 12 * i)
        x = center[0] + (CIRCLE_RADIUS + 60) * math.cos(angle)
        y = center[1] + (CIRCLE_RADIUS + 60) * math.sin(angle)
        color = BACKGROUND
        if note > 0:
            color = FOREGROUND
        pygame.draw.circle(screen, color, (x,y), SMALL_CIRCLE_RADIUS)


    for i, scale in enumerate(majors):
        # Calculate the positions of points around a circle
        center = (WINDOW_SIZE[0] // NUM_CIRCLES + 10, WINDOW_SIZE[1] // NUM_CIRCLES + 10)
        center_point = list(calculate_circle_center(NUM_POINTS, i, NUM_CIRCLES, WINDOW_WIDTH, WINDOW_HEIGHT))
        draw_text(f"{scale[1]}", tuple(center_point), FOREGROUND)
        center_point[1] -= 90

        # draw_text(f"{scale[2]}", tuple(center_point), FOREGROUND)
        circle_points = calculate_circle_points(NUM_POINTS, i, NUM_CIRCLES, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Draw circles and numbers
        for j, point in enumerate(circle_points):
            note = scale[0][j]
            color = BACKGROUND
            if note[2] > 0:
                color = get_color(scale, j)

            # if note and note[0] in selected_points:
            #     notes_in_scale += 1
            #     color = HIGHLIGHT_0
            # if notes_in_scale == len(selected_points):
            #     color = HIGHLIGHT_2

            pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), SMALL_CIRCLE_RADIUS)
            draw_text(scale[0][j][1], point, FOREGROUND)

    for i, scale in enumerate(harmonics):
        # Calculate the positions of points around a circle
        center = (WINDOW_SIZE[0] // NUM_CIRCLES + 10, WINDOW_SIZE[1] // NUM_CIRCLES + 10)
        center_point = list(calculate_circle_center(NUM_POINTS, i, NUM_CIRCLES, WINDOW_WIDTH, WINDOW_HEIGHT, True))
        draw_text(f"{scale[1]}", tuple(center_point), FOREGROUND)
        center_point[1] -= 90

        # draw_text(f"{scale[2]}", tuple(center_point), FOREGROUND)
        circle_points = calculate_circle_points(NUM_POINTS, i, NUM_CIRCLES, WINDOW_WIDTH, WINDOW_HEIGHT, True)

        # Draw circles and numbers
        for j, point in enumerate(circle_points):
            note = scale[0][j]
            color = BACKGROUND
            if note[2] > 0:
                color = get_color(scale, j)

            # if note and note[0] in selected_points:
            #     notes_in_scale += 1
            #     color = HIGHLIGHT_0
            # if notes_in_scale == len(selected_points):
            #     color = HIGHLIGHT_2

            pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), SMALL_CIRCLE_RADIUS)
            draw_text(scale[0][j][1], point, FOREGROUND)
    # Update the display
    pygame.display.flip()

# Close MIDI input
midi_input.close()

# Quit Pygame MIDI
pygame.midi.quit()

# Quit Pygame
pygame.quit()
