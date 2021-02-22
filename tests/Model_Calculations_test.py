# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false
from parameterized import parameterized 
from src.Mathematics.Model_Calculations import sigmoid, sigmoid_prime, cost, error, error_prime
from src.Mathematics.Matrix import Matrix
from MatrixTestCase import MatrixTestCase

class TestModelCalculations(MatrixTestCase):
    @parameterized.expand([
        (-100, 3.72e-44),
        (0, 0.5),
        (100, 1.0)
    ])
    def test_sigmoid(self, value, result):
        self.assertAlmostEqual(result, sigmoid(value), 46)

    @parameterized.expand([
        (-100, 3.72e-44),
        (0, 0.25),
        (100, 0.0)
    ])
    def test_sigmoid_prime(self, value, result):
        self.assertAlmostEqual(result, sigmoid_prime(value), 46)


    @parameterized.expand([
        (Matrix([[0.1, 0.3, 0.5, 0.7]]), Matrix([[1.0, 2.0, 3.0, 4.0]]), Matrix([[2.3025850929940455, 2.05127066471314, 0.6931471805599452, -2.185218637222878]]))
    ])
    def test_error(self, y_hat, y, result):
        self.assertMatrixAreEqual(error(y_hat, y), result)
    
    @parameterized.expand([
        (Matrix([[0.1, 0.3, 0.5, 0.7]]), Matrix([[1.0, 2.0, 3.0, 4.0]]), 0.7154460752610632)
    ])
    def test_cost(self, y_hat, y, result):
        self.assertAlmostEqual(cost(y_hat, y), result, 15)


    @parameterized.expand([
        (Matrix([[0.1, 0.2, 0.3, 0.4]]), Matrix([[1.0, 2.0 , 3.0, 4.0]]), Matrix([[-10.0, -11.25, -12.857142857142858, -15.0]]))
    ])
    def test_error_prime(self, y_hat, y, result):
        self.assertMatrixAreEqual(error_prime(y_hat, y), result)
