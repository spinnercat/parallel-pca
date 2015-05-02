from PIL import Image
import os

width = 640
height = 425

for path, dirnames, filenames in os.walk('cohn-kanade'):
  for filename in filenames:
      if filename == ".DS_Store":
        continue
      image_path = os.path.join(path, filename)
      print image_path
      image = Image.open(image_path)
      image = image.crop((0,0, width, height))
      image.show()