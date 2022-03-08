import sys
from PIL import Image, ImageDraw
from concurrent.futures import ProcessPoolExecutor
import time

Width = int(sys.argv[1])
Height = int(sys.argv[2])
Max_iter = int(sys.argv[3])

def main(args):
#    print("In main: Width/Height/Max_iter=", Width, Height, Max_iter)

    nw = 1
    if (len(args) > 3):
        nw = int(args[3])
        print("Using %d workers" % nw)

    pixels = Image.new("HSV", (Width, Height))
    image = ImageDraw.Draw(pixels, "HSV")

    t0 = time.time()

    with ProcessPoolExecutor(max_workers=nw) as doer:
        for row_index in range(int(Width/nw)):
            progress = nw*row_index / Width * 100
            #if (progress % 5 == 0):
            print(f"Progress: {progress}%")

            # Prepare rows for workers
            arr = [0] * nw
#            print("Array: ",arr)
            for sub in range(nw):
                arr[sub] = row_index*nw + sub

#            print("Array: ",arr)
            result = doer.map(mandelbrot_wrapper, arr)

            sub = 0
            for r in result:
#                print("r :", sub, ", ", r)
                for col_index in range(Height):
                    hsv_tuple = calc_color(r[col_index], Max_iter)
                    image.point((row_index*nw + sub, col_index), fill=hsv_tuple)
                sub += 1

    t1 = time.time()
        
    print(f"Code executed in {t1 - t0} s")
    if pixels.mode != 'RGB':
        pixels = pixels.convert('RGB')


    pixels.save("BT-%d-%d-%d.jpg" % (Width, Height, nw))
    return True

#Skalar ett värde från ett intervall till ett annat
def scale(value, old_min, old_max, new_min, new_max):
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((value - old_min) * new_range) / old_range) + new_min
    return new_value

#Kollar om punkten (x, y) finns i mandelbrotmängden
#Om punktens absolutvärde går över två ger den tillbaka antalet iterationer det tog
def mandelbrot(x, y, max_iter, Julia_mode=True, a=-0.12, b=-0.77): 

    if (Julia_mode):
        z = complex(x, y)
        c = complex(a, b)
    else:
        c = complex(x, y) # a + bj
        z = 0
    
    for i in range(max_iter):
        z = z**2 + c
        if (abs(z) > 2):
            return i

    return max_iter

def mandelbrot_wrapper(x): 
    res = [0] * Height
    scaled_x_val = scale(x, 0, Width, -2, 2)
    for col_index in range(Height):
        scaled_y_val = scale(col_index, 0, Height, -2, 2)
        res[col_index] = mandelbrot(scaled_x_val, scaled_y_val, Max_iter)
    return res
        

#Färglägger en pixel svart om den nått max_iter
#och absolutvärdet av z inte gått över två
def calc_color(iter, Max_iter):

    #här är c antalet iterationer som en procent
    #av max_iter i decimalform
    c = scale(iter, 0, Max_iter, 0, 1)
    if (c == 1):
        return 0
    else:
        hue = round((359 * c))
        value = round(255 * c * 25)
        hsv_tuple = (hue, 255, value)

        return hsv_tuple

def check_global():
    print("check_global: Width/Height/Max_iter=", Width, Height, Max_iter)

if __name__ == '__main__':

    if (len(sys.argv) < 4):
        print("Usage: ", sys.argv[0], "<Width>", "<Height>", "<MaxIter>")
    else:
        main(sys.argv[1:])

        check_global()
"""

from concurrent.futures import ProcessPoolExecutor
from time import sleep
  
values = [3,4,5,6]
def cube(x):
    print(f'Cube of {x}:{x*x*x}')
  
  
if __name__ == '__main__':
    result =[]
    with ProcessPoolExecutor(max_workers=5) as exe:
        exe.submit(cube, args=[2,3,4,56])
        exe.join()
          
        # Maps the method 'cube' with a iterable
        for i range(len(above_lst)):
            iterations = exe.map(get_iterations,lst)
            iter_lst.append(iterations)
      
    for r in result:
      print(r)

above_lst = [[ iter ],[ (x,y) ],[ (x,y) ]]     [ (x,y) ] = lst
            [[],[],[]]

def get_iterations(lst):
    for i in range(len(lst))
        iterations = mandelbrot(lst[i][0], lst[i][1], Max_iter)
        lst[i] = 
    



"""