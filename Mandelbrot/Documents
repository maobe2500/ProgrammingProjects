from PIL import Image, ImageDraw
import time
Width = 5000
Height = 5000
Max_iter = 500


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
        c = complex(x, y)
        z = 0
    
    for i in range(max_iter):
        z = z**2 + c
        if (abs(z) > 2):
            return i

    return max_iter


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

        scaled_x_val = scale(row_index, 0, Width, -2, 2)
        scaled_y_val = scale(col_index, 0, Height, -2, 2)
        iter = mandelbrot(scaled_x_val, scaled_y_val, Max_iter)
        hsv_tuple = calc_color(iter)
        image.point((row_index, col_index), fill=hsv_tuple)

t1 = time.time()
    
print(f"Code executed in {t1 - t0} s")
if pixels.mode != 'RGB':
    pixels = pixels.convert('RGB')


pixels.save(f"Fractal{time.time()}.jpg")