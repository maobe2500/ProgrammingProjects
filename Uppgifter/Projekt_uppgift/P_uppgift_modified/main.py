import pygame
from game import Game
import os


"""


Creator: Marcus Öberg
Date: 06-01-2022

Revisionsdatum: 12-01-2022 

"""



#
#Prints welcome message with usage info
#
def welcome():
    print('\n\n')
    filler = '{:^50}\n'.format('*******************************************************')
    print(filler*2)
    print('{:^50}\n'.format('Welcome!'))
    print(filler*2)
    print('\nUsage:\n\n')
    print('Path: The path to the seed file in the format of \"X Y\" on each line.\nThis is the format the world is saved in in the GUI version\n')
    print('Size: The size of the world. Cannot be bigger than 60 or smaller than 10,\nand will default to 20 if not in this range\n')
    print('Generations: The amount of generations before the world pauses\n')
    print('Steps: (Terminal only) The amount of generation it should calculate each time you press enter\n\n')
    print(filler*2)
    print('{:^50}\n'.format('READ BEFORE USING!!!\n'))
    print(filler*2)
    print('\nControls for terminal:')
    print('\nPress \"s\" to start and space bar to pause\nEnter key is used for stepping.\nEsc key exits the program\n\n')
    print(filler)

#
#Recives the settings and checks that they are in the right format
#
def input_stuff():
    print("\n\nInput the path to seed file, desired size and number of generations, press enter to skip and use standard\n")
    path = input('Path: ')
    size = input('Size: ')
    num_gen = input('Generations (For no maximum press enter): ')
    size = int(size) if size.isdigit() else 50
    num_gen = int(num_gen) if num_gen.isdigit() else False

    if path:
        print('\nSeeding from path...')
        return path, size, num_gen
    else:
        print('\nSeeding from standard file...')
        return None, size, num_gen

#
#Asks whether of not the user wants the terminal version
#If true it returns True and the answer of all terminal-related questions 
#If false it returns False and None for all answers
#
def check_terminal():
    terminal_bool = input('Would you like to use the terminal version (y | n): ')
   
    if terminal_bool.lower() == 'y':
        steps = input('Steps per generation: ')
        alive_color = input('(optional) choose: color for alive squares: ')
        dead_color = input('(optional) choose: color for dead squares: ')

        steps = int(steps) if steps.isdigit() else 1
        return True, steps, alive_color, dead_color
    
    else:
        return False, None, None, None
#
#Checks that the coordinates are within the width and height of the world
#Takes in the max width and height and returns a boolean answer 
#
def check_coordinates(init_file, x_max, y_max):
        try:
            with open(init_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    coordinates = line.split(' ')
                    x = int(coordinates[0])
                    y = int(coordinates[1][0:1])
                    if x > x_max or y > y_max:
                        print('World is too small to use this seed file... Starting standard world')
                        return False
                return True
        except:
            print("\nFile does not exist or is unreachable, starting standard world...\n")
            return False


def main():
    welcome()
    default_file = os.path.abspath('./Resources/seed_file.txt')

    try:
        path, size, num_gen = input_stuff()
        terminal_bool, steps, alive_color, dead_color = check_terminal()

        path = path if check_coordinates(path, size, size) else default_file
        #making sure the size isnt too big or small for the terminal
        size = 20 if terminal_bool and (size > 60 or size < 10) else size
        steps = int(steps) if steps else 1

        game = Game(size, size, 20, path, num_gen, GUI=not terminal_bool, num_steps=steps, alive_color=alive_color, dead_color=dead_color)

    except Exception as e:
        print(e)
        print('\nStarting with standard settings...\n\n')
        game = Game(50, 50, 20, default_file)

    game.main_loop()
    pygame.quit()


if __name__ == '__main__':
    main()