import pygame
from pygame import draw
from life import Life
from game import Game

def main():
    game = Game(100, 100, 5)
    game.main_loop()
    pygame.quit()


if __name__ == '__main__':
    main()