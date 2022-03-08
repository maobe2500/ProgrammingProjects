import pygame
from pygame import event
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
        
        #Objects needed for the game
        self.clock = pygame.time.Clock()        
        self.life = Life(width, height)
        self.life.seed_world()
        self.menu = Menu(self.screen, self.res_width, self.res_height, self.menu_area)

    #Checks for events that happen during the game
    def event_check(self):
        #self.menu.event_check()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(self.paused)
                if self.paused:
                    self.add_square()

                if self.menu.pause_button.rect_object.collidepoint(event.pos):
                    self.paused = not self.paused

    #The only function called from the outside
    def main_loop(self):
        while self.running:
            self.clock.tick(self.fps)
            self.event_check()
            self.draw_grid()
            self.calculate_life()

            #print(pygame.mouse.get_pressed()[0])

            self.pause_loop()

            self.menu.draw()

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

    def pause_loop(self):
        if self.paused:
            print('IS ACTIVE')

            while self.paused and self.running:
                self.event_check()
                self.draw_grid()
                pygame.display.flip()


def debug():
    import cProfile
    import pstats
    game = Game(200, 200, 5)

    with cProfile.Profile() as pr:
        game.main_loop()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
#    stats.print_stats()
    stats.dump_stats(filename='needs_profiling.prof')

    pygame.quit()
debug()