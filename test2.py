from math import cos, sin
from random import randrange
import pygame
from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom
from perlin_noise import PerlinNoise
import math, cmath

class Game():
    def __init__(self, xy_dim=1000):
        pygame.init()

        # Size values
        self.xy_dim = xy_dim
        
        self.offset = 200
        self.center = (self.xy_dim//2 + self.offset, self.xy_dim//2)
        
        # Colors 
        self.background_color = (10,10,10)
        self.draw_color = (242,242,242, 200)
        self.red = (200, 20, 20)

        # Game specific objects
        self.wave = []
        self.time = 0
        self.noise = PerlinNoise()
        self.vals = [randrange(0, 200) for _ in range(10)]
        self.speed = 0.03 #2 * math.pi / len(self.vals)

        # Pygame objects
        self.fps = 20
        self.screen = pygame.display.set_mode((self.xy_dim, self.xy_dim))
        self.running = True
        self.clock = pygame.time.Clock()

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def fourier(self, x):
        X = []
        N = len(x)
        for k in range(N):
            real, imag = 0, 0
            for n in range(N):
               real += x[n]*cos(2*math.pi*n*k/N) 
               imag -= x[n]*sin(2*math.pi*n*k/N)
            real = real / N
            imag = imag / N
            z = complex(real, imag) 
            phase = cmath.phase(z)
            polar = cmath.polar(z)
            amp = polar[0]
            phase = polar[1]
            freq = k
            print('\n' + str(k) + '\n')

            X.append((z, phase, amp, freq))
        return X


    def draw(self, time):
        x = self.center[0]
        y = self.center[1]
        fourier = self.fourier(self.vals)
        for i in range(len(self.vals)):
            oldx = x
            oldy = y
            z = fourier[i][0]
            phase = fourier[i][1]
            amp = fourier[i][2]
            freq = fourier[i][3]
            radius = amp
            x += radius * cos(freq*time + phase)
            y += radius * sin(freq*time + phase)
            
            pygame.draw.circle(self.screen, self.draw_color, (oldx, oldy), radius, width=1,)
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


g = Game()
g.main_loop()