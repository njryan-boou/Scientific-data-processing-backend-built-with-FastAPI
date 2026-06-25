import unittest

import matrix_engine as me


class ValidationApiTests(unittest.TestCase):
    def test_validation_helpers_accept_valid_inputs(self):
        matrix = me.Matrix([[1.0, 2.0], [3.0, 4.0]])

        me.validation.require(True, "should not fail")
        me.validation.square(matrix)
        me.validation.same_shape(matrix, matrix)
        me.validation.multiplication(matrix, matrix)
        me.validation.row(1, matrix.rows)
        me.validation.column(1, matrix.cols)
        me.validation.positive_dimension(matrix.rows, "rows")
        me.validation.reshape(4, matrix.rows * matrix.cols)

    def test_validation_helpers_raise_custom_errors(self):
        matrix = me.Matrix([[1.0, 2.0], [3.0, 4.0]])

        with self.assertRaises(me.ValueError):
            me.validation.require(False, "failed")

        with self.assertRaises(me.ShapeError):
            me.validation.square(me.Matrix([[1.0, 2.0, 3.0]]))

        with self.assertRaises(me.DimensionError):
            me.validation.multiplication(me.Matrix([[1.0, 2.0]]), me.Matrix([[1.0, 2.0]]))

        with self.assertRaises(me.IndexError):
            me.validation.row(2, matrix.rows)

    def test_methods_raise_custom_errors(self):
        with self.assertRaises(me.ShapeError):
            me.Matrix([[1.0, 2.0, 3.0]]).determinant()

        with self.assertRaises(me.DimensionError):
            me.Matrix([[1.0, 2.0]]) @ me.Matrix([[1.0, 2.0]])

        with self.assertRaises(me.IndexError):
            me.Matrix([[1.0]])[2, 0]

        with self.assertRaises(me.ValueError):
            me.Vector([1.0]) + me.Vector([1.0, 2.0])


if __name__ == "__main__":
    unittest.main()
