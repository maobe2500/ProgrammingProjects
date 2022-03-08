#!/usr/bin/env python3
import os
import time
from cell import Cell


class Life:
    def __init__(self, init_file, width, height, alive_color, dead_color):
        self._world = {}
        self.width = width
        self.height = height
        self.init_file = init_file
        self.colors = {
                        'white': '⬜', 'blue': '🟦', 'purple': '🟪', 'vackert röd': '🟥',
                        'orange': '🟧', 'yellow': '🟨', 'brown': '🟫', 'diamond': 
                        '🔶', 'standard_alive': 'X', 'black': '⬛', 'standard_dead': '_'
                      }
        
        try:
            self.alive_color = self.colors[alive_color]
            self.dead_color = self.colors[dead_color]
        except:
            self.alive_color = self.colors['white']
            self.dead_color = self.colors['black']
        
        self._create_world()

    #Returns a formated string representation of the hashmap
    def __str__(self):
        #clears the terminal
        clear = 'cls' if os.name in ('nt','dos') else 'clear'
        os.system(clear)
        world = ''
        for j in range(0, self.height):
            row = ''
            for i in range(0, self.width): 
                cell_content = self.alive_color if self._world[(i,j)] == 1 else self.dead_color
                row += f'{cell_content}'
            row += '\n'
            world += row
        return world

    #A simple getter function
    #This is how you access the world from the outside
    def get_world(self):
        return self._world.copy()

    #A simple setter function
    #This is how you set the world from the outside
    def set_world(self, new_world):
        self._world = new_world

    #Creates the world directly on init
    def _create_world(self):
        for j in range(0, self.height):
            for i in range(0, self.width):
                self._world[(i,j)] = 0

    #finds the filepath if given a file (NOT USED)
    def find_filepath(self, init_file):
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name == init_file:
                    return os.path.abspath(init_file)

    #Seeds the world with data from a file
    def seed_world(self):
        with open(self.init_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                coordinates = line.split(' ')
                x = int(coordinates[0])
                y = int(coordinates[1][0:1])
                self._world[(x,y)] = 1


    #A helper function that creates an infinite grid
    def _wrap(self, x, y):
        return (x % self.width, y % self.height)

    #Returns the sum of all the neigbors of the input tuple containing
    #coordinates likes so: (x, y)
    def get_neighbors(self, coord_tuple):
        x = coord_tuple[0]
        y = coord_tuple[1]
    
        north = self._wrap(x, y+1)
        south = self._wrap(x, y-1) 
        west = self._wrap(x-1, y)
        east = self._wrap(x+1, y) 
        northwest = self._wrap(x-1, y+1)
        northeast = self._wrap(x+1, y+1) 
        southwest = self._wrap(x-1, y-1)
        southeast = self._wrap(x+1, y-1)
     


        neighbors =    [self._world[north], self._world[south], 
                        self._world[west], self._world[east], 
                        self._world[northwest], self._world[northeast], 
                        self._world[southwest], self._world[southeast]]
        
        return (sum(neighbors), [north, south, west, east, northwest, northeast, southwest, southeast])
    

    #Calculates the survival based on the amount of neighbors
    def survival(self, neighbors):
        if neighbors < 2 or neighbors > 3:
            return False
        else:
            return True

    #Calculates the birth based on the amount of neighbors
    def birth(self, neighbors):
        if neighbors == 3:
            return True
        else:
            return False

