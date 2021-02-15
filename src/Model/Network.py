import logging
from typing import Callable, List, NamedTuple, Tuple
from .Layer import Layer
from src.Mathematics.Matrix import Matrix, Scalar
from collections import deque

class CacheEntry(NamedTuple):
    Z: Matrix
    activations: Matrix

class Network:
    __logger = logging.getLogger('Network')

    def __init__(self, layers: List[Layer]):
        
        if len(layers) <= 1:
            raise ValueError("Layers should have layers for training")
        self.__layers = layers
        self.__costs = []
        self.__cache = deque()
    
    @property
    def costs(self):
        return self.__costs

    
    def train(self, inputs: Matrix, labels: Matrix,
        cost: Callable[[Matrix, Matrix], float],
        error_prime: Callable[[Matrix, Matrix], Matrix],
        learning_rate: float) -> None:
        
        self.__train_layer(inputs, labels, cost, error_prime, learning_rate, 0)


    def __train_layer(self, inputs: Matrix, labels: Matrix,
        cost: Callable[[Matrix, Matrix], float],
        error_prime: Callable[[Matrix, Matrix], Matrix],
        learning_rate: float, index: int = 0) -> Matrix:

        assert(inputs.colomns == labels.colomns)
        Network.__logger.debug(f'Forward propogating layer {index}')
        current_layer = self.__layers[index]
        assert(current_layer.weights.colomns == inputs.rows)
        assert(current_layer.biases.rows == current_layer.weights.rows)
        assert(current_layer.biases.colomns == 1)

        # Forward propagation
        next_layer_activations = self.propogate_forward(inputs, current_layer.weights, current_layer.biases, current_layer.a)

        if index != len(self.__layers) - 1:            
            dzp = self.__train_layer(next_layer_activations, labels, cost, error_prime, learning_rate, index + 1)

            Network.__logger.debug(f'Backward propogating layer {index}')
            dz, dW, dB = self.propogate_backwards(dzp, current_layer.weights, labels.rows, current_layer.a_prime)
            current_layer.weights -= dW.multiply(learning_rate)
            current_layer.biases -= dB.multiply(learning_rate)
            return dz
        else:
            Network.__logger.debug(f'Output layer {index}')
            costVal = cost(next_layer_activations, labels) # pyright: reportUnusedVariable=false
            self.__costs.append(costVal)
            Network.__logger.debug(f'Backward propogating layer {index}')

            da = error_prime(next_layer_activations, labels)

            dz, dW, dB = self.propogate_backwards(da, current_layer.weights, labels.rows, current_layer.a_prime)
            current_layer.weights -= dW.multiply(learning_rate)
            current_layer.biases -= dB.multiply(learning_rate)
            return dz

    def propogate_forward(self, activations: Matrix, weights: Matrix, biases: Matrix, activation: Callable[[Scalar], Scalar]) -> Matrix:
        z = weights.dot(activations) + biases
        next_layer_activations = z.apply(activation)
        self.__cache.append(CacheEntry(z, activations))

        return next_layer_activations

    def propogate_backwards(self, dAl: Matrix, weights: Matrix, m: int, dactivation: Callable[[Scalar], Scalar]) -> Tuple[Matrix, Matrix, Matrix]:
        cacheEntry: CacheEntry = self.__cache.pop()
        dZ = dAl.multiply(cacheEntry.Z.apply(dactivation))
        dW = dZ.dot(cacheEntry.activations.rtocol()).divide(m)
        dB = dZ.rowsSum().divide(m)
        dAl_1 = weights.rtocol().dot(dZ)
        
        return dAl_1, dW, dB

    def run(self, data:Matrix) -> List[float]:
        layer_input = data

        for layer in self.__layers:
            z = layer.weights.dot(layer_input) + layer.biases
            layer_input = z.apply(layer.a)

        return [col for row in layer_input for col in row ]

    
    #def __propogate_backwards(self, layer: Layer, inputs, labels, label_index, output):
        
        #dz = output - labels[label_index]


    #return 0       