from typing import Callable
import math
from Matrix import Matrix

sigmoid = lambda x : 1/(1 + math.exp(-x))

sigmoid_prime = lambda x: sigmoid(x)*(1 - sigmoid(x))

l: Callable[[Matrix, Matrix], Matrix] = lambda y_hat, y : (y.multiply(y_hat.apply(math.log)) + (1 - y).multiply((1 - y_hat).apply(math.log))).multiply(-1)
c: Callable[[Matrix, Matrix], float] = lambda y_hat, y: l(y_hat, y).sum() / y.rows

dl: Callable[[Matrix, Matrix], float] = lambda y_hat, y: y.multiply(-1).divide(y_hat) +(1 - y).divide(1 - y_hat)
dc: Callable[[Matrix, Matrix], float] = lambda y_hat, y: dl(y_hat, y).divide(y.rows).sum()
