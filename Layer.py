from Matrix import Matrix

class Layer:
    def __init__(self, number_of_inputs, number_of_outputs,  a, a_prime):
        self.__a = a 
        self.__a_prime = a_prime
        self.__weights = Matrix.randomMatrix(number_of_inputs, number_of_outputs)
        self.__biases = Matrix.zeroMatrix(number_of_inputs, 1)

    @property
    def a(self):
        return self.__a
    
    @property
    def a_prime(self):
        return self.__a_prime
    
    @property
    def weights(self):
        return self.__weights
    
    @property
    def biases(self):
        return self.__biases
