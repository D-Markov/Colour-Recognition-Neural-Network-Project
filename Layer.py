from typing import Callable, Tuple
from Matrix import Matrix, Scalar

class Layer:
    def __init__(self, number_of_inputs: int, number_of_outputs: int,
      a: Callable[[Scalar], Scalar],
      a_prime: Callable[[Scalar], Scalar]):
        self.__a = a 
        self.__a_prime = a_prime
        self.__weights = Matrix.randomMatrix(number_of_outputs, number_of_inputs)
        self.__biases = Matrix.zeroMatrix(number_of_outputs, 1)

    @property
    def a(self):
        return self.__a
    
    @property
    def a_prime(self):
        return self.__a_prime
    
    @property
    def weights(self):
        return self.__weights

    @weights.setter
    def weights(self, value: Matrix):
        self.__weights = value
    
    @property
    def biases(self):
        return self.__biases

    @biases.setter
    def biases(self, value: Matrix):
        self.__biases = value

    def propogate_forwards(self, inputs: Matrix) -> Tuple[Matrix, Matrix]:
        z = self.weights.dot(inputs) + self.biases
        activation = z.apply(self.a)
        return z, activation
        