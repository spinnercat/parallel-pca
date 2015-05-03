from PIL import Image
import os

width_offset = 75
height_offset = 25

width = 500
height = 400


for path, dirnames, filenames in os.walk('cohn-kanade'):
  for filename in filenames:
      if filename == ".DS_Store":
        continue
      image_path = os.path.join(path, filename)
      image = Image.open(image_path)
      image = image.resize((100, 80), Image.ANTIALIAS)
      image.save(image_path)

