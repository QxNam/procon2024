import pygame
import pygame_gui

class InputFrame:
    def __init__(self, width, height, manager):
        self.manager = manager
        self.width = width
        self.height = height
        self.grid_generated = False
        self.rows = 0
        self.cols = 0

        self.setup_ui()

    def setup_ui(self):
        input_width, input_height = 200, 30
        button_width, button_height = 200, 50
        start_y_input = (self.height - (input_height * 2 + button_height + 60)) // 2

        self.rows_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((self.width - input_width) // 2, start_y_input), (input_width, input_height)), text='Enter number of rows', manager=self.manager)
        self.rows_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(((self.width - input_width) // 2, start_y_input + input_height + 10), (input_width, input_height)), manager=self.manager)
        
        self.cols_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((self.width - input_width) // 2, start_y_input + 2 * (input_height + 10)), (input_width, input_height)), text='Enter number of cols', manager=self.manager)
        self.cols_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(((self.width - input_width) // 2, start_y_input + 3 * (input_height + 10)), (input_width, input_height)), manager=self.manager)
        
        self.generate_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((self.width - button_width) // 2, start_y_input + 4 * (input_height + 10)), (button_width, button_height)), text='Generate Grid', manager=self.manager)

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.generate_button:
                try:
                    self.rows = int(self.rows_input.get_text())
                    self.cols = int(self.cols_input.get_text())
                    self.grid_generated = True
                except ValueError:
                    print("Invalid input for rows or columns.")

    def is_grid_generated(self):
        return self.grid_generated

    def get_grid_size(self):
        return self.rows, self.cols

    def render(self, screen, time_delta):
        self.manager.update(time_delta)
        self.manager.draw_ui(screen)
