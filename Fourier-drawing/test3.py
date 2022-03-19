from math import cos, sin
import pygame
import math, cmath

class Draw_Fourier():
    def __init__(self, xy_dim=1000):
        pygame.init()

        # Size values
        self.xy_dim = xy_dim
        self.offset = 0
        self.center = (self.xy_dim//2 + self.offset, self.xy_dim//2)
        
        # Colors 
        self.background_color = (10,10,10)
        self.draw_color = (242,242,242, 200)
        self.red = (200, 20, 20)

        # Game specific objects
        self.drawing_path = []
        self.time = 0
        self.vals = self.read_file('points.txt')
        self.speed = 2 * math.pi / len(self.vals)*0.1
        self.fourier = self.fourier_calc(self.vals)

        # Pygame objects
        self.fps = 20
        self.screen = pygame.display.set_mode((self.xy_dim, self.xy_dim))
        self.alpha_surface = pygame.Surface((self.xy_dim, self.xy_dim), pygame.SRCALPHA)
        self.alpha_surface.set_alpha(50)
        self.running = True
        self.clock = pygame.time.Clock()

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def fourier_calc(self, x):
        X = []
        N = len(x)
        for k in range(N):
            z = complex(0,0)
            for n in range(N):
               z += x[n]*(cos(2*math.pi*n*k/N) - sin(2*math.pi*n*k/N)*1j)
            z = complex(z.real/N, z.imag/N) 
            freq = k
            print('\n' + str(k) + '\n')

            X.append((z, freq))
        return X

    def draw(self, time):
        # Translate origin to center
        x = self.center[0]
        y = self.center[1]
        fourier = self.fourier
        # Go through computed fourier values
        for c, freq in fourier:
            oldx = x
            oldy = y
            r = cmath.polar(c)[0]
            x += r*cos(freq*time + cmath.phase(c))*0.1
            y += r*sin(freq*time + cmath.phase(c))*0.1
            pygame.draw.circle(self.alpha_surface, self.draw_color, (oldx, oldy), r, width=1)
            pygame.draw.line(self.screen, self.red, (oldx, oldy), (x, y), width=2)
            
        
        self.drawing_path.append((x,y))
        # Making the drawing_path animation
        if len(self.drawing_path) > 1:
            for i in range(len(self.drawing_path)-1):
                x_current = self.drawing_path[i][0]
                y_current = self.drawing_path[i][1]
                x_next = self.drawing_path[i+1][0]
                y_next = self.drawing_path[i+1][1]
                pygame.draw.line(self.screen, self.draw_color, (x_current, y_current), (x_next, y_next))
            #pygame.draw.line(self.screen, self.draw_color, (i+1+self.offset/2, self.drawing_path[i+1]), (x, y))

        if len(self.drawing_path) > 220:
            self.drawing_path.pop(0)
        pygame.draw.circle(self.screen, self.red, (-50, -50), 1, width=1,)
        pygame.draw.circle(self.screen, self.red, (oldx, oldy), 1, width=1,)
        pygame.draw.circle(self.screen, self.red, (oldx, oldy), 1, width=1,)
        self.screen.blit(self.alpha_surface, (0,0))
        pygame.display.update()

    def read_file(self, path):
        coord_list = []
        with open(path, 'r') as f:
            for line in f.readlines():
                x, y = line.split(',')
                print(f'x = {x}, y = {y}')
                coord_list.append(complex(int(x) - 250, int(y)-200))
        return coord_list

    def main_loop(self):
        
        while self.running:
            self.clock.tick(self.fps)
            self.event_check()
            self.screen.fill(self.background_color)
            self.alpha_surface.fill(self.background_color)
            self.draw(self.time)
            pygame.display.flip()
            
            self.time -= self.speed


g = Draw_Fourier()
g.main_loop()