"""
level.py — The Game World
==========================
Defines the layout of the single level: walls, floors, and decorations.

HOW LEVELS WORK HERE
--------------------
The level is described as a 2D grid of characters (a "tile map").
Each character means something:
    '#' = wall (solid, blocks movement)
    '.' = floor (walkable)
    'P' = player spawn point
    'G' = goal tile (reach this to win)
    'C' = coin (collect all to activate the goal)

The Level class reads that map, builds pygame.Rect objects for walls
(for collision), and knows where to spawn the player.

WHY TILEMAPS?
-------------
They're the standard way to build 2D levels:
  • Easy to edit (just change the string)
  • Cheap to store (1 char per tile instead of per pixel)
  • Simple to extend (add new tile types)
"""

import pygame
from renderer import draw_rect, draw_rect_outline


# ── Tile size in pixels ───────────────────────────────────────────────────────
TILE_SIZE = 40   # each cell in the map is 40×40 pixels

# ── Colors ────────────────────────────────────────────────────────────────────
COLOR_WALL        = (60,  60,  80)    # dark blue-grey
COLOR_WALL_EDGE   = (90,  90, 115)    # lighter edge highlight
COLOR_FLOOR       = (35,  35,  48)    # very dark floor
COLOR_FLOOR_ALT   = (38,  38,  52)    # checkerboard alt
COLOR_GOAL        = (40, 100,  40)    # dark green (inactive)
COLOR_GOAL_ACTIVE = (80, 220,  80)    # bright green (active)
COLOR_GOAL_GLOW   = (130, 255, 130)   # brighter outline (active)
COLOR_COIN        = (255, 215,   0)   # gold
COLOR_COIN_GLOW   = (255, 245, 100)   # bright gold highlight

# ── The map ───────────────────────────────────────────────────────────────────
# Change this string to redesign the level.
# Width = 20 tiles, Height = 15 tiles → 20×40=800 × 15×40=600 px (fills window)

TILE_MAP = [
    "####################",
    "#P.................#",
    "#..................#",
    "#....####..........#",
    "#....#..#..........#",
    "#....#..#....###...#",
    "#....####....#.....#",
    "#............#.....#",
    "#............###...#",
    "#..................#",
    "###..#.........#...#",
    "#...###...C.C...###.#",
    "#...#...............#",
    "#...####..C...C..G..#",
    "####################",
]


class Level:
    """
    Parses TILE_MAP and provides:
        self.walls        — list of pygame.Rect (for collision)
        self.goal_rect    — pygame.Rect of the goal tile
        self.spawn_x/y    — player starting position in pixels
        draw(surface)     — paint the entire level
    """

    def __init__(self):
        self.walls      = []       # solid rects the player cannot pass
        self.goal_rect  = None     # the winning tile
        self.coins      = []       # list of Rects for coins
        self.spawn_x    = 0        # pixel x where player starts
        self.spawn_y    = 0        # pixel y where player starts

        # ── Parse the tile map ───────────────────────────────────────────────
        # We iterate every row (y) and column (x) of the map string.
        for row_index, row in enumerate(TILE_MAP):
            for col_index, tile in enumerate(row):

                # Convert grid coordinates → pixel coordinates
                px = col_index * TILE_SIZE
                py = row_index * TILE_SIZE

                if tile == '#':
                    # Solid wall → add a collision rect
                    self.walls.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))

                elif tile == 'P':
                    # Player spawn
                    self.spawn_x = px
                    self.spawn_y = py

                elif tile == 'G':
                    # Goal tile
                    self.goal_rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)

                elif tile == 'C':
                    # Coin tile (center it in the 40x40 cell)
                    coin_size = 12
                    cx = px + (TILE_SIZE - coin_size) // 2
                    cy = py + (TILE_SIZE - coin_size) // 2
                    self.coins.append(pygame.Rect(cx, cy, coin_size, coin_size))

        print(f"[Level] Loaded: {len(self.walls)} walls, "
              f"spawn=({self.spawn_x},{self.spawn_y})")

    # ─────────────────────────────────────────
    #  Draw the level
    # ─────────────────────────────────────────
    def draw(self, surface: pygame.Surface, goal_active: bool = False):
        """Paint every tile based on the tile map."""

        for row_index, row in enumerate(TILE_MAP):
            for col_index, tile in enumerate(row):

                px = col_index * TILE_SIZE
                py = row_index * TILE_SIZE

                if tile == '#':
                    # ── Wall tile ─────────────────────────────────────────
                    draw_rect(surface, COLOR_WALL, px, py, TILE_SIZE, TILE_SIZE)
                    # Subtle top/left highlight to give a fake 3-D bevel
                    pygame.draw.line(surface, COLOR_WALL_EDGE,
                                     (px, py), (px + TILE_SIZE - 1, py))         # top
                    pygame.draw.line(surface, COLOR_WALL_EDGE,
                                     (px, py), (px, py + TILE_SIZE - 1))         # left

                elif tile == 'G':
                    # ── Goal tile ─────────────────────────────────────────
                    if goal_active:
                        draw_rect(surface, COLOR_GOAL_ACTIVE, px, py, TILE_SIZE, TILE_SIZE)
                        draw_rect_outline(surface, COLOR_GOAL_GLOW,
                                          px, py, TILE_SIZE, TILE_SIZE, border=2)
                    else:
                        # Grayed out / Inactive goal
                        draw_rect(surface, (60, 80, 60), px, py, TILE_SIZE, TILE_SIZE)
                        draw_rect_outline(surface, (80, 100, 80),
                                          px, py, TILE_SIZE, TILE_SIZE, border=1)

                else:
                    # ── Floor tile (checkerboard for visual depth) ────────
                    # (row + col) % 2 alternates between 0 and 1
                    color = COLOR_FLOOR if (row_index + col_index) % 2 == 0 \
                            else COLOR_FLOOR_ALT
                    draw_rect(surface, color, px, py, TILE_SIZE, TILE_SIZE)

        # ── 4. Coins (drawn separately from the map so they can be removed) ─
        for coin in self.coins:
            # Draw a small gold diamond/rect for the coin
            draw_rect(surface, COLOR_COIN, coin.x, coin.y, coin.width, coin.height)
            draw_rect_outline(surface, COLOR_COIN_GLOW, coin.x, coin.y, coin.width, coin.height, border=1)

    # ─────────────────────────────────────────
    #  World dimensions (pixels)
    # ─────────────────────────────────────────
    @property
    def pixel_width(self) -> int:
        return len(TILE_MAP[0]) * TILE_SIZE

    @property
    def pixel_height(self) -> int:
        return len(TILE_MAP) * TILE_SIZE
