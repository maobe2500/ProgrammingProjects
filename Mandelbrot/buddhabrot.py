from PIL import Image, ImageDraw
from decimal import Decimal
import time
Width = 4000
Height = 4000
Max_iter = 500

"""
For a Buddhabrot, the value of c is less important. 
Instead, the frequency with which the orbiting point z visits 
various pixels is recorded — lighter pixels have received a higher 
frequency of visits from z. While values of c are chosen at random, 
the classic Buddhabrot uses only those values of c which will 
cause z to escape to infinity (non Mandelbrot-set points). 

"""

#Skalar ett värde från ett intervall till ett annat
def scale(value, old_min, old_max, new_min, new_max):
    old_range = Decimal(old_max - old_min)
    new_range = Decimal(Decimal(new_max) - new_min)
    new_value = (((value - old_min) * new_range) / old_range) + new_min
    return new_value

#Kollar om punkten (x, y) finns i mandelbrotmängden
#Om punktens absolutvärde går över två ger den tillbaka antalet iterationer det tog
def mandelbrot(x, y, max_iter, Julia_mode=False, a=-0.75, b=0.1): 

    if (Julia_mode):
        z = complex(x, y)
        c = complex(a, b)
    else:
        c = complex(x, y)
        z = 0
    
    for i in range(max_iter):
        z = z**2 + c
        if (abs(z) > 2):
            return i

    return max_iter


def randomize_c() {}

#Färglägger en pixel svart om den nått max_iter
#och absolutvärdet av z inte gått över två
def calc_color(iter):

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

pixels = Image.new("HSV", (Width, Height))
image = ImageDraw.Draw(pixels, "HSV")


t0 = time.time()

for row_index in range(Width):
    print(f"Progress: {row_index / Width * 100}%")
    for col_index in range(Height):

        scaled_x_val = scale(row_index, 0, Width, -0.76, -0.74)
        scaled_y_val = scale(col_index, 0, Height, 0.98, 0.11)
        iter = mandelbrot(scaled_x_val, scaled_y_val, Max_iter)
        hsv_tuple = calc_color(iter)
        image.point((row_index, col_index), fill=hsv_tuple)

t1 = time.time()
    
print(f"Code executed in {t1 - t0} s")
if pixels.mode != 'RGB':
    pixels = pixels.convert('RGB')


pixels.save("Fractal16.1.jpg")