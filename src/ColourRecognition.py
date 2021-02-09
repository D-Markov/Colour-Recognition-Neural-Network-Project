# pyright: reportMissingTypeStubs=false
import os
from typing import Tuple, Any
from src.Mathematics.Matrix import Matrix
import h5py as h5
from src.Model.Layer import Layer
from src.Mathematics.Model_Calculations import sigmoid, sigmoid_prime, c, dc
from src.Model.Network import Network
import csv
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s %(name)s:%(message)s')
logger = logging.getLogger('model')

tmp_dir = '.tmp'

if not os.path.isdir(tmp_dir):
    os.mkdir(tmp_dir)


def load_data(path: str, x_set_name: str, y_set_name: str) -> Tuple[Any, Any]:
    with h5.File(path, "r") as dataset:
        x = dataset[x_set_name][:]
        y = dataset[y_set_name][:]
        
        return x, y

def save_layer(layers, file_base_name):
    for i, layer in enumerate(layers):
        with open(fr'{tmp_dir}\{file_base_name}-weights-layer{i}.csv','w') as f:
            writer = csv.writer(f)
            for row in layer.weights:
                writer.writerow(row)

        with open(fr'{tmp_dir}\{file_base_name}-biases-layer{i}.csv','w') as f:
            writer = csv.writer(f)
            for row in layer.biases:
                writer.writerow(row)


images, matches = load_data(r"ModelData\train_catvnoncat.h5", "train_set_x", "train_set_y")
images_flattened = []

matches = [int(match) for match in matches]
for image in images:
    pixels = [pixel for row in image for pixel in row]
    components = [int(component) for pixel in pixels for component in pixel]
    images_flattened.append(components)

imagesM = Matrix(images_flattened).rtocol().divide(255)

labels = Matrix([matches]).rtocol()

layers = [
    Layer(imagesM.rows, 5, sigmoid, sigmoid_prime),
    Layer(5, 1, sigmoid, sigmoid_prime),
    Layer(1, 1, sigmoid, sigmoid_prime)
]

save_layer(layers, 'pre-train')

nn = Network(layers, c, dc, 0.001)

for i in range(2):
    logger.info(f'running epoch {i}')
    nn.train(imagesM, labels)

save_layer(layers, 'post-train')

with open(fr'{tmp_dir}\costs.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(nn.costs)
