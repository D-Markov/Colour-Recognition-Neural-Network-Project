import unittest
import unittest.mock as mock
from Matrix import Matrix
from random import random

class MatrixTest(unittest.TestCase):

    # def test_matrix_mathematical_operations(self):
    #     multiplication = [[1, 2], [3, 4]]
    #     matrixR = Matrix.multiply([[1, 0], [0, 1]], [[1, 2], [3, 4]])
    #     self.assertListEqual(matrixR, multiplication)

    # def test_multiplication_exception_raised_on_invalid_matrix_dimensions_1(self):
    #     self.assertRaises(ValueError, Matrix.multiply, [[1, 0], [0, 1]], [[1, 2]])

    # def test_multiplication_exception_raised_on_invalid_matrix_dimensions_2(self):
    #     self.assertRaises(ValueError, Matrix.multiply, [[1, 2]], [[1, 0], [0, 1]])

    def test_random_matrix(self):
        with mock.patch("random.random", return_value = 1):
            randMatrix = Matrix.randomMatrix(2, 4)
            self.assertSequenceEqual([[1 for c in range(4)], [1 for c in range(4)]], randMatrix)

    def test_zero_matrix(self):
        zerMatrix = Matrix.zeroMatrix(2, 4)
        self.assertSequenceEqual([[0, 0, 0, 0],[0, 0, 0, 0]] , zerMatrix)

    # def test_add_matrix(self):
    #     addMatrix = [[9, 6], [0, 0]]
    #     matrix = 
    #     self.assertListEqual(addMatrix, 

if __name__ == '__main__':
    unittest.main()