import pygame
import pygame_gui
import sys
import threading
import queue
import random

# Initialize pygame and pygame_gui
pygame.init()

# Define colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Window settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Button Grid with Input and Frames")

# Initialize pygame_gui
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Set the size of input fields and button
input_width, input_height = 200, 30
button_width, button_height = 200, 50

# Calculate the total height of the input frame elements (2 input fields + 1 button + margins)
total_input_height = input_height * 2 + button_height + 20 * 2  # 20 pixels margin between each

# Calculate the starting position to center the elements vertically
start_y_input = (HEIGHT - total_input_height) // 2

# Create UI elements for Frame 1 (input) centered
rows_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(((WIDTH - input_width) // 2, start_y_input), (input_width, input_height)), manager=manager)
rows_input.set_text('Enter number of rows')

cols_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(((WIDTH - input_width) // 2, start_y_input + input_height + 20), (input_width, input_height)), manager=manager)
cols_input.set_text('Enter number of columns')

generate_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH - button_width) // 2, start_y_input + 2 * (input_height + 20)), (button_width, button_height)),
                                               text='Generate Grid',
                                               manager=manager)

# Button and margin size
MARGIN = 1

# Initial grid values
NUM_ROWS, NUM_COLS = 0, 0
BUTTON_SIZE = 10
button_grid = []
grid_numbers = []  # This will store the random numbers for each grid cell

# Queue for storing clicks
click_queue = queue.Queue()

# Application state variable
current_frame = "input_frame"  # This can be 'input_frame' or 'grid_frame'

# Function to log click coordinates (place into queue)
def log_click(row, col):
    click_queue.put((row, col))  # Add click to the queue

# Function to draw buttons with auto-scaling and displaying numbers
def draw_buttons():
    global BUTTON_SIZE

    # Calculate total grid dimensions
    BUTTON_WIDTH = (WIDTH - 300) // NUM_COLS  # Adjust WIDTH to give space for the UI elements
    BUTTON_HEIGHT = (HEIGHT - 50) // NUM_ROWS
    BUTTON_SIZE = min(BUTTON_WIDTH, BUTTON_HEIGHT)

    total_grid_width = NUM_COLS * (BUTTON_SIZE + MARGIN)
    total_grid_height = NUM_ROWS * (BUTTON_SIZE + MARGIN)

    # Calculate the starting positions to center the grid
    start_x = (WIDTH - total_grid_width) // 2
    start_y = (HEIGHT - total_grid_height) // 2

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            color = RED if button_grid[row][col] else GRAY
            x = col * (BUTTON_SIZE + MARGIN) + start_x
            y = row * (BUTTON_SIZE + MARGIN) + start_y
            pygame.draw.rect(screen, color, 
                             (x, y, BUTTON_SIZE, BUTTON_SIZE))

            # Scale font size based on BUTTON_SIZE
            font_size = int(BUTTON_SIZE * 0.6)  # Font size scales with button size
            font = pygame.font.Font(None, font_size)

            # Render the random number in the center of the button
            number_surface = font.render(str(grid_numbers[row][col]), True, WHITE)
            number_rect = number_surface.get_rect(center=(x + BUTTON_SIZE // 2, y + BUTTON_SIZE // 2))
            screen.blit(number_surface, number_rect)

# Function to handle mouse clicks in the grid
def handle_mouse_click(pos):
    # Recalculate the start positions for centering the grid (to correctly handle clicks)
    total_grid_width = NUM_COLS * (BUTTON_SIZE + MARGIN)
    total_grid_height = NUM_ROWS * (BUTTON_SIZE + MARGIN)
    start_x = (WIDTH - total_grid_width) // 2
    start_y = (HEIGHT - total_grid_height) // 2

    col = (pos[0] - start_x) // (BUTTON_SIZE + MARGIN)
    row = (pos[1] - start_y) // (BUTTON_SIZE + MARGIN)
    
    if 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
        if not button_grid[row][col]:  # Only log click if button is not already red
            button_grid[row][col] = True  # Change button state to red
            log_click(row, col)  # Log the coordinates when clicked to red
        else:
            button_grid[row][col] = False  # Toggle back to gray without logging

# Function to generate a grid based on input
def generate_grid():
    global NUM_ROWS, NUM_COLS, button_grid, grid_numbers, current_frame
    try:
        NUM_ROWS = int(rows_input.get_text())
        NUM_COLS = int(cols_input.get_text())
        button_grid = [[False for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
        grid_numbers = [[random.randint(0, 3) for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]  # Random numbers between 0 and 3
        current_frame = "grid_frame"  # Switch to the grid frame after the grid is generated
    except ValueError:
        print("Invalid input for rows or columns.")

# Function to write clicks to log file
def log_writer():
    with open("click_log_threaded.txt", "a") as log_file:
        while True:
            # Block until an item is available in the queue
            row, col = click_queue.get()
            if row is None and col is None:  # Termination signal
                break
            log_file.write(f"Clicked at (row: {row}, col: {col})\n")
            log_file.flush()  # Ensure it writes immediately
            click_queue.task_done()

# Start the log writer thread
log_thread = threading.Thread(target=log_writer, daemon=True)
log_thread.start()

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if current_frame == "input_frame":
            # Handle events for Frame 1 (input screen)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == generate_button:
                    generate_grid()

            manager.process_events(event)

        elif current_frame == "grid_frame":
            # Handle events for Frame 2 (grid screen)
            if event.type == pygame.MOUSEBUTTONDOWN and button_grid:
                handle_mouse_click(pygame.mouse.get_pos())
    
    screen.fill(WHITE)

    if current_frame == "input_frame":
        # Display Frame 1 UI elements
        manager.update(time_delta)
        manager.draw_ui(screen)

    elif current_frame == "grid_frame":
        # Display the grid if available
        if button_grid:
            draw_buttons()
    
    pygame.display.flip()

# Stop the logging thread (send termination signal)
click_queue.put((None, None))
log_thread.join()

pygame.quit()
sys.exit()
