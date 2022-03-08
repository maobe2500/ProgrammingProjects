#!/usr/bin/env python3

from PIL import Image, ImageDraw
import sys


def check_args(col_tuple):
    if (sys.argv[2] == 'b'):
        if (sys.argv[3] == 'r'):
            r = col_tuple[2]
            g = col_tuple[1]
            b = col_tuple[0]

    if (sys.argv[2] == 'g'):
        if (sys.argv[3] == 'r'):
            r = col_tuple[1]
            g = col_tuple[0]
            b = col_tuple[2]

    if (sys.argv[2] == 'r'):
        if (sys.argv[3] == 'g'):
            r = col_tuple[1]
            g = col_tuple[0]
            b = col_tuple[2]

    if (sys.argv[2] == 'b'):
        if (sys.argv[3] == 'g'):
            r = col_tuple[0]
            g = col_tuple[2]
            b = col_tuple[1]

    if (sys.argv[2] == 'r'):
        if (sys.argv[3] == 'b'):
            r = col_tuple[2]
            g = col_tuple[1]
            b = col_tuple[0]

    if (sys.argv[2] == 'g'):
        if (sys.argv[3] == 'b'):
            r = col_tuple[0]
            g = col_tuple[2]
            b = col_tuple[1]
    return (r, g, b)


def check_last_arg(col_tuple):
    
    r = col_tuple[0]
    g = col_tuple[1]
    b = col_tuple[2]

    if (sys.argv[4] == 't'):
        
        if (sys.argv[3] == 'r'):
            r += round((255 - col_tuple[0]) / 2)
        elif (sys.argv[3] == 'g'):
            g += round((255 - col_tuple[1]) / 2)
        else:
            b += round((255 - col_tuple[2]) / 2)

    elif (sys.argv[4] == 'td'):

        if (sys.argv[3] == 'r'):
            r += 2 * round((255 - col_tuple[0]) / 2)
        elif (sys.argv[3] == 'g'):
            g += 2 * round((255 - col_tuple[1]) / 2)
        else:
            b += 2 * round((255 - col_tuple[2]) / 2)

    elif (sys.argv[4] == 'ts'):

        if (sys.argv[3] == 'r'):
            r += round((255 - col_tuple[0]) / 4)
        elif (sys.argv[3] == 'g'):
            g += round((255 - col_tuple[1]) / 4)
        else:
            b += round((255 - col_tuple[2]) / 4)
        

    elif (sys.argv[4] == 'f'):
    
        pass

    else:

        raise Exception('Argument 3 not recognized.\n')
    
    return (r, g, b)


with Image.open(sys.argv[1]) as im:
    width, height = im.size
    image = im.load()
    pixels = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(pixels, 'RGB')

    if (not (sys.argv[2] == 'r' or sys.argv[2] == 'g' or sys.argv[2] == 'b')):
    	print('\nPlease input either \'r\', \'g\' or \'b\' for the color to change\n')
    	print('\nUsage: filename color-code-to-change color-code-to-change-to\n')
	 
    try:
        for i in range(width - 1):
            for j in range(height - 1):							
                col_tuple = image[i,j]
                
                switched_col_tuple = check_args(col_tuple)
                new_col_tuple = check_last_arg(switched_col_tuple)
                draw.point((i, j), fill=new_col_tuple)
    
            print(f'{i / width * 100}')	

        pixels.save(f'{sys.argv[1][:-4]}-{sys.argv[2]}-to-{sys.argv[3]}({sys.argv[4]}).jpg')

    except:
    	print('please add at least \'t\' or \'f\' to set highlighting to true or false')


