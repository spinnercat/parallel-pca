import numpy as np

def matrix_multiply(A, B):
  rows_A = len(A)
  cols_A = len(A[0])
  rows_B = len(B)
  cols_B = len(B[0])

  if cols_A != rows_B:
    raise Exception("Incorrect dimensions to mutiply")

  # Create the result matrix
  # Dimensions would be rows_A x cols_B
  C = [[0 for row in range(cols_B)] for col in range(rows_A)]

  print rows_A

  for i in xrange(rows_A):
    print i
    for k in xrange(cols_A):
      x = A[i][k]
      for j in xrange(cols_B):
        C[i][j] += x * B[k][j]
  return np.array(C)