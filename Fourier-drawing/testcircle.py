
import pygame
import math, cmath
class Game():
    def __init__(self, speed, xy_dim=1000):
        pygame.init()

        # Size values
        self.xy_dim = xy_dim
        self.speed = speed
        self.offset = 0
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
        n = 1
        i = complex(0,1)
        for n in range(1000):
            t = n*0.001
            z = cmath.exp(n*2*math.pi*1j*t)
            print(z)
            pygame.draw.circle(self.screen, (255,255,255), (self.center[0] + z.real*100, self.center[1] + z.imag*100), 1, width=1)

    def main_loop(self):
        
        while self.running:
            self.clock.tick(self.fps)
            self.event_check()
            self.screen.fill(self.background_color)
            self.draw(self.time)
            pygame.display.flip()
            self.time -= self.speed


#g = Game(0.03)
#g.main_loop()
def read():
    with open('./points.txt', 'r') as f:
        for line in f.readlines():
            x, y = line.split(',')
            print(f'x = {x}, y = {y}')
read()