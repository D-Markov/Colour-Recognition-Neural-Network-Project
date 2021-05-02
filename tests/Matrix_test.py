# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false
import unittest
import unittest.mock as mock
from parameterized import parameterized
from src.Mathematics.Matrix import Matrix
import math 
from MatrixTestCase import MatrixTestCase

class MatrixTest(MatrixTestCase):

    def test_ctor_4x1(self):
        m = Matrix([[1,2,3,4]])

        self.assertEqual(m.rows, 1)
        self.assertEqual(m.colomns, 4)


    @parameterized.expand([
        ("1x2 2x1", Matrix([[1, 4]]), Matrix([[1], [1]]), Matrix([[1.0, 4.0], [1.0, 4.0]])),
        ("1x2 2x2", Matrix([[1, 1]]), Matrix([[1, 4], [1, 6]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x1 1x2", Matrix([[1], [1]]), Matrix([[1, 4]]), Matrix([[1.0, 4.0], [1.0, 4.0]])),
        ("2x1 2x2", Matrix([[1], [1]]), Matrix([[1, 4], [1, 6]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 2x2", Matrix([[1, 1], [1, 1]]), Matrix([[1, 4], [1, 6]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 2x1", Matrix([[1, 4], [1, 6]]), Matrix([[1], [1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 1x2", Matrix([[1, 4], [1, 6]]), Matrix([[1, 1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 2x2", Matrix([[1, 4], [1, 6]]), Matrix([[1, 1], [1, 1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 int", Matrix([[1, 4], [1, 6]]), 1, Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 float", Matrix([[1, 4], [1, 6]]), 1.0, Matrix([[1.0, 4.0], [1.0, 6.0]]))
    ])
    def test_multiplication(self, name:str, left: Matrix, right: Matrix, result: Matrix):
        self.assertMatrixAreEqual(left.multiply(right), result)


    @parameterized.expand([
        ("2x1 2x2", Matrix([[168], [168]]), Matrix([[1, 4], [1, 6]]), Matrix([[168.0, 42.0], [168.0, 28.0]])),
        ("1x2 2x2", Matrix([[168, 168]]), Matrix([[1, 4], [1, 6]]), Matrix([[168.0, 42.0], [168.0, 28.0]])),
        ("2x2 2x1", Matrix([[1, 4], [1, 6]]), Matrix([[1], [1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 1x2", Matrix([[1, 4], [1, 6]]), Matrix([[1, 1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 2x2", Matrix([[1, 4], [1, 6]]), Matrix([[1, 1], [1, 1]]), Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 int", Matrix([[1, 4], [1, 6]]), 1, Matrix([[1.0, 4.0], [1.0, 6.0]])),
        ("2x2 float", Matrix([[1, 4], [1, 6]]), 1.0, Matrix([[1.0, 4.0], [1.0, 6.0]]))
    ])
    def test_division_operator(self, name: str, left: Matrix, right: Matrix, result: Matrix):
        self.assertMatrixAreEqual(left.divide(right), result)

   
    def test_random_matrix(self):
        with mock.patch("random.gauss", return_value = 1):
            randMatrix = Matrix.randomMatrix(2, 4)
            self.assertSequenceEqual([[1 for _ in range(4)], [1 for _ in range(4)]], randMatrix)

    def test_zero_matrix(self):
        zerMatrix = Matrix.zeroMatrix(2, 4)
        self.assertSequenceEqual([[0, 0, 0, 0],[0, 0, 0, 0]] , zerMatrix) 

    @parameterized.expand([
        ("3x2 3x2", Matrix([[0, 1], [0, 1], [0, 1]]), Matrix([[0, 0], [0, 0], [0, 0]]), [[0, 1], [0, 1], [0, 1]]),
        ("int 3x2", 1, Matrix([[0, 1], [0, 1], [0, 1]]), [[1, 2], [1, 2], [1, 2]]),
        ("3x2 int", Matrix([[0, 1], [0, 1], [0, 1]]), 1, [[1, 2], [1, 2], [1, 2]]),
        ("float 3x2", 1.0, Matrix([[0, 1], [0, 1], [0, 1]]), [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]]),
        ("3x2 float", Matrix([[0, 1], [0, 1], [0, 1]]), 1.0, [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]]),
        ("3x2 3x1", Matrix([[0, 1], [0, 1], [0, 1]]), Matrix([[1],[1],[1]]), [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]])
    ])
    def test_add_operation(self, name: str, left: Matrix, right: Matrix, result: Matrix):
        self.assertSequenceEqual(result, left + right)

    @parameterized.expand([
        ("1x2 2x2", Matrix([[1, 1]]), Matrix([[1, 1], [1, 1]]), [[0, 0], [0, 0]]),
        ("2x2 1x2", Matrix([[1, 1], [1, 1]]), Matrix([[1, 1]]), [[0, 0], [0, 0]]),
        ("2x1 2x2", Matrix([[1], [1]]), Matrix([[1, 1], [1, 1]]), [[0, 0], [0, 0]]),
        ("2x2 2x1", Matrix([[1, 1], [1, 1]]), Matrix([[1], [1]]), [[0, 0], [0, 0]]),
        ("3x2 3x2", Matrix([[0, 1], [0, 1], [0, 1]]), Matrix([[0, 0], [0, 0], [0, 0]]), [[0, 1], [0, 1], [0, 1]]),
        ("int 3x2", 1, Matrix([[0, 1], [0, 1], [0, 1]]), [[1, 0], [1, 0], [1, 0]]),
        ("3x2 int", Matrix([[1, 1], [1, 1], [1, 1]]), 1, [[0, 0], [0, 0], [0, 0]]),
        ("float 3x2", 1.0, Matrix([[1, 1], [1, 1], [1, 1]]), [[0, 0], [0, 0], [0, 0]]),
        ("3x2 float", Matrix([[1, 1], [1, 1], [1, 1]]), 1.0, [[0, 0], [0, 0],[0, 0]])
    ])
    def test_subtract_operator(self, name: str, left: Matrix, right: Matrix, result: Matrix):
        self.assertSequenceEqual(result, left - right)

    @parameterized.expand([
        ("4x4", Matrix([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]), Matrix([[4], [4], [4], [4]])),
        ("1x7", Matrix([[0.775112467947669, 0.6748015958065318, -0.35519107689330787, -0.18816103652461777, -0.05088776646897432, 0.43913101827589524, 0.4346996995492459]]), Matrix([[1.729504902]]))
        ])
    def test_rowsSum(self, name: str, matrix: Matrix, result: Matrix):
        self.assertMatrixAreEqual(result, matrix.rowsSum())

    @parameterized.expand([
        ("2x2 2x2", Matrix([[1, 1], [1, 1]]), Matrix([[9, 9], [9, 9]]), Matrix([[18, 18], [18, 18]])),
        ("1x2 2x1", Matrix([[1, 1]]), Matrix([[9], [9]]), Matrix([[18]])),
        ("2x1 1x2", Matrix([[1], [1]]), Matrix([[9, 9]]), Matrix([[9, 9],[9, 9]]))
        ])
    def test_dot(self, name: str, left: Matrix, right: Matrix, result: Matrix):
        self.assertMatrixAreEqual(left.dot(right), result)
        
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

    def test_getitem_checks_bounds(self):
        matrix = Matrix([[0], [1]])
        self.assertRaises(IndexError, lambda: matrix[-2])
        self.assertRaises(IndexError, lambda: matrix[2])

if __name__ == '__main__':
    unittest.main()