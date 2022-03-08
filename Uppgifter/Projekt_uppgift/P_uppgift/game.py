import pygame
from life import Life
from menu import Menu

class Game:
    def __init__(self, width, height, rect_size):
        pygame.init()
        #Size values
        self.width, self.height = width, height
        self.rect_size = rect_size
        self.offset = self.rect_size + 1
        self.res_width, self.res_height = self.width*self.offset, self.height*self.offset
        self.menu_area = self.res_height // 10

        #Game related values
        self.display = pygame.Surface((self.res_width, self.res_height + self.menu_area))
        self.screen = pygame.display.set_mode((self.res_width, self.res_height + self.menu_area))
        self.fps = 20
        self.running, self.paused = True, False

        #GUI related values
        self.black, self.white = (0,0,0), (255,255,255)
        self.font = pygame.font.get_default_font()
        self.button_color = (105,105,105)
        self.hover_color = (200,200,200)
        self.pause_button = None
        self.pause_button_color = self.button_color
        self.step_button = None
        self.step_button_color = self.button_color

        #Objects needed for the game
        self.clock = pygame.time.Clock()        
        self.life = Life(width, height)
        self.life.seed_world()

    #The only function called from the outside
    def main_loop(self):
        while self.running:
            self.clock.tick(self.fps)
            self.event_check()
            self.display_gui()
            self.freeze_on_pause()
            self.draw_grid()
            self.calculate_life()

    #Checks for events that happen during the game
    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.pause_button.collidepoint(event.pos):
                    self.paused = not self.paused
                if self.paused:
                    self.add_square()
                if self.step_button.collidepoint(event.pos):
                    self.calculate_life()
                    self.draw_grid()

            #Change hover color 
            mx, my = pygame.mouse.get_pos()
            if self.pause_button is not None and self.step_button is not None:

                if self.pause_button.collidepoint((mx, my)):
                    self.pause_button_color = self.hover_color
                else:
                    self.pause_button_color = self.button_color
                
                if self.step_button.collidepoint((mx, my)):
                    self.step_button_color = self.hover_color
                else:
                    self.step_button_color = self.button_color

    #Draws the grid that the user sees
    def draw_grid(self):
        world = self.life.get_world()
        for j in range(0, self.height):
            for i in range(0, self.width):

                rect = pygame.Rect(i*self.offset, j*self.offset, self.rect_size, self.rect_size)
                color = self.black if world[(i, j)] else self.white
                pygame.draw.rect(self.screen, color, rect)

        pygame.display.flip()
 
    #Calculates the next iteration of the world
    def calculate_life(self):
        temp_world = self.life.get_world()
        for j in range(-1, self.height+1):
            for i in range(-1, self.width+1):
                neighbors = self.life.get_neighbors((i, j))
                is_alive = temp_world[(i, j)]

                if is_alive:
                    if self.life.survival(neighbors):
                        temp_world[(i, j)] = 1
                    else:
                        temp_world[(i, j)] = 0
                else:
                    if neighbors:
                        if self.life.birth(neighbors):
                            temp_world[(i, j)] = 1

        self.life.set_world(temp_world)

    #Freezes the current screen so that user can add squares
    def freeze_on_pause(self):
        if self.paused:
            while self.paused:
                quit = self.event_check()
                if quit:
                    break
                self.draw_grid()
                pygame.display.flip()

    #adds a square at the mouse position
    def add_square(self):
        mx, my = pygame.mouse.get_pos()
        x = mx // self.offset
        y = my // self.offset
        print(x, y)
        temp_world = self.life.get_world()
        if y < self.height:
            if temp_world[(x, y)]:
                temp_world[(x, y)] = 0
            else:
                temp_world[(x, y)] = 1
        
        self.life.set_world(temp_world)
        
    #A collection of GUI functions to be moved in to their own class at some point

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


def debug():
    import cProfile
    import pstats
    game = Game(50, 50, 20)

    with cProfile.Profile() as pr:
        game.main_loop()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
#    stats.print_stats()
    stats.dump_stats(filename='needs_profiling.prof')

    pygame.quit()
debug()