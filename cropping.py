# -*- coding: utf-8 -*-
"""
croppin an image
"""

from PIL import Image

def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    cropped_image.show()


image_path = r"D:\Users\703143501\Documents\Genpact Internal\EY\screenshot.png"
image_obj = Image.open(image_path)

image_width, image_height = image_obj.size

print("The height and width of the image are {height} pixel and {width} pixel respectively".format(height = image_height, width = image_width))

# A tuple of x/y coordinates (x1, y1, x2, y2)
#crop_ratios = [0.575, 0.7, 0.75, 0.8]

coords = (int(image_width * 0.575),
          int(image_height * 0.7),
          int(image_width * 0.75),
          int(image_height * 0.77)
          )


save_path = r"D:\Users\703143501\Documents\Genpact Internal\EY\cropped.png"
#save_format = ".png"

cropped_image = image_obj.crop(coords)

## saving the image to disk
cropped_image.save(save_path)

## consider implementing this a a class
