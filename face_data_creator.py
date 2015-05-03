from PIL import Image
import os

width_offset = 75
height_offset = 25

width = 100
height = 80

out_file = open("images.txt", "w")
num_doubles = 0

for path, dirnames, filenames in os.walk('cohn-kanade'):
  num_to_add = 2 if num_doubles < 25 else 1
  if len(filenames) > 5:
    num_doubles += 1
  for filename in filenames:
      if filename == ".DS_Store" or num_to_add <= 0:
        continue
      image_path = os.path.join(path, filename)
      image = Image.open(image_path)
      data = image.getdata()
      row = [x[0] for x in list(data)]
      out_file.write(" ".join(str(x) for x in row)+"\n")
      num_to_add -= 1

