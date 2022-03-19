import pygame
from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom

class Game():
    def __init__(self, svg_file_path, svg_mode=True):
        pygame.init()
        self.svg_file_path = svg_file_path
        self.coord_list = []
        self.xy_dim = 500
        self.read_svg()
        self.screen = pygame.display.set_mode((self.xy_dim, self.xy_dim))
        self.running = True
        self.background_color = (100,100,100)
        self.draw_color = (242,242,242)
        self.svg_mode = svg_mode
        self.center = (self.xy_dim//2, self.xy_dim//2)

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # read the SVG file
    def read_svg(self):
        path = parse_path('M 50 50 L 200 50 L 100 200 L 50 50' )
        print(path)
        for e in path:
            if isinstance(e, Line):
                x0 = e.start.real
                y0 = e.start.imag
                x1 = e.end.real
                y1 = e.end.imag
                coord_tuple = (x0, y0, x1, y1)

                # Making sure the drawing fits on the screen
                if max(coord_tuple) > self.xy_dim:
                    self.xy_dim = max(coord_tuple) + 100
                self.coord_list.append(self.translate(coord_tuple))

    def translate(self, coord_tuple):
        new_coords = []
        for coord in coord_tuple:
            coord = self.xy_dim//2 + coord
            new_coords.append(coord)
        return new_coords

    def draw_svg(self):
        for coord in self.coord_list:
            pygame.draw.line(self.screen, self.draw_color,(coord[0], coord[1]),(coord[2], coord[3]))




    def draw_standard(self):
        radius = 75
        pygame.draw.circle(self.screen, self.draw_color, radius)
        pygame.draw.line(self.screen, self.center, self.center + radius)




    def draw(self):
        self.screen.fill(self.background_color)
        if self.svg_mode == True:
            self.draw_svg()
        else:
            pygame.draw_standard()
        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.event_check()
            self.draw()


g = Game('./ftmath-prod.svg')
g.main_loop()