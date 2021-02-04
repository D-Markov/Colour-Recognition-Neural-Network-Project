import logging
from typing import Callable, List
from .Layer import Layer
from src.Mathematics.Matrix import Matrix


class Network:
    __logger = logging.getLogger('Network')

    def __init__(self, layers: List[Layer],
        cost: Callable[[Matrix, Matrix], float],
        cost_prime: Callable[[Matrix, Matrix], float],
        learning_rate: float):
        
        if len(layers) <= 1:
            raise ValueError("Layers should have layers for training")
        self.__layers = layers
        self.__cost = cost
        self.__cost_prime = cost_prime
        self.__learning_rate = learning_rate
    
    def train(self, inputs: Matrix, labels: Matrix) -> None:
        self.__train_layer(inputs, labels, 0)


    def __train_layer(self, inputs: Matrix, labels: Matrix, index: int = 0) -> Matrix:
        Network.__logger.debug(f'Forward propogating layer {index}')
        current_layer = self.__layers[index]        
        z = current_layer.weights.dot(inputs) + current_layer.biases
        next_layer_activations = z.apply(current_layer.a)

        if index != len(self.__layers) - 1:            
            dzp = self.__train_layer(next_layer_activations, labels, index + 1)
            a = z.apply(current_layer.a_prime)
            dz = self.__layers[index + 1].weights.rtocol().dot(dzp).multiply(a)
        else:


            Network.__logger.debug(f'Output layer {index}')
            cost = self.__cost(next_layer_activations, labels) # pyright: reportUnusedVariable=false
            da = z.apply(current_layer.a_prime)
            dc = self.__cost_prime(next_layer_activations, labels)

            dz = da.multiply(dc) 

        Network.__logger.debug(f'Backward propogating layer {index}')
        dw = dz.dot(inputs.rtocol()).divide(labels.rows)
        db = dz.rowsSum().divide(labels.rows)
        current_layer.weights -= dw.multiply(self.__learning_rate)
        current_layer.biases -= db.multiply(self.__learning_rate)

        return dz            
            
        #self.__propogate_backwards()


    
    #def __propogate_backwards(self, layer: Layer, inputs, labels, label_index, output):
        
        #dz = output - labels[label_index]


    #return 0       