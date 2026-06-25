import unittest

import matrix_engine as me


class MatrixBasicsTests(unittest.TestCase):
    def test_properties_indexing_and_arithmetic(self):
        a = me.Matrix([[1.0, 2.0], [3.0, 4.0]])
        b = me.Matrix([[5.0, 6.0], [7.0, 8.0]])

        self.assertEqual(a.shape, (2, 2))
        self.assertEqual(a.rows, 2)
        self.assertEqual(a.cols, 2)
        self.assertEqual(a[1, 0], 3.0)

        a[1, 0] = 9.0
        self.assertEqual(a[1, 0], 9.0)
        a[1, 0] = 3.0

        self.assertEqual(str(a + b), "[ 6 8 ]\n[ 10 12 ]\n")
        self.assertEqual(str(b - a), "[ 4 4 ]\n[ 4 4 ]\n")
        self.assertEqual(str(a * b), "[ 5 12 ]\n[ 21 32 ]\n")
        self.assertEqual(str(b / a), "[ 5 3 ]\n[ 2.33333 2 ]\n")

    def test_row_iteration(self):
        matrix = me.Matrix([[1.0, 2.0], [3.0, 4.0]])

        self.assertEqual([list(row) for row in matrix], [[1.0, 2.0], [3.0, 4.0]])


if __name__ == "__main__":
    unittest.main()
