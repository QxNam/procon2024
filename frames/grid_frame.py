import pygame
import pygame_gui
import random

class GridFrame:
    def __init__(self, width, height, grid_width, manager):
        self.width = width
        self.height = height
        self.grid_width = grid_width
        self.manager = manager
        self.rows = 0
        self.cols = 0
        self.button_grid = []
        self.grid_numbers = []
        self.back_to_input = False
        self.step_count = 0

        # Exit button
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.width - 250, self.height - 100), (200, 50)), text='Exit', manager=self.manager)
        self.exit_button.hide()

    def set_grid(self, grid_size):
        self.rows, self.cols = grid_size
        self.button_grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid_numbers = [[random.randint(0, 3) for _ in range(self.cols)] for _ in range(self.rows)]
        self.exit_button.show()

    def handle_event(self, event, click_queue):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(pygame.mouse.get_pos(), click_queue)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_button:
                self.back_to_input = True
                self.exit_button.hide()

    def handle_mouse_click(self, pos, click_queue):
        # Similar implementation as before
        pass

    def is_back_to_input(self):
        return self.back_to_input

    def render(self, screen, time_delta):
        self.draw_buttons(screen)
        self.manager.update(time_delta)
        self.manager.draw_ui(screen)

    def draw_buttons(self, screen):
        # Similar implementation as before
        pass
