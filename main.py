"""
main.py — Entry Point
======================
This is the only file you run:   python main.py

It does the bare minimum:
  1. Create the engine (window + loop)
  2. Create the first scene (the gameplay)
  3. Hand control to the engine

That's it. All game logic lives in game_scene.py and below.
"""

from engine     import Engine
from game_scene import GameScene


def main():
    engine = Engine()       # boot pygame, open window
    scene  = GameScene()    # set up the level, player, input

    # Hand off to the engine — it loops until the player quits.
    engine.run(scene)


# ── Standard Python idiom: only run main() when executed directly ─────────────
# This means you can also   import main   from another file without side effects.
if __name__ == "__main__":
    main()
