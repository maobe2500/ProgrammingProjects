#!/usr/bin/env python3
import os
import time

class Life:
    def __init__(self, width, height):
        self._world = {}
        self.width = width
        self.height = height
        self.init_file = os.path.abspath('./P_uppgift/seed_file.txt')

        self._create_world()

    #Returns a formated string representation of the hashmap
    def __str__(self):
        world = ''
        for j in range(-1, self.height+1):
            row = '|'
            for i in range(-1, self.width+1): 
                row += '{:^11}|'.format(f'{(i,j)}')
            row += '\n'
            world += row
        return world

    #A simple getter function
    def get_world(self):
        return self._world.copy()

    #A simple setter function
    def set_world(self, new_world):
        self._world = new_world

    #Creates the world directly on init
    def _create_world(self):
        for j in range(-2, self.height+2):
            for i in range(-2, self.width+2):
                self._world[(i,j)] = 0

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

    #Returns the sum of all the neigbors
    def get_neighbors(self, coord_tuple):
        x = coord_tuple[0]
        y = coord_tuple[1]
        neighbors = [   
                        self._world[self._wrap(x, y+1)], self._world[self._wrap(x, (y-1))], 
                        self._world[self._wrap(x-1, y)], self._world[self._wrap(x+1, y)], 
                        self._world[self._wrap(x-1, y+1)], self._world[self._wrap(x+1, y+1)], 
                        self._world[self._wrap(x-1, y-1)], self._world[self._wrap(x+1, y-1)]
                    ]
        return sum(neighbors)

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
'''
l = Life(10, 10)
l.seed_world()
print(l)
print(l.get_neighbors((0, 2)))
print(l.birth(0,0))'''