import numpy as np
import pickle
import PIL.Image as Image

"""
make each row of vs and x have norm 1 and multiply
vs: m-by-n
xs: p-by-n
"""
def project(vs, xs):
    # for row in vs:
    #     row /= np.float(np.sqrt(sum(row**2)))

    return np.dot(vs, xs.T)

def calc_error(vs, xs):
    compressed = project(vs, xs)
    print compressed
    rec = np.dot(compressed.T, vs)
    print re

    print np.sqrt(np.sum((rec - xs)**2) / rec.size)

def reconstruct_images(vs, xs):
  width = 100
  height = 80
  compressed = project(vs, xs)
  rec = np.dot(compressed.T, vs)
  means_file = open('means.txt')
  means = []
  for mean_row in means_file:
    for x in mean_row.split():
      means.append(float(x))
  print len(means)
  for idx, row in enumerate(rec):
    image = []
    for i in range(0, len(row)):
      image.append((int(round(row[i] + means[i])), 255))
    im = Image.new("LA", (100,80))
    im.putdata(image)
    im.save("test_output/"+str(idx)+".png")

def save_eigenvectors(vs):
  means_file = open('means.txt')
  means = []
  for mean_row in means_file:
    for x in mean_row.split():
      means.append(float(x))
  print len(means)
  for idx, eigenvector in enumerate(vs):
    image = []
    minV = min(eigenvector)
    maxV = max(eigenvector)
    for i in range(0, len(eigenvector)):
      val = eigenvector[i]
      image.append((int(round((val-minV)*(255)/(maxV-minV))), 255))
    im = Image.new("LA", (100,80))
    im.putdata(image)
    im.save("eig_output/"+str(idx)+".png")


if __name__ == '__main__':
    vs = np.array([[2., 0., 0.], [0., 2., 0.]])
    xs = np.array([[2., 3., 1.], [4., 5., 6.], [-1., -3., 5.]])
    calc_error(vs, xs)

