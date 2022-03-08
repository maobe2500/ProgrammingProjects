import pygame
from GUI.button import Button
from GUI.text_box import TextBox

# This is just a wrapper class for organisation and made for easy buildout
#
# To do:
#   Automate the placing of the buttons
#   Automate the settings and add functions for drawing pregame selections menues
#
class Menu:
    def __init__(self, screen, res_width, res_height, menu_area):
        self.screen = screen
        self.res_width = res_width
        self.res_height = res_height
        self.menu_area = menu_area

        self.black, self.white = (0,0,0), (255,255,255)
        self.paused = False
        
        button_h = self.res_height//10
        
        # Pause button
        pause_x = 0
        pause_y = self.res_height
        pause_w = 2/9 * self.res_width

        # Step button
        step_x = 2/9 * self.res_width
        step_y = self.res_height
        step_w = 2/9 * self.res_width

        # clear button
        clear_x = 4/9 * self.res_width
        clear_y = self.res_height
        clear_w = 2/9 * self.res_width

        # Step input
        step_in_x = 2/3 * self.res_width
        step_in_y = self.res_height
        step_in_w = self.res_width/3

        self.pause_button = Button(self.screen, pause_x, pause_y, pause_w, button_h, 'Start', 'Pause')        
        self.step_button = Button(self.screen, step_x, step_y, step_w, button_h, 'Step')
        self.clear_button = Button(self.screen, clear_x, clear_y, clear_w, button_h, 'Clear')

        self.step_input = TextBox(self.screen, step_in_x, step_in_y, step_in_w+1, button_h/2+1, 'Input steps')
        self.save_button = Button(self.screen, step_in_x, self.res_height + button_h/2+1, step_in_w +1,button_h/2, 'Save state')
        pygame.init()


    # Draws the buttons and the inputs, this is made for future building purposes and not
    def draw(self):
        self.draw_buttons()
        self.step_input.draw() 

    # Gathers all the buttons
    # In the future this will be done automatically
    def draw_buttons(self):
        self.pause_button.draw()
        self.step_button.draw()
        self.save_button.draw()
        self.clear_button.draw()
