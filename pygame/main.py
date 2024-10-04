import pygame
import pygame_gui
import sys
import threading
from frames.input_frame import InputFrame
from frames.grid_frame import GridFrame
from frames.log_writer import start_log_writer, stop_log_writer
from screeninfo import get_monitors

# Initialize pygame and pygame_gui
pygame.init()

# Get screen dimensions
SHAPE_SCREEN = get_monitors()[0]
WIDTH, HEIGHT = int(SHAPE_SCREEN.width), int(SHAPE_SCREEN.height)
GRID_WIDTH = int(WIDTH * 2/3)

# Window settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Button Grid with Input and Frames")

# Initialize pygame_gui
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Application state variables
current_frame = "input_frame"  # Default starting frame
clock = pygame.time.Clock()

# Create instances of frames
input_frame = InputFrame(WIDTH, HEIGHT, manager)
grid_frame = GridFrame(WIDTH, HEIGHT, GRID_WIDTH, manager)

# Start log writer thread
log_thread, click_queue = start_log_writer()

running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_frame == "input_frame":
            input_frame.handle_event(event)
            if input_frame.is_grid_generated():
                current_frame = "grid_frame"
                grid_frame.set_grid(input_frame.get_grid_size())

        elif current_frame == "grid_frame":
            grid_frame.handle_event(event, click_queue)
            if grid_frame.is_back_to_input():
                current_frame = "input_frame"

        manager.process_events(event)

    screen.fill((255, 255, 255))

    if current_frame == "input_frame":
        input_frame.render(screen, time_delta)

    elif current_frame == "grid_frame":
        grid_frame.render(screen, time_delta)

    pygame.display.flip()

# Stop the log writer thread
stop_log_writer(log_thread, click_queue)
pygame.quit()
sys.exit()
