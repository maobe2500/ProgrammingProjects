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
        if index >= row_num:
            del row[col_num:len(row)]
    print_chocolate_bar(chomped_matrix)
    return chomped_matrix


def main():
    t = Text_colors()
    while True:
        try:
            #Prints the welcome message and begins the game loop (game loop not yet in existance)
            print("\n*****************\n\nWelcome to chomp!\n\n*****************\n")
            
            rows = int(input("How many rows? "))
            cols = int(input("How many columns? "))
            bar = create_chocolate_bar(cols, rows)
            print_chocolate_bar(bar)
            chomp_num = int(input("Enter block number "))
            chomp(bar, chomp_num)
            break

        #Gives the user another chance to give the correct input
        except Exception as e:
            print( "\n" + t.make_red(str(e)) + "\n" )
            print("Enter a correct value or type \"q\" to quit.")
            q_or_go = input("Press enter to continue or \"q\" to quit ")
            if q_or_go != "q":
                continue
            else:
                break


if __name__ == '__main__':
	main()
