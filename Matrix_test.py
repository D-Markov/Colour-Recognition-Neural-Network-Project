import unittest
import unittest.mock as mock
from parameterized import parameterized
from Matrix import Matrix
from random import random
import math 
from test_utils import assertMatrixAreEqual

class MatrixTest(unittest.TestCase):

    def test_ctor_4x1(self):
        m = Matrix([[1,2,3,4]])

        self.assertEqual(m.rows, 1)
        self.assertEqual(m.colomns, 4)


    @parameterized.expand([
        (Matrix([[1], [1]]), Matrix([[1, 4], [1, 6]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 1]]), Matrix([[1, 4], [1, 6]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), Matrix([[1], [1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), Matrix([[1, 1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), Matrix([[1, 1], [1, 1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), 1, Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), 1.0, Matrix([[1.0, 4.0], [1.0, 6.0]]))
    ])
    def test_multiplication(self, left, right, result):
        assertMatrixAreEqual(left.multiply(right), result)


    @parameterized.expand([
        (Matrix([[168], [168]]), Matrix([[1, 4], [1, 6]]), Matrix([[168.0, 42.0], [168.0, 28.0]])),
        (Matrix([[168, 168]]), Matrix([[1, 4], [1, 6]]), Matrix([[168.0, 42.0], [168.0, 28.0]])),
        (Matrix([[1, 4], [1, 6]]), Matrix([[1], [1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), Matrix([[1, 1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), Matrix([[1, 1], [1, 1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), 1, Matrix([[1.0, 4.0], [1.0, 6.0]])),
        (Matrix([[1, 4], [1, 6]]), 1.0, Matrix([[1.0, 4.0], [1.0, 6.0]]))
    ])
    def test_division_operator(self, left, right, result):
        assertMatrixAreEqual(left.divide(right), result)

   
    def test_random_matrix(self):
        with mock.patch("random.random", return_value = 1):
            randMatrix = Matrix.randomMatrix(2, 4)
            self.assertSequenceEqual([[1 for c in range(4)], [1 for c in range(4)]], randMatrix)

    def test_zero_matrix(self):
        zerMatrix = Matrix.zeroMatrix(2, 4)
        self.assertSequenceEqual([[0, 0, 0, 0],[0, 0, 0, 0]] , zerMatrix) 

    @parameterized.expand([
        (Matrix([[0, 1], [0, 1], [0, 1]]), Matrix([[0, 0], [0, 0], [0, 0]]), [[0, 1], [0, 1], [0, 1]]),
        (1, Matrix([[0, 1], [0, 1], [0, 1]]), [[1, 2], [1, 2], [1, 2]]),
        (Matrix([[0, 1], [0, 1], [0, 1]]), 1, [[1, 2], [1, 2], [1, 2]]),
        (1.0, Matrix([[0, 1], [0, 1], [0, 1]]), [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]]),
        (Matrix([[0, 1], [0, 1], [0, 1]]), 1.0, [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]])
    ])
    def test_add_operation(self, left, right, result):
        self.assertSequenceEqual(result, left + right)

    @parameterized.expand([
    (Matrix([[0, 1], [0, 1], [0, 1]]), Matrix([[0, 0], [0, 0], [0, 0]]), [[0, 1], [0, 1], [0, 1]]),
    (1, Matrix([[0, 1], [0, 1], [0, 1]]), [[1, 0], [1, 0], [1, 0]]),
    (Matrix([[1, 1], [1, 1], [1, 1]]), 1, [[0, 0], [0, 0], [0, 0]]),
    (1.0, Matrix([[1, 1], [1, 1], [1, 1]]), [[0, 0], [0, 0], [0, 0]]),
    (Matrix([[1, 1], [1, 1], [1, 1]]), 1.0, [[0, 0], [0, 0],[0, 0]])
    ])
    def test_subtract_operator(self, left, right, result):
        self.assertSequenceEqual(result, left - right)

    def test_dot(self):
        matrixP = Matrix([[1, 4], [9, 16]])
        dotVal = matrixP.dot(Matrix([[1, 4], [9, 16]]))
        self.assertEqual(354, dotVal)

    def test_rtocol_2x2(self):
        data = [[1, 4], [5, 6]]
        matrixT = Matrix(data)
        m = matrixT.rtocol()

        self.assertSequenceEqual(matrixT, data)
        self.assertEqual(matrixT.rows, 2)
        self.assertEqual(matrixT.colomns, 2)
        
        self.assertSequenceEqual(m, [[1, 5], [4, 6]])
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.colomns, 2)

    def test_rtocol_2x4(self):
        data = [[2, 5, 2, 9], [1, 2, 4, 6]]
        matrixT = Matrix(data)
        m = matrixT.rtocol()

        self.assertSequenceEqual(matrixT, data)
        self.assertEqual(matrixT.rows, 2)
        self.assertEqual(matrixT.colomns, 4)

        self.assertSequenceEqual([[2, 1], [5, 2], [2, 4], [9, 6]], m)
        self.assertEqual(m.rows, 4)
        self.assertEqual(m.colomns, 2)
    
    def test_apply(self):
        matrix = Matrix([[0, 0], [0, 0]])
        m = matrix.apply(lambda x: 1/(1 + math.exp(-x)))
        self.assertSequenceEqual([[0.5, 0.5], [0.5, 0.5]], m)
        
    # def test_add_matrix(self):
    #     addMatrix = [[9, 6], [0, 0]]
    #     matrix = 
    #     self.assertListEqual(addMatrix, 

if __name__ == '__main__':
    unittest.main()