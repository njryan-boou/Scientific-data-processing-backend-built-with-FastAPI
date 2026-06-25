import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "cpp_math"))

import matrix_engine as me

CppMatrix = me.Matrix
CppVector = me.Vector

A = CppVector([1.0, 2.0, 3.0])
B = CppVector([4.0, 5.0, 6.0])
M = CppMatrix([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

try:
    M.determinant()
except me.ShapeError as exc:
    print(f"caught ShapeError: {exc}")

print("\nelementwise logical examples")

print(A == B)
print(A < B)
print((A < B) & (B > A))
print((A == B) | (A < B))
print(~(A == B))

N = CppMatrix([[1.0, 0.0, 3.0], [0.0, 5.0, 7.0]])
print(M == N)
print(M < N)
print(M & N)
print(~M)
print([] == [])
