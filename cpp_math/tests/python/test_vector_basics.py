import unittest

import matrix_engine as me


class VectorBasicsTests(unittest.TestCase):
    def test_arithmetic_and_dot(self):
        a = me.Vector([1.0, 2.0, 3.0])
        b = me.Vector([4.0, 5.0, 6.0])

        self.assertEqual(list(a + b), [5.0, 7.0, 9.0])
        self.assertEqual(list(b - a), [3.0, 3.0, 3.0])
        self.assertEqual(list(a * b), [4.0, 10.0, 18.0])
        self.assertEqual(list(b / a), [4.0, 2.5, 2.0])
        self.assertEqual(list(a * 2.0), [2.0, 4.0, 6.0])
        self.assertEqual(list(2.0 * a), [2.0, 4.0, 6.0])
        self.assertEqual(a @ b, 32.0)

    def test_iteration_contains_and_indexing(self):
        vector = me.Vector([1.0, 2.0, 3.0])
        vector[0] = 10.0

        self.assertEqual(vector[0], 10.0)
        self.assertEqual(list(vector), [10.0, 2.0, 3.0])
        self.assertIn(2.0, vector)
        self.assertNotIn(4.0, vector)

    def test_vector_methods(self):
        a = me.Vector([1.0, 2.0, 3.0])
        b = me.Vector([4.0, 5.0, 6.0])

        self.assertAlmostEqual(a.magnitude(), 14.0 ** 0.5)
        self.assertEqual(list(a.cross(b)), [-3.0, 6.0, -3.0])


if __name__ == "__main__":
    unittest.main()
