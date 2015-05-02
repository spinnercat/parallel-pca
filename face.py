from PIL import Image
import os

width_offset = 75
height_offset = 25

width = 500
height = 400

for path, dirnames, filenames in os.walk('cohn-kanade'):
  for filename in filenames:
      if filename == ".DS_Store" or filename == "S014_002_02411100.png":
        continue
      image_path = os.path.join(path, filename)
      image = Image.open(image_path)
      image = image.crop((width_offset,height_offset, width + width_offset, height + height_offset))
      image = image.convert("LA")
      image.save(image_path)