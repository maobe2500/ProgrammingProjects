#!/usr/bin/env python3
from TV import TV as Tv


#Reads the file
def read_file(file):
    with open(file) as f:
        tv_list = f.readlines()
        object_lst = []
        
        #For every string in a line, separate out the attributes
        #and create a tv object, then return it
        for attr_string in tv_list:
            attr = attr_string.split(',')
            tv = Tv(attr[0], int(attr[1]),int(attr[2]),int(attr[3]),int(attr[4]))
            object_lst.append(tv) 
        return object_lst

#Writes the attributes, comma separated, on each line
def write_file(tv_list, file):
    with open(file, 'w') as f:
        for tv in tv_list:
            f.write(tv.str_for_file())

#Changes the channel of the input tv
def change_channel(TV):
    print('\nEnter channel number: ', end='')
    while True:
        try:
            new_channel = int(input())
r           
            #Checks if able to change to given channel
            if TV.change_channel(new_channel):
                TV.change_channel(new_channel)
                break
            
            else:
                print(f'This tv has channel range 1 to {TV.max_channel}, try again: ', end='')
        except:
            print('\nOnly intagers allowed, try again: ', end='')
   
def increase_volume(TV):
    TV.increase_volume()

def decrease_volume(TV):
    TV.decrease_volume()

#Prints the options to manipulate tv object and returns the selection
def adjust_menu():
    print('1. change channel \n2. increase volume \n3. decrease volume \n4. return to main menu\n')
    sel = int(input('Select option: '))
    return sel  

def select_TV_menu(TV_list):
    #Prints the tvs as options plus an exit option
    exit_option = len(TV_list) + 1
    for index, TV in enumerate(TV_list):
        print(f'{index + 1}. {TV.tv_name}\n')
        
    print(f'{exit_option}. exit\n')
    
    #Make sure the input at least 
    while True:
        sel = int(input('Select option: '))
        if sel <= exit_option:
            break
        else:
            print('Invalid option, try again.\n')
    
    return TV_list[sel - 1] if sel < exit_option else None



def main():
    obj_list = read_file('./tv_cache.txt')
    
    #Main menu loop
    while True:
        try:
            TV = select_TV_menu(obj_list)
            if TV == None:
                break
            print(f'\n{TV}\n')
            
            #Individual tv loop
            while True:

                #Handeling rouge input
                try:
                    sel = adjust_menu()
                    if sel == 1:
                        change_channel(TV)
                    elif sel == 2:
                        increase_volume(TV)
                    elif sel == 3:
                        decrease_volume(TV)
                    else:
                        break
                except:
                    print('Invalid option, try again.')
        except:
            print('Only integers allowed...') 

    #saves the settings to cache
    write_file(obj_list, './tv_cache.txt')

        
if __name__ == '__main__':
    main()

