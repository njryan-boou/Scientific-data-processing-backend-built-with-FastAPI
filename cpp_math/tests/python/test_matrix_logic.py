import unittest

import matrix_engine as me


class MatrixLogicTests(unittest.TestCase):
    def test_comparison_masks(self):
        a = me.Matrix([[0.0, 2.0], [3.0, 4.0]])
        b = me.Matrix([[1.0, 2.0], [2.0, 5.0]])

        self.assertEqual(str(a == b), "[ 0 1 ]\n[ 0 0 ]\n")
        self.assertEqual(str(a != b), "[ 1 0 ]\n[ 1 1 ]\n")
        self.assertEqual(str(a < b), "[ 1 0 ]\n[ 0 1 ]\n")
        self.assertEqual(str(a <= b), "[ 1 1 ]\n[ 0 1 ]\n")
        self.assertEqual(str(a > b), "[ 0 0 ]\n[ 1 0 ]\n")
        self.assertEqual(str(a >= b), "[ 0 1 ]\n[ 1 0 ]\n")

    def test_logical_masks(self):
        a = me.Matrix([[0.0, 2.0], [3.0, 4.0]])
        b = me.Matrix([[1.0, 2.0], [2.0, 5.0]])

        self.assertEqual(str(a & b), "[ 0 1 ]\n[ 1 1 ]\n")
        self.assertEqual(str(a | b), "[ 1 1 ]\n[ 1 1 ]\n")
        self.assertEqual(str(a ^ b), "[ 1 0 ]\n[ 0 0 ]\n")
        self.assertEqual(str(~a), "[ 1 0 ]\n[ 0 0 ]\n")


if __name__ == "__main__":
    unittest.main()
