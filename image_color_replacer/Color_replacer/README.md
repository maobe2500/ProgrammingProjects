# Color_replacer
A image color replacer thant takes in an image and switches the rgb colors based on various settings and the writes these changes to a copy of the image.

Usage: 

    ./image_color_replacer.py [filename] [color-to-replace] [color-to-replace-with] [highliting-code]
    
    The options for color are r, g and b.
    
    The options for highliting are:
      
      t - true. Increases the color value of the color being changed to realtive to the other colors.
      ts - true, soft. Increases the color being changed to but half the reltive ammout.
      td - true, double. Increases the color being changed to but doubles the reltive ammont.
      f - false. Switches the colors without increasing the relative ammont.

Examples:

    If we want to switch all the blue in an image with an equal red ammunt we write:
    
        ./image_color_replacer.py img.jpg b r f
    
    If we want to switch all the green in an image with a slightly increased blue ammunt we write:
    
        ./image_color_replacer.py img.jpg g b ts
