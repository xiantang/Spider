import glob
from PIL import Image
import os
image_path = glob.glob("imgs/*.jpg")
path_save = "new_imgs"

for file in image_path:
    print(file)
    name = os.path.join(file)
    try:
        im = Image.open(file).convert('RGB')
        im.thumbnail((800,800))
        im.save(name,"JPEG")
        
    except Exception as e:
        print(e)