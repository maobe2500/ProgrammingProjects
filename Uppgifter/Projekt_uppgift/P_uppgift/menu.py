import pygame
#A collection of GUI functions to be moved in to their own class at some point
class Menu:
    def __init__(self, screen, res_width, res_height, menu_area):
        self.screen = screen
        self.width = res_width
        self.height = res_height
        self.menu_area = menu_area

        pygame.init()

    
    def display_gui(self):
        #Pause/Start Button
        pause_x, pause_y = 0, self.res_height
        label = "Start" if self.paused else "Pause"
        pause_button = self.draw_button(pause_x, pause_y, self.pause_button_color)
        self.pause_button = pause_button
        self.draw_text_centered(pause_button.centerx, pause_button.centery, label)

        #Step button
        step_x, step_y = self.res_width / 2, self.res_height
        step_button = self.draw_button(step_x, step_y, self.step_button_color)
        self.step_button = step_button
        self.draw_text_centered(step_button.centerx, step_button.centery, "Step")

    def draw_text_centered(self, x, y, text, color=(250,250,250)):
        font = pygame.font.SysFont(self.font, 32)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface,text_rect)

    def draw_button(self, x, y, color):
        button = pygame.Rect(x, y, self.res_width / 2, self.menu_area)
        pygame.draw.rect(self.screen, color, button)

        return button