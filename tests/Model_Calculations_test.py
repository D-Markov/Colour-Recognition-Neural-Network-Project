# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false
from parameterized import parameterized 
from src.Mathematics.Model_Calculations import sigmoid, sigmoid_prime, l, c, dl, dc
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
        (Matrix([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6], [0.7, 0.8]]), Matrix([[1.0], [2.0], [3.0], [4.0]]), Matrix([[2.30258509, 1.60943791], [2.05127066, 1.32175584], [0.69314718, -0.30010459],[-2.18521864, -3.93573953]]))
    ])
    def test_l(self, y_hat, y, result):
        self.assertMatrixAreEqual(l(y_hat, y), result)
    
    @parameterized.expand([
        (Matrix([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6], [0.7, 0.8]]), Matrix([[1.0], [2.0], [3.0], [4.0]]), 0.3892834822412179)
    ])
    def test_c(self, y_hat, y, result):
        self.assertAlmostEqual(c(y_hat, y), result, 15)


    @parameterized.expand([
        (Matrix([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6], [0.7, 0.8]]), Matrix([[1.0], [2.0], [3.0], [4.0]]), Matrix([[-10.0, -5.0], [-8.0952381, -6.66666667], [-10.0, -10.0], [-15.71428571, -20.0]]))
    ])
    def test_dl(self, y_hat, y, result):
        self.assertMatrixAreEqual(dl(y_hat, y), result)

    
    @parameterized.expand([
        (Matrix([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6], [0.7, 0.8]]), Matrix([[1.0], [2.0], [3.0], [4.0]]), (-21.36904761904762))
    ])
    def test_dc(self, y_hat, y, result):
        self.assertAlmostEqual(dc(y_hat, y), result, 14)