"""
renderer.py — Drawing Utilities
================================
Thin wrappers around pygame draw calls.

WHY A SEPARATE FILE?
--------------------
Keeping draw logic here means:
  • Game objects describe WHAT they are (position, size, color).
  • The renderer decides HOW to draw them (outlines, shadows, effects).
  • Swapping from pixel art → 3D later only changes this file.

Right now it's simple rectangles, but you could add sprite sheets,
particle effects, or lighting here without touching game logic.
"""

import pygame


def draw_rect(surface, color, x, y, width, height):
    """
    Draw a filled rectangle.

    surface — the pygame surface to draw on (usually the screen)
    color   — (R, G, B) tuple, values 0-255
    x, y    — top-left corner position in pixels
    width, height — size in pixels
    """
    pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height))


def draw_rect_outline(surface, color, x, y, width, height, border=2):
    """
    Draw a hollow rectangle (outline only).
    'border' is the thickness of the outline in pixels.
    """
    pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height), border)


def draw_text(surface, text, x, y, font, color=(255, 255, 255)):
    """
    Render a string of text at (x, y).

    font  — a pygame.font.Font object (created once and reused, not every frame)
    color — (R, G, B) text color
    """
    text_surface = font.render(text, True, color)   # True = anti-aliased edges
    surface.blit(text_surface, (x, y))              # blit = "copy pixels onto"


def draw_grid(surface, cell_size, color=(40, 40, 55)):
    """
    Draw a faint background grid — helps you see the coordinate system.
    Only used for debugging; remove it in a final game.
    """
    w, h = surface.get_size()

    # Vertical lines
    for x in range(0, w, cell_size):
        pygame.draw.line(surface, color, (x, 0), (x, h))

    # Horizontal lines
    for y in range(0, h, cell_size):
        pygame.draw.line(surface, color, (0, y), (w, y))
