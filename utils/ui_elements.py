import pygame_gui
import pygame

def setup_ui_elements(width, height, manager):
    input_width, input_height = 200, 30
    button_width, button_height = 200, 50

    start_y_input = (height - (input_height * 2 + button_height + 60)) // 2

    rows_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((width - input_width) // 2, start_y_input), (input_width, input_height)),
        text='Enter number of rows',
        manager=manager
    )

    rows_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(((width - input_width) // 2, start_y_input + input_height + 10), (input_width, input_height)),
        manager=manager
    )

    cols_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((width - input_width) // 2, start_y_input + 2 * (input_height + 10)), (input_width, input_height)),
        text='Enter number of cols',
        manager=manager
    )

    cols_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(((width - input_width) // 2, start_y_input + 3 * (input_height + 10)), (input_width, input_height)),
        manager=manager
    )

    generate_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((width - button_width) // 2, start_y_input + 4 * (input_height + 10)), (button_width, button_height)),
        text='Generate Grid',
        manager=manager
    )

    return rows_label, rows_input, cols_label, cols_input, generate_button
