import unittest

import matrix_engine as me


class VectorLogicTests(unittest.TestCase):
    def test_comparison_masks(self):
        a = me.Vector([0.0, 2.0, 3.0])
        b = me.Vector([1.0, 2.0, 4.0])

        self.assertEqual(list(a == b), [0.0, 1.0, 0.0])
        self.assertEqual(list(a != b), [1.0, 0.0, 1.0])
        self.assertEqual(list(a < b), [1.0, 0.0, 1.0])
        self.assertEqual(list(a <= b), [1.0, 1.0, 1.0])
        self.assertEqual(list(b > a), [1.0, 0.0, 1.0])
        self.assertEqual(list(b >= a), [1.0, 1.0, 1.0])

    def test_logical_masks(self):
        a = me.Vector([0.0, 2.0, 3.0])
        b = me.Vector([1.0, 2.0, 4.0])

        self.assertEqual(list(a & b), [0.0, 1.0, 1.0])
        self.assertEqual(list(a | b), [1.0, 1.0, 1.0])
        self.assertEqual(list(a ^ b), [1.0, 0.0, 0.0])
        self.assertEqual(list(~a), [1.0, 0.0, 0.0])


if __name__ == "__main__":
    unittest.main()
