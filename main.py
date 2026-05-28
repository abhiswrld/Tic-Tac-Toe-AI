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
    # We start the range at 1 because we don't need lines at the absolute edges (index 0)
    for i in range(1, BOARD_ROWS):
        # Draw horizontal lines (y-axis changes, x spans the width)
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        # Draw vertical lines (x-axis changes, y spans the height)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures(color=WHITE):
    # Loop through every row and column in our 3x3 matrix to update visual shapes
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            
            # If the logical board has a 1, draw the Player's circle (O)
            if board[row][col] == 1:
                # Calculate the exact center pixel of the chosen grid square
                center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
                center_y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, color, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
                
            # If the logical board has a 2, draw the AI's cross (X)
            elif board[row][col] == 2:
                # Top-left to bottom-right line offset calculation (uses 1/4 and 3/4 padding inside the box)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                # Bottom-left to top-right line offset calculation
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

# UTILITY CORE GAME LOGIC

def mark_square(row, col, player):
    # Assign the current square coordinates to the specific player integer (1 or 2)
    board[row][col] = player

def available_square(row, col):
    # Returns True if the square is 0 (empty), False if it is already taken
    return board[row][col] == 0

def is_board_full(check_board=board):
    # Scan every cell to see if any spot is still open
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False # Found an empty square, board is NOT full
    return True # Looped through all cells and found no zeros

def check_win(player, check_board=board):
    # 1. Vertical win checks (scanning each column)
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player: 
           return True
        
    # 2. Horizontal win checks (scanning each row)
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player: 
           return True
    
    # 3. Top-Left to Bottom-Right diagonal win check
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True

    # 4. Bottom-Left to Top-Right diagonal win check
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    # Return False if none of the winning line configurations are met
    return False

# MINIMAX AI ENGINE

def minimax(minimax_board, depth, is_maximizing):
    # Base Cases: Terminal states that stop the recursive search tree loop
    if check_win(2, minimax_board):
        return float('inf')   # AI winning is the absolute best outcome
    elif check_win(1, minimax_board):
        return float('-inf')  # Player winning is the absolute worst outcome
    elif is_board_full(minimax_board):
        return 0              # Tie is completely neutral score
    
    # AI Maximizing Branch: Simulates its own best possible responses
    if is_maximizing:
        best_score = -100
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2                  # Temporarily place AI move
                    score = minimax(minimax_board, depth + 1, False) # Recurse down to player turn
                    minimax_board[row][col] = 0                  # Backtrack and reset board state
                    best_score = max(score, best_score)          # Track maximum possible value
        return best_score
        
    # Player Minimizing Branch: Simulates what the opponent would do to hurt the AI
    else:
        best_score = 100
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1                  # Temporarily place Player move
                    score = minimax(minimax_board, depth + 1, True)  # Recurse down to AI turn
                    minimax_board[row][col] = 0                  # Backtrack and reset board state
                    best_score = min(score, best_score)          # Track minimum possible value
        return best_score

def best_move():
    best_score = -100
    best_target = (-1, -1) # Track the coordinates of our top-rated game square
    
    # Evaluate every single empty cell to initialize the first recursion level
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2              # Fake an AI move on the actual matrix
                score = minimax(board, 0, False) # Kickoff minimax to predict future states
                board[row][col] = 0              # Backtrack and clear the cell
                
                # If this sequence scores higher than our benchmark, save its details
                if score > best_score:
                    best_score = score
                    best_target = (row, col)
    
    # If a valid calculated pathway was captured, commit the piece permanently to the board
    if best_target != (-1, -1):
        mark_square(best_target[0], best_target[1], 2)
        return True
    
    return False

def restart_game():
    # Clear the graphical window and reset the logical numpy data matrix back to zeros
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# INITIAL RENDER

# Draw the initial grid before starting the listening loop
draw_lines()

player = 1
game_over = False

# MAIN GAME LOOP

# This infinite loop keeps the window open and listens for user interactions
while True:
    for event in pygame.event.get():
        
        # Handle the user clicking the native 'Close Window' button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle mouse clicks on the game grid
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # Convert raw pixel coordinates into logical matrix grid indexes (0, 1, or 2)
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            # Process human player move sequence
            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1
            
                # Immediately trigger the AI opponent move if the game is still running
                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1
                
                # Final fallback check to verify if the board hit a stalemate tie scenario
                if not game_over:
                    if is_board_full():
                        game_over = True
        
        # Handle keyboard shortcuts for resetting state mechanics
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
        
    # Visual rendering state controller loop
    if not game_over:
        draw_figures()
    else:
        # Repaint grid and elements using specialized color codes depending on who won
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GREY)
            draw_lines(GREY)

    # Push all buffered graphical updates live to the active display frame
    pygame.display.update()