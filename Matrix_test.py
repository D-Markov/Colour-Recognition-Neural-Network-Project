import unittest
import unittest.mock as mock
from Matrix import Matrix
from random import random
import math 

class MatrixTest(unittest.TestCase):

    def test_ctor_4x1(self):
        m = Matrix([[1,2,3,4]])

        self.assertEqual(m.rows, 1)
        self.assertEqual(m.colomns, 4)

    def test_matrix_mathematical_operations_square(self):
         multiplication = Matrix([[1, 0], [0, 1]])
         matrixO = Matrix([[1, 2], [3, 4]]) 
         multiplication.multiply(matrixO)
         self.assertSequenceEqual([[1, 2], [3, 4]], multiplication)
         self.assertEqual(multiplication.rows, 2)
         self.assertEqual(multiplication.colomns, 2)

    def test_matrix_mathematical_operations_2x3_3x2(self):
         multiplication = Matrix([[1, 0, 1], [0, 1, 0]])
         matrixO = Matrix([[1, 2], [3, 4], [5, 6]]) 
         multiplication.multiply(matrixO)
         self.assertSequenceEqual([[6, 8], [3, 4]], multiplication)
         self.assertEqual(multiplication.rows, 2)
         self.assertEqual(multiplication.colomns, 2)

    def test_matrix_mathematical_operations_3x2_2x3(self):
         multiplication = Matrix([[1, 2], [3, 4], [5, 6]])
         matrixO = Matrix([[1, 0, 1], [0, 1, 0]]) 
         multiplication.multiply(matrixO)
         self.assertSequenceEqual([[1, 2, 1], [3, 4, 3], [5, 6, 5]], multiplication)
         self.assertEqual(multiplication.rows, 3)
         self.assertEqual(multiplication.colomns, 3)

    def test_matrix_mathematical_operations_1x1_1x1(self):
         multiplication = Matrix([[2]])
         matrixO = Matrix([[3]]) 
         multiplication.multiply(matrixO)
         self.assertSequenceEqual([[6]], multiplication)
         self.assertEqual(multiplication.rows, 1)
         self.assertEqual(multiplication.colomns, 1)
    
    def test_scalar_multiplication(self):
        multiplier = 11
        matrixS = Matrix([[1, 2], [10, 11]])
        matrixS.multiply_scalar(multiplier)

        self.assertSequenceEqual(matrixS, [[11, 22], [110, 121]])

    def test_multiplication_exception_raised_on_invalid_matrix_dimensions_1(self):
         self.assertRaises(ValueError, Matrix([[1, 0], [0, 1]]).multiply, Matrix([[1, 2]]))

    def test_multiplication_exception_raised_on_invalid_matrix_dimensions_2(self):
        self.assertRaises(ValueError, Matrix([[1, 2]]).multiply, Matrix([[1, 0], [0, 1]]))

    def test_random_matrix(self):
        with mock.patch("random.random", return_value = 1):
            randMatrix = Matrix.randomMatrix(2, 4)
            self.assertSequenceEqual([[1 for c in range(4)], [1 for c in range(4)]], randMatrix)

    def test_zero_matrix(self):
        zerMatrix = Matrix.zeroMatrix(2, 4)
        self.assertSequenceEqual([[0, 0, 0, 0],[0, 0, 0, 0]] , zerMatrix) 

    def test_add_matrix(self):
        matrixA = Matrix([[0, 1], [0, 1], [0, 1]])
        matrixA.add(Matrix([[0, 0], [0, 0], [0, 0]]))
        self.assertSequenceEqual([[0, 1], [0, 1], [0, 1]], matrixA)

    
    def test_dot(self):
        matrixP = Matrix([[1, 4], [9, 16]])
        dotVal = matrixP.dot(Matrix([[1, 4], [9, 16]]))
        self.assertEqual(354, dotVal)

    def test_rtocol_2x2(self):
        matrixT = Matrix([[1, 4], [5, 6]])
        matrixT.rtocol()
        self.assertSequenceEqual([[1, 5], [4, 6]], matrixT)
        self.assertEqual(matrixT.rows, 2)
        self.assertEqual(matrixT.colomns, 2)

    def test_rtocol_2x4(self):
        matrixT = Matrix([[2, 5, 2, 9], [1, 2, 4, 6]])
        matrixT.rtocol()
        self.assertSequenceEqual([[2, 1], [5, 2], [2, 4], [9, 6]], matrixT)
        self.assertEqual(matrixT.rows, 4)
        self.assertEqual(matrixT.colomns, 2)
    
    def test_apply(self):
        m = Matrix([[0, 0], [0, 0]])
        m.apply(lambda x: 1/(1 + math.exp(-x)))
        self.assertSequenceEqual([[0.5, 0.5], [0.5, 0.5]], m)


    # def test_add_matrix(self):
    #     addMatrix = [[9, 6], [0, 0]]
    #     matrix = 
    #     self.assertListEqual(addMatrix, 

if __name__ == '__main__':
    unittest.main()