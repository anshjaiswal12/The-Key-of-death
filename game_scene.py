"""
game_scene.py — The Game Scene
================================
A "scene" (also called a "state" or "screen") is one mode of the game:
main menu, gameplay, game-over screen, pause screen, etc.

The Engine doesn't know what game we're making — it just calls:
    scene.update(dt, events)
    scene.draw(screen)

The GameScene knows about gameplay: the player, the level, win condition.
This separation means you can swap scenes without touching the engine.
"""

import pygame
from level        import Level
from player       import Player
from input_handler import InputHandler
from renderer     import draw_text


# ── Colors for the HUD (heads-up display) ────────────────────────────────────
HUD_COLOR    = (200, 200, 200)
WIN_COLOR    = ( 80, 220,  80)
SHADOW_COLOR = ( 20,  20,  20)


class GameScene:
    """
    Owns the level, the player, input, and win detection.

    The Engine calls update() and draw() each frame.
    """

    def __init__(self):
        # ── Sub-systems ───────────────────────────────────────────────────────
        self.input   = InputHandler()
        self.level   = Level()

        # Create the player at the spawn point defined in the tile map.
        self.player  = Player(
            start_x  = self.level.spawn_x,
            start_y  = self.level.spawn_y,
            world_w  = self.level.pixel_width,
            world_h  = self.level.pixel_height,
        )

        # ── Fonts (created once — font creation is slow!) ─────────────────────
        # None = use pygame's built-in font; 18 = size in points
        self.font_small = pygame.font.Font(None, 22)
        self.font_large = pygame.font.Font(None, 56)

        # ── Game state ────────────────────────────────────────────────────────
        self.won           = False
        self.elapsed       = 0.0   # total seconds played (for a timer display)
        self.coins_total   = len(self.level.coins)
        self.coins_picked  = 0

    # ─────────────────────────────────────────
    #  Update  (called every frame by Engine)
    # ─────────────────────────────────────────
    def update(self, dt: float, events: list):
        """
        dt     — seconds since last frame
        events — list of pygame.Event (we forward to sub-systems if needed)
        """
        if self.won:
            return    # freeze everything when the player wins

        # ── 1. Poll keyboard ──────────────────────────────────────────────────
        self.input.update()

        # ── 2. Update the player (movement + collision) ───────────────────────
        self.player.update(dt, self.input, self.level.walls)

        # ── 3. Coin collection ────────────────────────────────────────────────
        player_rect = self.player.get_rect()
        for i in range(len(self.level.coins) - 1, -1, -1):
            if player_rect.colliderect(self.level.coins[i]):
                self.level.coins.pop(i)
                self.coins_picked += 1
                print(f"[Game] Collected coin ({self.coins_picked}/{self.coins_total})")

        # ── 4. Win condition: player overlaps the goal tile ───────────────────
        # Note: In this version, you MUST collect all coins first!
        if self.level.goal_rect and \
           self.coins_picked >= self.coins_total and \
           player_rect.colliderect(self.level.goal_rect):
            self.won = True
            print(f"[Game] You won in {self.elapsed:.1f}s!")

        # ── 5. Timer ──────────────────────────────────────────────────────────
        self.elapsed += dt

    # ─────────────────────────────────────────
    #  Draw  (called every frame by Engine)
    # ─────────────────────────────────────────
    def draw(self, surface: pygame.Surface):
        """
        Draw order matters — things drawn later appear on top.
        1. Level (background)
        2. Player (foreground)
        3. HUD    (always on top)
        """

        # ── 1. Level ──────────────────────────────────────────────────────────
        goal_ready = (self.coins_picked >= self.coins_total)
        self.level.draw(surface, goal_active=goal_ready)

        # ── 2. Player ─────────────────────────────────────────────────────────
        self.player.draw(surface)

        # ── 3. HUD ────────────────────────────────────────────────────────────
        self._draw_hud(surface)

    # ─────────────────────────────────────────
    #  HUD helpers
    # ─────────────────────────────────────────
    def _draw_hud(self, surface: pygame.Surface):
        """Draw timer and controls hint in the corner."""

        # Timer (top-left)
        timer_text = f"Time: {self.elapsed:.1f}s"
        # Shadow first (offset by 1 px) so text is readable on any background
        draw_text(surface, timer_text, 11, 11, self.font_small, SHADOW_COLOR)
        draw_text(surface, timer_text, 10, 10, self.font_small, HUD_COLOR)

        # Coin counter (top-right)
        coin_text = f"Coins: {self.coins_picked} / {self.coins_total}"
        if self.coins_picked < self.coins_total:
            color = HUD_COLOR
        else:
            color = WIN_COLOR   # Highlight green when ready to finish!
            coin_text = "Goal Active! " + coin_text

        tw = self.font_small.size(coin_text)[0]
        draw_text(surface, coin_text, surface.get_width() - tw - 11, 11, self.font_small, SHADOW_COLOR)
        draw_text(surface, coin_text, surface.get_width() - tw - 10, 10, self.font_small, color)

        # Controls hint (bottom-left)
        hint = "WASD / Arrow keys to move   |   ESC to quit"
        draw_text(surface, hint, 11, surface.get_height() - 24,
                  self.font_small, SHADOW_COLOR)
        draw_text(surface, hint, 10, surface.get_height() - 25,
                  self.font_small, HUD_COLOR)

        # Win banner
        if self.won:
            w, h = surface.get_size()
            msg = f"You reached the goal!  {self.elapsed:.1f}s"
            draw_text(surface, msg,
                      w // 2 - 180, h // 2 - 30,
                      self.font_large, WIN_COLOR)
