"""
    Script for cropping and resizing images for goblin nft website cards.
    Author: Joywalker
    Date: 14.04.2022
"""
import os
import glob
from PIL import Image

imgs = glob.glob('/Volumes/Macintosh HD/GoblinsNFT/shit/*.png')
new_path = "good"

# Setting the points for cropped image
left = 796 * 2.306396484375
top = 0
right = 9447 - (150 * 2.306396484375)
bottom = 7087

scale = 1.1953125
height = 765
width = int(height / scale)
# Cropped image of above dimension
# (It will not change original image)

for img in imgs:
    img_name = img.split(os.sep)[-1]
    image = Image.open(img)
    image = image.crop((left, top, right, bottom))

    image = image.resize((width, height))

    paath = os.path.join(new_path, img_name)
    image.save(paath, quality=100, subsampling=0)
