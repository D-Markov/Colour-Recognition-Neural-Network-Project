from typing import Callable
import math
from .Matrix import Matrix, Scalar

sigmoid: Callable[[Scalar], Scalar] = lambda x : 1/(1 + math.exp(-x))
# sigmoid_prime: Callable[[Scalar], Scalar] = lambda x: sigmoid(x)*(1 - sigmoid(x))
def sigmoid_prime(x: Scalar) -> Scalar:
    a = sigmoid(x)
    return a * (1 - a)

relu: Callable[[Scalar], Scalar] = lambda x: max(0, x)

def relu_prime(x: Scalar) -> Scalar:
    return x if x > 0 else 0

def error(y_hat: Matrix, y: Matrix) -> Matrix:
    '''
        Logistic Regression cost function
    '''
    if y_hat.colomns != y.colomns:
        raise ValueError("yh and y must have one column each")
    if y_hat.rows != y.rows:
        raise ValueError("yh and y must have same number of rows")

    err = (y.multiply(y_hat.apply(math.log)) + (1 - y).multiply((1 - y_hat).apply(math.log))).multiply(-1)

    assert(err.rows == y.rows)
    assert(err.colomns == y.colomns)

    return err


def error_prime(y_hat: Matrix, y: Matrix) -> Matrix:

    if y_hat.colomns != y.colomns:
        raise ValueError("yh and y must have one column each")
    if y_hat.rows != y.rows:
        raise ValueError("yh and y must have same number of rows")

    derr = (y.divide(y_hat) - (1 - y).divide(1 - y_hat)).multiply(-1)

    assert(derr.rows == y.rows)
    assert(derr.colomns == y.colomns)

    return derr


# cost: Callable[[Matrix, Matrix], Scalar] = lambda y_hat, y: error(y_hat, y).sum() / y.colomns
def cost(y_hat: Matrix, y: Matrix) -> Scalar:
    return error(y_hat, y).sum() / y.colomns

activation_functions = {
    'sigmoid': sigmoid,
    'sigmoid_prime': sigmoid_prime,
    'relu': relu,
    'relu_prime': relu_prime
}
