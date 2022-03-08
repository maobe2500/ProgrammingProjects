import keyboard
import pygame
from life import Life
from GUI.menu import Menu
import os, sys
import time

class Game:
    def __init__(self, width, height, rect_size, init_file, num_gen=False, GUI=True, num_steps=1, alive_color='white', dead_color='black'):
        pygame.init()
        #Size values
        self.width, self.height = width, height
        self.rect_size = rect_size
        self.offset = self.rect_size
        self.res_width, self.res_height = self.width*self.offset, self.height*self.offset
        self.menu_area = self.res_height // 10

        #Game related values
        self.GUI = GUI
        self.fps = 20
        self.num_steps = num_steps
        self.running, self.clearing_time = True, False
        self.cache = set()
        self.num_gen = num_gen
        self.paused = True
        self.init_file = init_file

        #GUI related values
        self.dead_color, self.white, self.alive_color, self.cache_color = (241, 236, 225), (255,255,255), (192, 88, 80), (226, 171, 127)

        #Objects needed for the game
        self.clock = pygame.time.Clock()

        if self.GUI:
            self.display = pygame.Surface((self.res_width, self.res_height + self.menu_area))
            self.screen = pygame.display.set_mode((self.res_width, self.res_height + self.menu_area))
            self.menu = Menu(self.screen, self.res_width, self.res_height, self.menu_area)

        self.life = Life(init_file, width, height, alive_color, dead_color)
        self.life.seed_world()


    #(GUI Only) Checks for events that happen during the game
    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu.pause_button.is_pressed(event.pos):
                    self.paused = not self.paused
                    self.menu.pause_button.toggle_active()
                if self.menu.step_button.is_pressed(event.pos) and self.paused:
                    self.step(self.num_steps)
                if self.menu.save_button.is_pressed(event.pos) and self.paused:
                    self.save()
                if self.menu.clear_button.is_pressed(event.pos) and self.paused:
                    self.clearing_time = True

                if self.menu.step_input.is_pressed(event.pos):
                    self.menu.step_input.activate()
                else:
                    self.menu.step_input.deactivate()


            if event.type == pygame.KEYDOWN and self.menu.step_input.get_active():
                step_int = self.menu.step_input.check_input(event, int)
                if step_int:
                    self.num_steps = step_int
                else:
                    self.num_steps = 1


    #(Terminal only) checks which key is pressed
    def check_press(self):
        if keyboard.is_pressed('s'):
            self.paused = False
        if keyboard.is_pressed('space'):
            self.paused = True
        if keyboard.is_pressed('esc'):
            self.running = False
        if keyboard.is_pressed('enter'):
            self.step(self.num_steps)


    def GUI_loop(self):
        self.clock.tick(self.fps)
        self.menu.draw()
        self.event_check()
        self.calculate_life()
        self.draw_grid()
        if self.paused:
            self.pause_loop()
        if self.clearing_time:
            self.clear()
            self.clearing_time = False

    def terminal_loop(self):
        self.check_press()
        self.calculate_life()
        self.draw_grid()
        if self.paused:
            self.pause_loop()
        time.sleep(0.1)
        

    #The only function called from the outside
    def main_loop(self):
        gen = 0
        while self.running:
            if self.GUI:
                self.GUI_loop()
            else:
                self.terminal_loop()

            #Pauses the game when it has reached the desired generation
            if self.num_gen:
                #Need to do -1 since it has to do another generation before it gets triggered
                if gen == self.num_gen - self.num_steps - 1:
                    self.paused = True

            gen += 1


    #Draws the grid that the user sees
    def draw_grid(self):
        if self.GUI:
            world = self.life.get_world()
            for j in range(0, self.height):
                for i in range(0, self.width):

                    rect = pygame.Rect(i*self.offset, j*self.offset, self.rect_size, self.rect_size)
                    n_col = self.cache_color if (i, j) in self.cache else self.dead_color
                    #color = self.alive_color if world[(i, j)] else n_col
                    color = self.alive_color if world[(i, j)].val else n_col
                    

                    pygame.draw.rect(self.screen, color, rect)

            pygame.display.flip()
        else:
            self.life.print_world()


    #Calculates the next iteration of the world manually at first and the uses cache instead
    def calculate_life(self):
        temp_world = self.life.get_world()
        if not self.cache:
            for j in range(0, self.height):
                for i in range(0, self.width):
                    num_neighbors, neighbors = self.life.get_neighbors((i, j))
                    coord_tuple = (i, j)
                    temp_world = self.evolve(temp_world, num_neighbors, coord_tuple)

 #                   if temp_world[(i, j)].val:
                    #if temp_world[(i, j)]:
  #                      for neighbor in neighbors:
  #                          self.cache.add(neighbor)
                        #self.cache.add(coord_tuple)
 #                       self.cache.add(temp_world[coord_tuple])

            self.life.set_world(temp_world)
    """    else:
            temp_cache = set()
            #for coord_tuple in self.cache:
            for coord_tuple in self.cache:
                num_neighbors, neighbors = self.life.get_neighbors(coord_tuple)
                temp_world = self.evolve(temp_world, num_neighbors, coord_tuple)

                #if temp_world[coord_tuple]:
                if temp_world[coord_tuple].val:
                    for neighbor in neighbors:
                        temp_cache.add(neighbor)
                    temp_cache.add(coord_tuple)

            self.cache = temp_cache
            self.life.set_world(temp_world)
"""

    #Updates a cell to the next generation
    def evolve(self, temp_world, num_neighbors, coord_tuple):
        if temp_world[coord_tuple]:
            if self.life.survival(num_neighbors):
                #temp_world[coord_tuple] = 1
                temp_world[coord_tuple].val = 1

            else:
                #temp_world[coord_tuple] = 0
                temp_world[coord_tuple].val = 0
        else:
            if num_neighbors:
                if self.life.birth(num_neighbors):
                    #temp_world[coord_tuple] = 1
                    temp_world[coord_tuple].val = 1
        return temp_world


    #(GUI Only) Adds a square at the mouse position
    def add_life(self, life_bool):
        mx, my = pygame.mouse.get_pos()
        temp_world = self.life.get_world()
        i = mx // self.offset
        j = my // self.offset
        if j < self.height:
            # If life bool is false we add death *(unless the current cell is a neighbors) 
            # if it is posetive we add life
            if not life_bool:

                #temp_world[(i, j)] = 0
                temp_world[(i, j)].val = 0

                #                           Since we dont want to remove neighbors
                #if (i, j) in self.cache and temp_world[(i, j)]:
                if temp_world[(i, j)] in self.cache and temp_world[(i, j)].val:
                    #self.cache.remove((i, j))
                    self.cache.remove(temp_world[(i, j)])
            else:   
                #temp_world[(i, j)] = 1
                temp_world[(i, j)].val = 1
                #self.cache.add((i, j))
                self.cache.add(temp_world[(i, j)])
        self.draw_grid()
        self.life.set_world(temp_world)

    #(GUI Only) Removes all life from the world in both cache and actual world
    def clear(self):
        temp_world = self.life.get_world()
        for coord_tuple in self.cache:
            #temp_world[coord_tuple] = 0
            temp_world[coord_tuple].val = 0
        self.life.set_world(temp_world)
        self.cache = set()

    #The loop that runs during pause where the user can add or remove squares and step through the generations
    def pause_loop(self):
        if self.GUI:
            while self.paused and self.running:

                self.event_check()
                if pygame.mouse.get_pressed()[0]:
                    self.add_life(True)
                if pygame.mouse.get_pressed()[2]:
                    self.add_life(False)
                if self.clearing_time:
                    self.clear()
                    self.clearing_time = False

                self.draw_grid()
                self.menu.draw()
                pygame.display.flip()
        else:
            while self.paused and self.running:
                self.check_press()
                self.draw_grid()
                time.sleep(0.1)

    #Saves the current state in a file in the same format as the init_file and files from Vahid
    def save(self):
        with open(f'./Resources/Saves/save_at_{time.time()}.txt', 'w') as f:
            world = self.life.get_world()
            for coord_tuple in world.keys():
                #if world[coord_tuple]:
                if world[coord_tuple].val:
                    f.write(f'{coord_tuple[0]} {coord_tuple[1]}\n')

    #Steps through X number of generations 
    def step(self, num_steps):
        for _ in range(num_steps):
            self.calculate_life()
        self.draw_grid()

"""
def debug():
    import cProfile
    import pstats
    game = Game(20, 20, 20,'seed_file.txt')

    with cProfile.Profile() as pr:
        game.main_loop()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
#    stats.print_stats()
    stats.dump_stats(filename='poop.prof')

    pygame.quit()
debug()"""