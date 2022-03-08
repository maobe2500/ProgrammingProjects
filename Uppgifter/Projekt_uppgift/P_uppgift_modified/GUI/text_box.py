from pygame.constants import K_BACKSPACE, K_RETURN
import pygame

class TextBox:
    def __init__(self, screen, x, y, width, height, descriptive_text):
        pygame.init()
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect_object = pygame.Rect(self.x, self.y, self.width, self.height)

        self._active, self._hover = False, False

        self.descriptive_text = descriptive_text
        self.input_text = self.descriptive_text
        self.font_name = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(self.font_name, int(self.height))

        self.hover_color = (80, 86, 104) if not self._active else (255,255,255)
        self.normal_color = (80, 86, 104) if not self._active else (255,255,255)
        self.button_color = self.hover_color if self._hover else self.normal_color
        self.text_color = (241, 236, 225) if not self._active else (33,33,33)

    # A getter function for the active state
    def get_active(self):
        return self._active
    
    # Activates the text box
    def activate(self):
        self._active = True
        self.input_text = ''
    
    # Deactivates the text box
    def deactivate(self):
        self._active = False
        self.input_text = self.descriptive_text

    # Returnes true if the button is pressed
    def is_pressed(self, event_pos):
        return self.rect_object.collidepoint(event_pos)
    
    #Self contained draw function that handles the checking of hover
    def draw(self):
        self._check_mouse_hover()

        #Draw the box
        color = self.hover_color if self._hover else self.button_color
        pygame.draw.rect(self.screen, color, self.rect_object)

        #Draw the text from user centered on the textbox
        text = self.input_text
        
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width/2, self.y + self.height/2)
        self.screen.blit(text_surface, text_rect)

    #Self explanatory, checks if mouse is hovering over the text box
    def _check_mouse_hover(self):
        if self.rect_object.collidepoint(pygame.mouse.get_pos()):
            self._hover = True
        else:
            self._hover = False

    #Checks that the input is of whatever format the input "func" checks
    #For example, if func is "int" then the function checks that input is an integer
    def check_input(self, event, func):
        #Delete a character on backspace if the string is not empty
        if event.key == K_BACKSPACE and self.input_text:
            shortened_text = self.input_text[:-1]
            self.input_text = shortened_text

        #Set the step amount on enter. if the string does not convert to int, then retrun empty string
        elif event.key == K_RETURN:
            try:
                converted = func(self.input_text)
                self.input_text = ''
                return converted
            except:
                return ''

        else:
            self.input_text += str(pygame.key.name(event.key))
        
        


