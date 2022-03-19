from math import cos, sin
import pygame
from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom
import math

class Game():
    def __init__(self, speed, xy_dim=1000):
        pygame.init()

        # Size values
        self.xy_dim = xy_dim
        self.speed = speed
        self.offset = 200
        self.center = (self.xy_dim//2 + self.offset, self.xy_dim//2)
        
        # Colors 
        self.background_color = (10,10,10)
        self.draw_color = (242,242,242, 200)
        self.red = (200, 20, 20)

        # Game specific objects
        self.wave = []
        self.time = 0

        # Pygame objects
        self.fps = 50
        self.screen = pygame.display.set_mode((self.xy_dim, self.xy_dim))
        self.running = True
        self.clock = pygame.time.Clock()

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    

    def draw(self, time):
        x = self.center[0]
        y = self.center[1]
        for i in range(50):
            n = i*2 + 1
            oldx = x
            oldy = y
            self.mother_radius = 100 * 4/(n*math.pi)
            x += self.mother_radius * cos(n*time)
            y += self.mother_radius * sin(n*time)
            
            pygame.draw.circle(self.screen, self.draw_color, (oldx, oldy), self.mother_radius, width=1,)
            pygame.draw.line(self.screen, self.red, (oldx, oldy), (x, y), width=2)
        self.wave.append(y)
        if len(self.wave) > 1:
            for i in range(len(self.wave)-1):
                pygame.draw.line(self.screen, self.draw_color, (i+self.offset/2, self.wave[i]), ( i+1+self.offset/2, self.wave[i+1]))
            pygame.draw.line(self.screen, self.draw_color, (i+1+self.offset/2, self.wave[i+1]), (x, y))

        if len(self.wave) > 200:
            self.wave.pop(0)

    def main_loop(self):
        
        while self.running:
            self.clock.tick(self.fps)
            self.event_check()
            self.screen.fill(self.background_color)
            self.draw(self.time)
            pygame.display.flip()
            self.time -= self.speed


g = Game(0.03)
g.main_loop()