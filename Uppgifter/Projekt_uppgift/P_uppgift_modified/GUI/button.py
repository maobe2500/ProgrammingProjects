import pygame


class Button:
    def __init__(self, screen, x, y, width, height, inactive_text, active_text=''):
        pygame.init()
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect_object = pygame.Rect(self.x, self.y, self.width, self.height)

        self._active, self._hover = False, False

        self.active_text = active_text if active_text else inactive_text
        self.inactive_text = inactive_text
        self.font = pygame.font.get_default_font()
        
        self.hover_color = (80, 86, 104)
        self.normal_color = (58, 53, 63)
        #Button color depends on if the mouse is hovering over it or not
        self.button_color = self.hover_color if self._hover else self.normal_color
        self.text_color = (242,242,242) if not self._hover else (33,33,33)

    # A getter function for the active state
    def get_active(self):
        return self._active

    # A function that toggles the active state on/off
    def toggle_active(self):
        self._active = not self._active
    
    # Returnes true if the button is pressed
    def is_pressed(self, event_pos):
        return self.rect_object.collidepoint(event_pos)
    
    #Self contained draw function that handles the checking of hover
    def draw(self):
        self._check_mouse_hover()

        #Draw the button
        color = self.hover_color if self._hover else self.button_color
        pygame.draw.rect(self.screen, color, self.rect_object)

        #Draw the text centered on the button
        text = self.active_text if self._active else self.inactive_text
        text_color = self.text_color if not self._hover else self.normal_color
        font = pygame.font.SysFont(self.font, 32)

        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width//2, self.y + self.height//2)
        self.screen.blit(text_surface, text_rect)

    #Checks if mouse is hovering over the button
    def _check_mouse_hover(self):
        if self.rect_object.collidepoint(pygame.mouse.get_pos()):
            self._hover = True
        else:
            self._hover = False
