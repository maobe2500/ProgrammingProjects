#!/usr/bin/env python3
import random

#Prints a table of celsius to farenheit conversions from 0 to 20
def display_farenheit_to_celsius():

    #Creates the headers for the C and F
    c_header = "{:_^7}".format("C")
    f_header = "{:_^7}".format("F")
    print(f"|{c_header}|{f_header}|")

    #Prints the formatet table of values
    for i in range(20):

        c_string = "{:^7}".format(i)
        f = (i * 9 + 160) / 5
        f_string = "{:^7}".format(f)

        print(f"|{c_string}|{f_string}|")

#class used for formating text 
class Text_colors:
    def __init__(self):
        self._YELLOW = '\033[93m'
        self._RED = '\033[91m'
        self._NORMAL = '\033[0m'

    def make_yellow(self, data):
        return self._YELLOW + f"{data}" + self._NORMAL 

    def make_red(self, data):
        return self._RED + f"{data}" + self._NORMAL

#Returns a list with random numbers
def get_dice(num_dice):
    dice = []
    for _ in range(int(num_dice)):
        die = random.randint(1, 6)
        dice.append(die)
    return dice

#Simulates the rolling of the dice
def roll(dice):
    for i, dice_val in enumerate(dice):
        print(f"Dice number {i}: {dice_val}")

#The main logic for the dice game 
def roll_dice(num_dice, num_turns):
    start_quit = input("\nPress enter to roll, \"q\" to quit. ")
    if start_quit != "q":

        for i in range(num_turns):
     
            dice = get_dice(num_dice)
            roll(dice)
            if i < num_turns - 1:
                go_again = input("Roll again? (y,n) ")
            else:
                go_again = "n"

            if go_again == "y":
                continue
            else:
                break
        return f"You got {str(dice)[1:-1]}"
    else:
        return False


#A thin wrapper for the dice game to get info and break out of the game
def dice_game():
    num_dice = int(input("How many dice do you need? "))
    num_rolls = int(input("How many rolls per player? "))
    while True:
        result = roll_dice(num_dice, num_rolls)
        if result:
            print(result)
        else:
            break

#Displays a multiplication table with color red for squares and orange for the numbers being muliplied
def display_multiplication_table(first_number, second_number):
    i = 0
    t = Text_colors()
    while i <= first_number:
        j = 1
        row = "|"        #Ugly fix  

        while j <= second_number:
            if i == 0:                                              #First row is yellow
                row += "{:_^14}|".format(t.make_yellow(i + 1 * j))  
            elif i == j:                                            #Squares are red
                row += "{:^14}|".format(t.make_red(i * j))          
            else:                                                   
                row += "{:^5}|".format(i * j)                       #Other numbers are grey
            j += 1

        left_column = "|{:^14}".format(t.make_yellow(i))
        x_square = "|{:_^14}".format(t.make_yellow("X"))
        print(left_column + row if i > 0 else x_square + row)
        i += 1

def main():
    choice = input("Press \"m\" for multiplicationtable\nPress \"f\" for farenheit to celsius\nPress \"d\" for dice game\n")
    try:
        if choice == "m":
            number1 = int(input("Choose 1st number "))
            number2 = int(input("Choose 2nd number "))
            display_multiplication_table(number1,number2)
        elif choice == "f":
            display_farenheit_to_celsius()
        else:
            dice_game()
    except:
        print("Enter a correct value.")

if __name__ == '__main__':
    main()