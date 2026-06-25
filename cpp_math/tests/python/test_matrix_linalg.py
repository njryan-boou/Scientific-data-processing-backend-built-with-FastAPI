import unittest

import matrix_engine as me


class MatrixLinalgTests(unittest.TestCase):
    def test_matmul_matvec_and_vecmat(self):
        a = me.Matrix([[1.0, 2.0], [3.0, 4.0]])
        b = me.Matrix([[5.0, 6.0], [7.0, 8.0]])
        v = me.Vector([2.0, 3.0])

        self.assertEqual(str(a @ b), "[ 19 22 ]\n[ 43 50 ]\n")
        self.assertEqual(list(a @ v), [8.0, 18.0])
        self.assertEqual(list(v @ a), [11.0, 16.0])

    def test_transpose_and_determinant(self):
        a = me.Matrix([[1.0, 2.0], [3.0, 4.0]])
        b = me.Matrix([[6.0, 1.0, 1.0], [4.0, -2.0, 5.0], [2.0, 8.0, 7.0]])

        self.assertEqual(str(a.transpose()), "[ 1 3 ]\n[ 2 4 ]\n")
        self.assertEqual(a.determinant(), -2.0)
        self.assertEqual(b.determinant(), -306.0)


if __name__ == "__main__":
    unittest.main()
