# The Key of Death — 2D Engine Adventure

A lethal, modular 2D engine built from scratch in Python + Pygame. 
Navigate the dark corridors, collect all hidden coins, and unlock the exit before it's too late.

---

## 🕹️ Gameplay
*   **Move**: Use **WASD** or **Arrow Keys**.
*   **Objective**: Collect all gold coins scattered in the maze.
*   **Win**: Once all coins are collected, the **Inactive Goal** will turn green and activate. Reach it to escape.
*   **Quit**: Press **ESC** at any time.

---

## 🏗️ Technical File Structure

```
game/
├── main.py          ← Entry point.
├── engine.py        ← Game loop, window, clock, and delta-time capping.
├── input_handler.py ← Action-based keyboard abstraction.
├── renderer.py      ← Pygame draw wrappers (Rects, Text, Outlines).
├── player.py        ← Entity logic: Axis-separated AABB collisions.
├── level.py         ← Tile map parser: Handles walls, spawns, and coins.
└── game_scene.py    ← Wires everything together; progress & win detection.
```

---

## 🚀 Installation & Run

1. **Install Dependencies** (Optimized for Linux/Arch):
   ```bash
   sudo pacman -S python python-pygame
   ```

2. **Run the Game**:
   ```bash
   python main.py
   ```

---

## 🛠️ Advanced Engine Features

### 1. Robust Collision Resolution
The engine uses axis-separated AABB collision logic. By checking X and Y movement independently, the player can smoothly **slide** along walls instead of sticking, even at high speeds.

### 2. Frame-Rate Independence
Movement is tied to `delta time (dt)` but capped at `0.1s`. This ensures the game feels identical on 30Hz or 144Hz monitors and prevents "tunnelling" through walls during frame spikes.

### 3. Decoupled Architecture
*   **The Engine** doesn't know *what* game it is running; it only knows how to run a `Scene`.
*   **The Scene** manages the interaction between the `Level` and `Player`.
*   **The InputHandler** maps keys to actions, making it trivial to add controller support or rebind keys.

---

## 📜 Project Concepts Summary

```
main.py
  └─ Engine (System Loop)
       └─ GameScene (State Logic)
            ├─ InputHandler (Action Mapping)
            ├─ Level        (Environment & Collectibles)
            ├─ Player       (Physics & Bounding Boxes)
            └─ Renderer     (Visual Output)
```

Each module adheres to the **Single Responsibility Principle**, ensuring the codebase remains readable, stable, and easy to extend.
``

Each file has **one job**. This is the Single Responsibility Principle —
the most important design pattern for keeping code you can understand and change.
