import matrix_engine

v1 = matrix_engine.Vector(3)
v2 = matrix_engine.Vector(3)

v1[0] = 1
v1[1] = 2
v1[2] = 3

v2[0] = 4
v2[1] = 5
v2[2] = 6

print("v1 =", v1)
print("v2 =", v2)

print("v1 + v2 =", v1 + v2)
print("v1 - v2 =", v1 - v2)
print("type(v1) =", type(v1))
print("len(v1) =", len(v1))

print("dot =", v1.dot(v2))
print("magnitude =", v1.magnitude())
print("normalized =", v1.normalize())
print(matrix_engine.__doc__)