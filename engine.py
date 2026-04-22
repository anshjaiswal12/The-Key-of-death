"""
engine.py — The Core Game Engine
=================================
This is the heart of the game. It owns:
  1. The window (display surface)
  2. The game loop  (update → render → repeat)
  3. The clock     (keeps a fixed frame rate)

Think of this as the "operating system" of your game.
Every other system (input, rendering, entities) plugs into this.
"""

import pygame
import sys


# ─────────────────────────────────────────────
#  Constants — tweak these to change the feel
# ─────────────────────────────────────────────
WINDOW_TITLE  = "My First Game Engine"
WINDOW_WIDTH  = 800          # pixels
WINDOW_HEIGHT = 600          # pixels
TARGET_FPS    = 60           # frames per second we aim for


class Engine:
    """
    The Engine class wraps everything pygame needs to run.

    Usage:
        engine = Engine()
        engine.run(game_scene)   # game_scene is an object with update() and draw()
    """

    def __init__(self):
        # ── Step 1: Boot pygame ──────────────────────────────────────────────
        # pygame.init() starts ALL pygame sub-systems (display, sound, input…)
        pygame.init()

        # ── Step 2: Create the window ────────────────────────────────────────
        # The "surface" is just a big grid of pixels we can paint on.
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        # ── Step 3: Create the clock ─────────────────────────────────────────
        # pygame.time.Clock() lets us call clock.tick(FPS) once per frame.
        # That call sleeps just long enough so we never exceed TARGET_FPS.
        self.clock = pygame.time.Clock()

        # ── Step 4: State flags ──────────────────────────────────────────────
        self.running = True   # set to False anywhere to quit the game

        print(f"[Engine] Window {WINDOW_WIDTH}×{WINDOW_HEIGHT} @ {TARGET_FPS} FPS")

    # ─────────────────────────────────────────
    #  The Game Loop
    # ─────────────────────────────────────────
    def run(self, scene):
        """
        The game loop — runs until self.running is False.

        Every single frame does exactly three things, in order:
            1. Handle events   (did the player press a key? close the window?)
            2. Update          (move things, apply physics, check collisions)
            3. Draw            (paint the new state onto the screen)

        'scene' is any object that has:
            scene.update(dt, events)
            scene.draw(screen)
        """

        while self.running:

            # ── 1. EVENTS ────────────────────────────────────────────────────
            # pygame collects everything that happened since last frame
            # into a list of Event objects.
            events = pygame.event.get()

            for event in events:
                # The red X button or Alt+F4
                if event.type == pygame.QUIT:
                    self.running = False

                # Escape key also quits (handy during development)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # dt = "delta time" in seconds since the last frame.
            # Multiplying speeds by dt makes movement frame-rate independent.
            # We cap dt to 0.1s to prevent physics glitches if the game stutters.
            dt = min(self.clock.tick(TARGET_FPS) / 1000.0, 0.1)

            scene.update(dt, events)

            # ── 3. DRAW ──────────────────────────────────────────────────────
            # First, wipe the screen (otherwise old frames bleed through).
            self.screen.fill((20, 20, 30))   # dark background color (R, G, B)

            # Let the scene paint itself.
            scene.draw(self.screen)

            # Flip the back-buffer to the screen.
            # pygame draws everything off-screen first, then shows it all at once
            # to avoid flickering. This is called "double buffering".
            pygame.display.flip()

        # ── Shutdown ─────────────────────────────────────────────────────────
        pygame.quit()
        sys.exit()
