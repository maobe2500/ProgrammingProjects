#!/usr/bin/env python3
from Textcolor import Text_colors

#Creates a matrix with the a given length and width 
def create_chocolate_bar(col_len, row_len):

    #For some reason a requirement???
    if col_len <= 0 or row_len <= 0:
        return None

    bar_matrix = []
    for i in range(11, col_len*11, 10):
        row = []
        for j in range(row_len):
            row.append(i + j)
        bar_matrix.append(row)
    return bar_matrix


#Goes through the matrix and prints the formatted version of each row
def print_chocolate_bar(bar_matrix):
    
    #A text formating class from another file used to make the code look cleaner
    t = Text_colors()
    
    for r_index in range(len(bar_matrix)):
        row = ""
    
        #Make the P red and the rest normal and add spaces in between
        for c_index, num in enumerate(bar_matrix[r_index]):
            if r_index == 0 and c_index == 0:
                row += "{:^15}".format(t.make_red("P"))
            else:
                row += "{:^6}".format(str(num))
        print(row)


def chomp(bar_matrix, chomp_num):
    
    #Finds the row and column of the number input by the user
    for i in range(len(bar_matrix)):
        for j, num in enumerate(bar_matrix[i]):
            if int(num) == chomp_num:
                row_num = i
                col_num = j

    #"chomps" the matrix at the each row and column index bigger than row_num and col_num
    chomped_matrix = bar_matrix
    for index, row in enumerate(bar_matrix):

        if row_num == 1 and col_num == 0:
            del bar_matrix[1:len(bar_matrix)]       #Dont mind me just doing some cleaning...
        if index >= row_num:
            del row[col_num:len(row)]
               
    return chomped_matrix

#Coninuously asks the player to input a correct number until they do
def ask_cell_number(bar):
    while True:
        try:
            found_flag = False
            chomp_num = int(input(", enter block number "))
            for row in bar:
                for num in row:
                    if num == chomp_num:
                        found_flag = True
                        break
            if found_flag: 
                break
            else:
                print("Number does not exitst in the chocolate bar", end="")
        except:
            print("Can only enter integers", end="")
            continue
    return chomp_num

#Checks if someone won 
def check_winner(bar):
    if len(bar) == 1 and len(bar[0]) == 1:
        return True
    else:
        return False

#Main game loop that handles the game logic
def game_loop(bar):
    turn = 0
    first_player = "First player"
    second_player = "Second player"
    print_chocolate_bar(bar)
    while True:
        
        #Check who is playing based on the turn number is even or odd
        currently_playing = first_player if turn % 2 == 0 else second_player
        print(f"{currently_playing}s turn", end="")

        #chomps the bar matrix and prints out the result
        chomp_num = ask_cell_number(bar)
        chomp(bar, chomp_num)
        
        #Checks if someone won and enbs the game if they did
        if check_winner(bar):
            print(f"{currently_playing} wins!!!")
            break
        print_chocolate_bar(bar)
        turn += 1
        

def main():
    t = Text_colors()
    while True:
        try:
            #Prints the welcome message and begins the game loop (game loop not yet in existance)
            print("\n*****************\n\nWelcome to chomp!\n\n*****************\n")
            
            rows = int(input("How many rows? "))
            cols = int(input("How many columns? "))
            bar = create_chocolate_bar(rows, cols)
            game_loop(bar)
            break

        #Gives the user another chance to give the correct input
        except Exception:
            print("Enter a correct value... ", end="")

            q_or_go = input("Press enter to continue or \"q\" to quit ")
            if q_or_go != "q":
                continue
            else:
                break


if __name__ == '__main__':
	main()
