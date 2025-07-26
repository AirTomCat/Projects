# Py-Pacman 🟡👻

A complete, playable version of the classic arcade game Pac-Man, built from scratch using Python and the Pygame library.

This implementation features custom-drawn sprites, smooth player controls, and all the core mechanics that make the original game a classic.

---

## Features

-   **Complete Game Loop:** Includes a start screen, a main game state, and a "Game Over" screen.
-   **Smooth Controls:** Features buffered input, allowing you to press a direction key before reaching an intersection for fluid, responsive movement.
-   **Classic Gameplay Elements:** Collect dots, eat power pellets to make ghosts vulnerable, and chase high scores.
-   **Custom Sprites:** Both Pac-Man and the ghosts are drawn as circular characters with eyes, and Pac-Man rotates to face his direction of movement.
-   **Simple AI:** Ghosts move randomly around the maze, providing a dynamic challenge.
-   **Restart Functionality:** Easily restart the game by pressing the 'R' key after a game is over.

---

## Requirements

-   Python 3.x
-   Pygame

---

## How to Play

### Running the Game

1.  **Save the Code:** Ensure the game's code is saved in a file named `pacman_game.py`.
2.  **Install Pygame:** If you haven't already, open your terminal or command prompt and run:
    ```bash
    pip install pygame
    ```
3.  **Run the Script:** From the same directory as the file, execute the command:
    ```bash
    python pacman_game.py
    ```

### Controls

-   **Arrow Keys:** Move Pac-Man up, down, left, and right.
-   **'R' Key:** Restart the game from the "Game Over" screen.
