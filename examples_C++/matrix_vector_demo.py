import matrix_engine

A = matrix_engine.Matrix([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 9]])

for i in range(3):
    A[i, i] = 2

v = matrix_engine.Vector([1, 2, 3])

v[0] = 1
v[1] = 2
v[2] = 3

result = A.matvec(v)

print(result)