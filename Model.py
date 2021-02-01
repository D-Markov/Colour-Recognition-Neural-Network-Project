# pyright: reportMissingTypeStubs=false
from os import write
from typing import Tuple, Any
from Matrix import Matrix
import h5py as h5
from Layer import Layer
from Model_Calculations import sigmoid, sigmoid_prime, c, dc
from Network import Network
import csv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s:%(message)s')

logger = logging.getLogger('model')

def load_data(path: str, x_set_name: str, y_set_name: str) -> Tuple[Any, Any]:
    with h5.File(path, "r") as dataset:
        x = dataset[x_set_name][:]
        y = dataset[y_set_name][:]
        
        return x, y


images, matches = load_data(r"train_catvnoncat.h5", "train_set_x", "train_set_y")
images_flattened = []

matches = [int(match) for match in matches]
for image in images:
    pixels = [pixel for row in image for pixel in row]
    components = [int(component) for pixel in pixels for component in pixel]
    images_flattened.append(components)


imagesM = Matrix(images_flattened).rtocol().divide(255)

labels = Matrix([matches]).rtocol()

layers = [
    Layer(imagesM.rows, 1, sigmoid, sigmoid_prime),
    # Layer(5, 1, sigmoid, sigmoid_prime),
    Layer(1, 1, sigmoid, sigmoid_prime)
]

# with open('pre-train-weights-layer0.csv','w') as f:
#     writer = csv.writer(f)
#     for row in layers[0].weights:
#         writer.writerow(row)

# with open('pre-train-biases-layer0.csv','w') as f:
#     writer = csv.writer(f)
#     for row in layers[0].biases:
#         writer.writerow(row)

nn = Network(layers, c, dc, 0.001)


for i in range(2):
    logger.info(f'running epoch {i}')
    nn.train(imagesM, labels)

# with open('post-train-weights-layer0.csv','w') as f:
#     writer = csv.writer(f)
#     for row in layers[0].weights:
#         writer.writerow(row)

# with open('post-train-biases-layer0.csv','w') as f:
#     writer = csv.writer(f)
#     for row in layers[0].biases:
#         writer.writerow(row)