import pygame
from pygame import draw
import random

from pygame.constants import MOUSEMOTION

class Point:
    def __init__(self, coord_tuple, color):
        self.x, self.y = coord_tuple
        self.color = color



class Box:
    def __init__(self, center, width, height):
        self.x, self.y = center
        self.width = width
        self.height = height

    def contains(self, point):
        leftedge = self.x - self.width
        rightedge = self.x + self.width
        topedge = self.y + self.height
        loweredge = self.y - self.height
        return leftedge < point.x and point.x < rightedge and loweredge < point.y and point.y < topedge

    def intersects(self, box):
        left = self.x - self.width
        right = self.x + self.width
        top = self.y + self.height
        bottom = self.y - self.height
        box_left = box.x - box.width
        box_right = box.x + box.width
        box_top = box.y + box.height
        box_bottom = box.y - box.height
        return not (right < box_left or left > box_right or top < box_bottom or bottom > box_top)




class Quadtree:
    def __init__(self, screen, boundary):
        pygame.init()
        self.screen = screen
        self.node_capacity = 1
        self.points = []
        self.boudary = boundary
        self.divided = False

        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def insert(self, point):

        if not self.boudary.contains(point):
            return False

        if len(self.points) < self.node_capacity and not self.divided:
            self.points.append(point)
            return False
        else:
            if not self.divided:
                self.subdivide()
                self.divided = True

        if self.northwest.insert(point):
            return True
        if self.northeast.insert(point):
            return True
        if self.southwest.insert(point):
            return True
        if self.southeast.insert(point):
            return True

        return False

    def subdivide(self):
        nw = Box((self.boudary.x - self.boudary.width/2, self.boudary.y - self.boudary.height/2), self.boudary.width/2, self.boudary.height/2)
        self.northwest = Quadtree(self.screen, nw)
        ne = Box((self.boudary.x + self.boudary.width/2, self.boudary.y - self.boudary.height/2), self.boudary.width/2, self.boudary.height/2)
        self.northeast = Quadtree(self.screen, ne)
        sw = Box((self.boudary.x - self.boudary.width/2, self.boudary.y + self.boudary.height/2), self.boudary.width/2, self.boudary.height/2)
        self.southwest = Quadtree(self.screen, sw)
        se = Box((self.boudary.x + self.boudary.width/2, self.boudary.y + self.boudary.height/2), self.boudary.width/2, self.boudary.height/2)
        self.southeast = Quadtree(self.screen, se)

    def query_range(self, box_range, points=[]):

        if not box_range.intersects(self.boudary):
            return points

        for p in self.points:
            if box_range.contains(p):
                points.append(p)
                #print(p)

        if self.divided:
            self.northwest.query_range(box_range, points)
            self.northeast.query_range(box_range, points)
            self.southwest.query_range(box_range, points)
            self.southeast.query_range(box_range, points)

        return points
    
    def clear_qtree(self):
        self.points.clear()
        if self.divided:
            self.northwest.clear_qtree()
            self.northeast.clear_qtree()
            self.southwest.clear_qtree()
            self.southeast.clear_qtree()

    def print_contents(self):
        print(self.points)
        if self.divided:
            self.northwest.print_contents()
            self.northeast.print_contents()
            self.southwest.print_contents()
            self.southeast.print_contents()

    def show(self):
        rect = pygame.Rect(self.boudary.x, self.boudary.y, self.boudary.width*2, self.boudary.height*2)
        rect.center = (self.boudary.x, self.boudary.y)
        draw.rect(self.screen, (255,255,255), rect, width = 1)
        for p in self.points:
            pygame.draw.circle(self.screen, p.color, (p.x, p.y), 3)
            
        if self.divided:
            self.northwest.show()
            self.northeast.show()
            self.southwest.show()
            self.southeast.show()




width = 500
height = 500
screen = pygame.display.set_mode((width,height))
running = True
center = (width/2, height/2)
boundary = Box(center,width/2, height/2)
qt = Quadtree(screen, boundary)

WHITE = (225,225,225)
BLACK = (0,0,0)
GREEN = (0,255,0)
ps = []
for i in range(250):
    p = Point((random.randrange(0, width), random.randrange(0, height)), WHITE)
    qt.insert(p)
    ps.append(p)

while running:

    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_p = Point((mouse_pos[0], mouse_pos[1]), WHITE)
            ps.append(mouse_p)
            qt.insert(mouse_p)
            qt.show()

    screen.fill(BLACK)

    #Create and draw the visual box centered on the mouse
    range = Box(mouse_pos, 50, 50)
    rect = pygame.Rect(range.x, range.y, range.width * 2, range.height * 2)
    rect.center = mouse_pos
    draw.rect(screen, (0, 255, 0), rect, width=2)

    points = []
    qt.query_range(range, points)
    for p in ps:
        if p in points:
            p.color = GREEN 
        else:
            p.color = WHITE

    print(points)
    qt.show()
    pygame.display.update()


pygame.quit()