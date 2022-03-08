#!/usr/bin/env python3
import os
import time
from cell import Cell


class Life:
    def __init__(self, init_file, width, height, alive_color, dead_color):
        #self._world = {}
        self._cells = {}        #Comment out to return to normal
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
    def print_world(self):
        #clears the terminal
        clear = 'cls' if os.name in ('nt','dos') else 'clear'
        os.system(clear)
        world = ''
        for j in range(0, self.height):
            row = ''
            for i in range(0, self.width): 
                cell_content = self.alive_color if self._cells[(i,j)].val == 1 else self.dead_color
                #cell_content = self.alive_color if self._world[(i,j)] == 1 else self.dead_color
                row += f'{cell_content}'
            row += '\n'
            world += row
        print(world)

    #A simple getter function
    def get_world(self):
        return self._cells.copy()
        #return self._world.copy()

    #A simple setter function
    def set_world(self, new_world):
        #self._world = new_world
        self._cells = new_world

    #Creates the world directly on init
    def _create_world(self):
        for j in range(0, self.height):
            for i in range(0, self.width):
                cell = Cell(0)
                self._cells[(i, j)] = cell
                #self._world[(i,j)] = 0

    #finds the filepath
    def find_filepath(self, init_file):
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name == init_file:
                    return os.path.abspath(init_file)

    #Seeds the world with data from a file if the file is not correct format it seeds with standard seed file
    def seed_world(self):
        with open(self.init_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                coordinates = line.split(' ')
                x = int(coordinates[0])
                y = int(coordinates[1][0:1])
                self._cells[(x,y)].val = 1
                #self._world[(x,y)] = 1


    #A helper function that creates an infinite grid
    def _wrap(self, x, y):
        return (x % self.width, y % self.height)

    #Returns the sum of all the neigbors
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
     

        neighbors =    [self._cells[north], self._cells[south], 
                        self._cells[west], self._cells[east], 
                        self._cells[northwest], self._cells[northeast], 
                        self._cells[southwest], self._cells[southeast]]

        """
        neighbors =    [self._world[north], self._world[south], 
                        self._world[west], self._world[east], 
                        self._world[northwest], self._world[northeast], 
                        self._world[southwest], self._world[southeast]]
        
        return (sum(neighbors), [north, south, west, east, northwest, northeast, southwest, southeast])
        """
        #___________________new stuff_______________________
        sum = 0
        for neighbor in neighbors:
            sum += neighbor.val
        
        return (sum, neighbors)


    #Calculates the survival for a point
    def survival(self,neighbors):
        if neighbors < 2 or neighbors > 3:
            return False
        else:
            return True

    #Calculates the birth for a point
    def birth(self, neighbors):
        if neighbors == 3:
            return True
        else:
            return False

