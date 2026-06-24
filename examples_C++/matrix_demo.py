import matrix_engine as matrix_engine

A = matrix_engine.Matrix(2, 2)

A[0, 0] = 1
A[0, 1] = 2
A[1, 0] = 3
A[1, 1] = 4

print("A:")
print(A)

print("transpose:")
print(A.transpose())

print("determinant:")
print(A.determinant())

print("inverse:")
print(A.inverse())