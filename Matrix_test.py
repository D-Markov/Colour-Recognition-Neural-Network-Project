import unittest
import Matrix

class MatrixTest(unittest.TestCase):

    def test_matrix_mathematical_operations(self):
        multiplication = [[1, 2], [3, 4]]
        matrixR = Matrix.Multiply([[1, 0], [0, 1]], [[1, 2], [3, 4]])
        self.assertListEqual(matrixR, multiplication)

    def test_multiplication_exception_raised_on_invalid_matrix_dimensions_1(self):
        self.assertRaises(ValueError, Matrix.Multiply, [[1, 0], [0, 1]], [[1, 2]])

    def test_multiplication_exception_raised_on_invalid_matrix_dimensions_2(self):
        self.assertRaises(ValueError, Matrix.Multiply, [[1, 2]], [[1, 0], [0, 1]])

if __name__ == '__main__':
    unittest.main()