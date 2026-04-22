"""
input_handler.py — Keyboard Input
==================================
Abstracts raw pygame key codes into clean "actions".

WHY BOTHER?
-----------
If you scatter pygame.K_LEFT checks all over your code, changing
the controls later means hunting through every file. Instead, we
define actions (MOVE_LEFT, MOVE_RIGHT, …) here once. Everything
else just asks "is MOVE_LEFT held?" — no pygame details leak out.

This pattern is called an "input abstraction layer".
"""

import pygame


# ── Action names (just strings used as dictionary keys) ──────────────────────
MOVE_UP    = "move_up"
MOVE_DOWN  = "move_down"
MOVE_LEFT  = "move_left"
MOVE_RIGHT = "move_right"


# ── Key bindings: action → list of keys that trigger it ──────────────────────
# Multiple keys can map to the same action (arrows AND WASD both work).
KEY_BINDINGS = {
    MOVE_UP:    [pygame.K_w, pygame.K_UP],
    MOVE_DOWN:  [pygame.K_s, pygame.K_DOWN],
    MOVE_LEFT:  [pygame.K_a, pygame.K_LEFT],
    MOVE_RIGHT: [pygame.K_d, pygame.K_RIGHT],
}


class InputHandler:
    """
    Call update() once per frame, then query is_held(action) anywhere.

    is_held() returns True every frame the key stays pressed,
    which is what you want for smooth movement.
    """

    def __init__(self):
        # We'll store a snapshot of the keyboard state here each frame.
        self._keys = {}

    def update(self):
        """
        pygame.key.get_pressed() returns a list indexed by key code.
        Index with a key constant (e.g. pygame.K_LEFT) → True/False.
        We call this once per frame so all movement reads the same snapshot.
        """
        self._keys = pygame.key.get_pressed()

    def is_held(self, action: str) -> bool:
        """
        Returns True if ANY key bound to 'action' is currently pressed.

        Example:
            if input_handler.is_held(MOVE_LEFT):
                player.move(-1, 0)
        """
        for key in KEY_BINDINGS.get(action, []):
            if self._keys[key]:
                return True
        return False
