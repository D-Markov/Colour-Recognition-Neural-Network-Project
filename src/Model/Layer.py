import logging
from typing import Tuple
from src.Mathematics.Matrix import Matrix
from src.Mathematics.Model_Calculations import activation_functions

class Layer:
    __logger = logging.getLogger('Layer')

    def __init__(self, a: str, a_prime: str, weights: Matrix, biases: Matrix):
        self.__a = a 
        self.__a_prime = a_prime
        self.__weights = weights
        self.__biases = biases
        Layer.__logger.debug(f'Created w[{self.__weights.rows},{self.__weights.colomns}]; b[{self.__biases.rows},{self.__biases.colomns}]')

    @property
    def a(self):
        return activation_functions[self.__a]
    
    @property
    def a_prime(self):
        return activation_functions[self.__a_prime]
    
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

    @staticmethod
    def create(number_of_inputs: int, number_of_outputs: int, factor: float, a: str, a_prime: str):
        return Layer(
            a,
            a_prime,
            Matrix.randomMatrix(number_of_outputs, number_of_inputs).divide(factor),
            Matrix.zeroMatrix(number_of_outputs, 1)
        )

    def propogate_forwards(self, inputs: Matrix) -> Tuple[Matrix, Matrix]:
        z = self.weights.dot(inputs) + self.biases
        activation = z.apply(self.a)
        return z, activation
        