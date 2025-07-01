# Hand-Controlled Maze Game

This project implements a simple, interactive maze game controlled by hand gestures via a webcam. Players navigate a red circular player avatar through static rectangular walls to reach a green finish line. It leverages computer vision techniques using OpenCV for real-time video processing and `cvzone` for robust hand detection and tracking.

## Features

* **Real-time Hand Tracking:** Detects and tracks a single hand to control the player avatar.
* **Maze Environment:** Features a pre-defined layout of static rectangular walls forming a maze.
* **Player Control:** Users control a red circular player avatar by performing a "pinch" gesture (bringing index and middle fingers together) and moving their hand.
* **Collision Detection:** Detects collisions between the player circle and maze walls. A collision results in "GAME OVER."
* **Win Condition:** Detects when the player circle successfully reaches the green finish line.
* **Game Reset:** Allows players to restart the game at any time (especially after a game over or win) by pressing the 'R' key.
* **Visual Feedback:** Displays maze walls, the player circle, the finish line, and game status messages (e.g., "GAME OVER", "YOU WIN!").
## Prerequisites

* Python (3.x recommended).
* A webcam connected to your computer.

## Installation

1.  **Clone or Download the Repository:**
    Get the project files to your local machine.

2.  **Install Required Libraries:**
    Open your terminal or command prompt, navigate to the project directory, and run the following commands:
    ```bash
    pip install opencv-python numpy cvzone
    ```
    * Ensure `HandTrackingModule.py` (which you likely have from previous projects) is in the same directory as `maze_game.py` or accessible in your Python path.

## Usage

1.  **Run the Script:**
    Open your terminal or command prompt, navigate to the project directory, and execute:
    ```bash
    python maze_game.py
    ```
2.  **Play the Game:**
    * A window will open displaying your webcam feed overlaid with a maze. You will see a red circle (your player avatar).
    * Perform a **"pinch" gesture** (bring your index finger and middle finger tips close together, typically a distance less than 30 pixels).
    * While maintaining the pinch, move your hand to drag the red circle through the maze.
    * **Avoid hitting the blue-green walls.** If your player circle collides with a wall, "GAME OVER!" will appear.
    * **Reach the green circle** to win the game ("YOU WIN!").
3.  **Restart Game:** Press the `R` key on your keyboard at any time (especially after Game Over or You Win) to reset the circle to its starting position and begin a new game.
4.  **Exit:** Press the `q` key on your keyboard to close the application window.

## How It Works

1.  **Webcam & Hand Tracking:**
    * The webcam continuously captures live video frames.
    * `cvzone.HandDetector` detects hands in each frame and provides a list of 21 key landmarks for the primary hand.
2.  **Player Control (`DragCircle` class):**
    * The player is represented by a `DragCircle` object.
    * The script calculates the Euclidean distance between the tip of the index finger (landmark 8) and the tip of the middle finger (landmark 12).
    * If this distance falls below a predefined threshold (e.g., `30` pixels), it's interpreted as a "pinch" or "grab" gesture.
    * When grabbed, the `DragCircle`'s position is updated to follow the index finger's tip, allowing the player to move the circle.
3.  **Maze Walls (`DragRect` class):**
    * Maze walls are represented by `DragRect` objects, defined by their center positions and sizes.
    * The `check_collision` method within `DragRect` determines if the player circle is overlapping with a wall using a distance-based approach from the circle's center to the closest point on the rectangle.
4.  **Game Logic:**
    * The game continuously checks for collisions between the player circle and all maze walls. If a collision is detected, `game_over` is set to `True`.
    * It also checks if the player circle overlaps with the `finish_pos` circle. If so, `game_won` is set to `True`.
    * Based on `game_over` or `game_won` flags, appropriate messages are displayed on the screen.
5.  **Visual Overlay:**
    * Maze walls and game status messages are drawn on a separate black `numpy` array (`imgNew`).
    * This `imgNew` is then blended with the original webcam `img` using `cv2.addWeighted` and boolean masking. This creates a semi-transparent overlay effect, showing both the live webcam feed and the interactive maze elements.

## Customization

* **Camera Resolution:** Adjust `cap.set(3, 1280)` and `cap.set(4, 720)` at the beginning of the script for different webcam resolutions.
* **Hand Detection Confidence:** Modify `detectionCon` in `HandDetector(detectionCon=0.8)` to fine-tune hand detection sensitivity.
* **Pinch Threshold:** Adjust the `distance < 30` value in `maze_game.py` to make the "pinch" gesture more or less sensitive.
* **Colors:** Change `color_rect`, `color_circle`, `color_finish` (BGR format) to customize the appearance of game elements.
* **Player/Wall Sizes:** Adjust `radius` in `DragCircle` and `size` in `DragRect` to change the dimensions of the player and walls.
* **Maze Layout:** Modify the `rect_positions` list to create entirely different maze configurations.
* **Finish Line Position/Size:** Adjust `finish_pos` and `finish_radius` to change the target location and size.
* **Overlay Transparency:** Adjust the `alpha = 0.1` value in `cv2.addWeighted` for different levels of transparency of the overlay (0.0 for fully transparent, 1.0 for fully opaque).

## Troubleshooting

* **"Unable to capture camera image!":** Verify your webcam is connected, not being used by another application, and its drivers are up-to-date. Try restarting the script or your computer.
* **No hand detection:** Ensure good lighting conditions and that your hand is clearly visible to the camera. Adjust `detectionCon` if necessary.
* **Player not grabbing/releasing properly:** Adjust the `distance < 30` pinch threshold. Your hand size and camera distance affect this pixel value.
* **Collision detection issues:** Ensure the `width, height` for `DragRect` and `radius` for `DragCircle` accurately reflect your visuals.
