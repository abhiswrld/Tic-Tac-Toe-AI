import sys         # Used to safely exit the application process
import pygame      # The main engine for rendering graphics and handling events
import numpy as np # Used to manage the 3x3 game board as a mathematical matrix

# Initialize the Pygame engine before doing anything else
pygame.init()

# CONSTANTS & CONFIGURATION

# Color Palette (RGB Format)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)      # Used later for winning lines
RED = (255, 0, 0)        # Used later for losing lines
GREY = (180, 180, 180)   # Used later for ties
BLACK = (0, 0, 0)        # Background color

# Screen Dimensions
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5

# Board Layout
BOARD_ROWS = 3
BOARD_COLS = 3
# Floor division (//) ensures perfect 100x100 pixel squares without decimal errors
SQUARE_SIZE = WIDTH // BOARD_ROWS  

# Figure Proportions (For drawing X's and O's)
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# SETUP & STATE

# Set up the main display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

# Initialize an empty 3x3 logical board using numpy 
# 0 = empty square, 1 = Player (O), 2 = AI (X)
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# DRAWING FUNCTIONS

def draw_lines(color=WHITE):
    """Draws the 3x3 grid lines on the screen."""
    # We start the range at 1 because we don't need lines at the absolute edges (index 0)
    for i in range(1, BOARD_ROWS):
        # Draw horizontal lines (y-axis changes, x spans the width)
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        # Draw vertical lines (x-axis changes, y spans the height)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures(color=WHITE):
    """Scans the logical numpy board and draws 'O's and 'X's where appropriate."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            # If the logical board has a '1', draw the Player's circle (O)
            if board[row][col] == 1:
                # Calculate the precise center pixel of the specific square
                center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
                center_y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, color, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)

# INITIAL RENDER

# Draw the initial grid before starting the listening loop
draw_lines()
pygame.display.update()

# MAIN GAME LOOP

# This infinite loop keeps the window open and listens for user interactions
while True:
    for event in pygame.event.get():
        
        # Handle the user clicking the native 'Close Window' button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()