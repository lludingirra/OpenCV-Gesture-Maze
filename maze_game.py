import cv2 # Import the OpenCV library for image and video processing.
import math # Import the math module for mathematical operations (e.g., square root for distance).
import numpy as np # Import numpy for numerical operations and array manipulation.
from cvzone.HandTrackingModule import HandDetector # Import HandDetector from cvzone for hand detection and tracking.

# --- Webcam Setup ---
cap = cv2.VideoCapture(0) # Initialize video capture from the default webcam (index 0).
cap.set(3, 1280) # Set the width of the captured video frame to 1280 pixels.
cap.set(4, 720) # Set the height of the captured video frame to 720 pixels.

# --- Drawing Colors and Detector Initialization ---
color_rect = (210, 204, 5) # Color for the maze walls (a shade of blue-green/teal).
color_circle = (0, 0, 255) # Color for the player circle (red).
color_finish = (0, 255, 0) # Color for the finish line (green).
detector = HandDetector(detectionCon=0.8) # Initialize HandDetector with a detection confidence of 0.8.

# --- DragRect Class (for Maze Walls) ---
class DragRect:
    """
    A class to represent a rectangular maze wall.
    It includes collision detection with a circular object.
    """
    def __init__(self, posCenter, size=[100, 100]):
        """
        Initializes a DragRect (wall) object.

        Args:
            posCenter (tuple): The center position (cx, cy) of the wall.
            size (list): The width and height [w, h] of the wall.
        """
        self.posCenter = posCenter
        self.size = size

    def check_collision(self, circle_center, radius):
        """
        Checks for collision between this rectangle and a given circle.

        Args:
            circle_center (tuple): The (x, y) coordinates of the circle's center.
            radius (int): The radius of the circle.

        Returns:
            bool: True if collision occurs, False otherwise.
        """
        cx, cy = self.posCenter # Wall center.
        w, h = self.size # Wall dimensions.

        # Find the closest point on the rectangle to the center of the circle.
        closest_x = max(cx - w // 2, min(circle_center[0], cx + w // 2))
        closest_y = max(cy - h // 2, min(circle_center[1], cy + h // 2))

        # Calculate the distance between this closest point and the circle's center.
        distance = math.sqrt((closest_x - circle_center[0]) ** 2 + (closest_y - circle_center[1]) ** 2)
        
        # Collision occurs if this distance is less than the circle's radius.
        return distance < radius

# --- DragCircle Class (for Player Circle) ---
class DragCircle:
    """
    A class to represent the draggable player circle in the maze game.
    """
    def __init__(self, posCenter, radius=30):
        """
        Initializes a DragCircle (player) object.

        Args:
            posCenter (tuple): The initial center position (cx, cy) of the circle.
            radius (int): The radius of the circle.
        """
        self.start_pos = posCenter # Store the initial starting position for game resets.
        self.posCenter = posCenter # Current center position of the circle.
        self.radius = radius # Radius of the circle.
        self.grabbed = False # Flag to indicate if the circle is currently being grabbed by the hand.

    def update(self, cursor):
        """
        Updates the circle's position to follow the cursor if it's grabbed.

        Args:
            cursor (tuple): The (x, y) coordinates of the hand cursor.
        """
        if self.grabbed:
            self.posCenter = cursor[:2] # Update center to cursor's position.

# --- Game Reset Function ---
def reset_game():
    """
    Resets the game state to its initial conditions.
    """
    global game_over, game_won # Declare global variables to modify them.
    game_over = False # Reset game over flag.
    game_won = False # Reset game won flag.
    circle.posCenter = circle.start_pos # Reset player circle to its starting position.

# --- Define Maze Layout (Wall Positions) ---
rect_positions = [
    (200, 200), (400, 200), (600, 200), (800, 200), (1000, 200), # Top row walls
    (200, 400), (400, 400), (800, 400), (1000, 400), # Middle row walls
    (200, 600), (600, 600), (1000, 600) # Bottom row walls
]

rectList = [DragRect(pos) for pos in rect_positions] # Create DragRect objects for all wall positions.

# --- Initialize Player Circle and Finish Line ---
circle = DragCircle([640, 360]) # Player circle, initially at the center.

finish_pos = (1100, 100) # Center position of the finish circle.
finish_radius = 40 # Radius of the finish circle.

# --- Game State Flags ---
game_over = False # Flag indicating if the game is over (collided with wall).
game_won = False # Flag indicating if the game is won (reached finish line).

# --- Main Game Loop ---
while True:
    success, img = cap.read() # Read a frame from the webcam.
    img = cv2.flip(img, 1) # Flip the image horizontally for a mirror effect.

    if not success:
        print("Unable to capture camera image!") # Print error if frame reading fails.
        break # Exit the loop.

    hands, img = detector.findHands(img) # Detect hands in the image.

    # Only allow interaction if the game is not over and not won.
    if hands and not game_over and not game_won: 
        lmList = hands[0]['lmList'] # Get landmarks for the first detected hand.
        
        # Check if enough landmarks are detected (specifically for index and middle finger tips).
        if len(lmList) >= 13: 
            x1, y1 = lmList[8][:2] # Index finger tip (landmark 8) coordinates.
            x2, y2 = lmList[12][:2] # Middle finger tip (landmark 12) coordinates.

        # Calculate distance between index and middle finger tips (for "grab" gesture).
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        if distance < 30: # If fingers are close (pinch gesture), attempt to grab the circle.
            cursor = lmList[8] # Use index finger tip as the cursor.

            # Check if the cursor is currently over the player circle.
            if math.sqrt((cursor[0] - circle.posCenter[0]) ** 2 +
                         (cursor[1] - circle.posCenter[1]) ** 2) < circle.radius:
                circle.grabbed = True # Set grabbed flag to True.
        else:
            circle.grabbed = False # If fingers are not close, ungrab the circle.

        if circle.grabbed: # If the circle is grabbed, update its position to follow the cursor.
            circle.update(cursor)

    # --- Drawing Game Elements ---
    # Create a new blank image (canvas) to draw maze walls and overlay later.
    imgNew = np.zeros_like(img, np.uint8)

    # Draw maze walls on the 'imgNew' canvas.
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), color_rect, cv2.FILLED)

    # Draw the player circle on the original 'img'.
    cv2.circle(img, circle.posCenter, circle.radius, color_circle, cv2.FILLED)

    # Draw the finish line circle on the original 'img'.
    cv2.circle(img, finish_pos, finish_radius, color_finish, cv2.FILLED)

    # --- Game Logic: Collision and Win/Lose Conditions ---
    # Check for collision with maze walls.
    for rect in rectList:
        if rect.check_collision(circle.posCenter, circle.radius):
            game_over = True # Set game_over flag if collision occurs.

    # Check for collision with the finish line.
    if math.sqrt((circle.posCenter[0] - finish_pos[0]) ** 2 +
                 (circle.posCenter[1] - finish_pos[1]) ** 2) < (circle.radius + finish_radius):
        game_won = True # Set game_won flag if reached finish.

    # Display Game Over/You Win messages.
    if game_over:
        # Draw "GAME OVER" text in red.
        cv2.putText(imgNew, "GAME OVER! Press 'R' to Restart", (350, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 5)
    elif game_won:
        # Draw "YOU WIN!" text in green.
        cv2.putText(imgNew, "YOU WIN! Press 'R' to Restart", (400, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 5)

    # --- Combine Original Image and Canvas ---
    out = img.copy() # Make a copy of the original webcam image.
    alpha = 0.1 # Transparency level for the original image (0.0 - 1.0).
    mask = imgNew.astype(bool) # Create a boolean mask from 'imgNew' (True where maze walls/messages are drawn).
    # Blend the original image and the canvas image.
    # Maze walls and game messages from 'imgNew' are overlaid on 'out' with some transparency.
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("IMG", out) # Display the final combined image.

    key = cv2.waitKey(1) & 0xFF # Wait for 1ms for a key press.
    if key == ord('q'): # If 'q' is pressed, exit.
        break
    elif key == ord('r'): # If 'r' is pressed, reset the game.
        reset_game()

# Release the webcam object and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()