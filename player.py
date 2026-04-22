"""
player.py — The Player Entity
==============================
Represents the character the user controls.

An "entity" in game dev is anything that exists in the game world
with its own state (position, health, velocity, …) and behaviour.

The Player's responsibilities:
  1. Know where it is  (x, y)
  2. Know how fast it moves  (speed)
  3. React to input  (update)
  4. Know how to draw itself  (draw)
  5. Stay inside the level boundaries  (clamping)
"""

import pygame
from input_handler import InputHandler, MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT
from renderer import draw_rect, draw_rect_outline


# ── Visual constants for the player ──────────────────────────────────────────
PLAYER_WIDTH  = 32   # pixels
PLAYER_HEIGHT = 32
PLAYER_COLOR        = (80, 160, 255)   # blue body
PLAYER_OUTLINE      = (180, 220, 255)  # lighter blue outline
PLAYER_SPEED        = 200              # pixels per second


class Player:
    """
    The player character.

    __init__  — set starting position
    update    — read input, move, clamp to world bounds
    draw      — paint onto the screen
    """

    def __init__(self, start_x: float, start_y: float, world_w: int, world_h: int):
        # ── Position (top-left corner of the player rectangle) ───────────────
        # We store as float so sub-pixel movement accumulates correctly.
        # (If we stored as int, moving 0.7 px/frame would always round to 0.)
        self.x = float(start_x)
        self.y = float(start_y)

        # ── Size ─────────────────────────────────────────────────────────────
        self.width  = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        # ── Speed ─────────────────────────────────────────────────────────────
        self.speed = PLAYER_SPEED   # pixels per second

        # ── World boundary (so the player can't walk off screen) ──────────────
        self.world_w = world_w
        self.world_h = world_h

        # ── Visual state (for a little animation feel) ────────────────────────
        self.is_moving = False

    # ─────────────────────────────────────────
    #  Update  (called every frame)
    # ─────────────────────────────────────────
    def update(self, dt: float, input_handler: InputHandler, walls: list):
        """
        dt             — seconds since last frame (for frame-rate independent movement)
        input_handler  — lets us check which keys are held
        walls          — list of pygame.Rect objects the player cannot overlap
        """

        # ── 1. Calculate intended movement ───────────────────────────────────
        # We build a velocity vector (dx, dy) based on held keys.
        dx = 0.0
        dy = 0.0

        if input_handler.is_held(MOVE_LEFT):
            dx -= 1.0
        if input_handler.is_held(MOVE_RIGHT):
            dx += 1.0
        if input_handler.is_held(MOVE_UP):
            dy -= 1.0    # pygame Y axis points DOWN, so "up" = negative Y
        if input_handler.is_held(MOVE_DOWN):
            dy += 1.0

        # ── 2. Normalize diagonal movement ───────────────────────────────────
        # Without this, moving diagonally is √2 ≈ 1.41× faster than straight.
        # We scale the vector back to length 1 when both axes are active.
        if dx != 0 and dy != 0:
            dx *= 0.7071   # 1 / √2
            dy *= 0.7071

        # ── 3. Mark whether we're moving (used for visual feedback) ──────────
        self.is_moving = (dx != 0 or dy != 0)

        # ── 4. Apply speed and delta time to get pixel displacement ──────────
        move_x = dx * self.speed * dt
        move_y = dy * self.speed * dt

        # ── 5. Move on X axis, then check wall collisions on X ───────────────
        self.x += move_x
        self._resolve_wall_collisions_x(walls, move_x)

        # ── 6. Move on Y axis, then check wall collisions on Y ───────────────
        # We separate X and Y so the player can slide along walls.
        self.y += move_y
        self._resolve_wall_collisions_y(walls, move_y)

        # ── 7. Clamp to world boundaries ─────────────────────────────────────
        # max(0, …) stops the player going past the left/top edge.
        # min(world_size - player_size, …) stops it going past the right/bottom.
        self.x = max(0, min(self.world_w - self.width,  self.x))
        self.y = max(0, min(self.world_h - self.height, self.y))

    # ─────────────────────────────────────────
    #  Collision helpers
    # ─────────────────────────────────────────
    def get_rect(self) -> pygame.Rect:
        """Return the player's bounding box as a pygame.Rect (integer pixels)."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def _resolve_wall_collisions_x(self, walls: list, move_x: float):
        """Push the player out of any wall it overlaps, on the X axis only."""
        for wall in walls:
            player_rect = self.get_rect()
            if player_rect.colliderect(wall):
                if move_x > 0:
                    # Moving right -> hit the left side of the wall
                    self.x = wall.left - self.width
                elif move_x < 0:
                    # Moving left -> hit the right side of the wall
                    self.x = wall.right
                else:
                    # Stationary overlap fallback (using center comparison)
                    if self.x + self.width / 2 < wall.centerx:
                        self.x = wall.left - self.width
                    else:
                        self.x = wall.right

    def _resolve_wall_collisions_y(self, walls: list, move_y: float):
        """Push the player out of any wall it overlaps, on the Y axis only."""
        for wall in walls:
            player_rect = self.get_rect()
            if player_rect.colliderect(wall):
                if move_y > 0:
                    # Moving down -> hit the top side of the wall
                    self.y = wall.top - self.height
                elif move_y < 0:
                    # Moving up -> hit the bottom side of the wall
                    self.y = wall.bottom
                else:
                    # Stationary overlap fallback
                    if self.y + self.height / 2 < wall.centery:
                        self.y = wall.top - self.height
                    else:
                        self.y = wall.bottom

    # ─────────────────────────────────────────
    #  Draw  (called every frame after update)
    # ─────────────────────────────────────────
    def draw(self, surface: pygame.Surface):
        ix, iy = int(self.x), int(self.y)

        # Body
        draw_rect(surface, PLAYER_COLOR, ix, iy, self.width, self.height)

        # Outline — brighter when moving so you feel the responsiveness
        outline_color = (255, 255, 255) if self.is_moving else PLAYER_OUTLINE
        draw_rect_outline(surface, outline_color, ix, iy, self.width, self.height, border=2)

        # A small "eye" so you can see which direction feels like "forward"
        # (top-center of the rectangle)
        eye_x = ix + self.width  // 2 - 3
        eye_y = iy + 6
        draw_rect(surface, (255, 255, 200), eye_x, eye_y, 6, 6)
