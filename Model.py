from typing import Callable
import math
from Matrix import Matrix
import h5py as h5
from Layer import Layer
from Model_Calculations import l,c,dl,dc



def load_data(path, x_set_name, y_set_name):
    with h5.File(path, "r") as dataset:
        x = dataset[x_set_name][:]
        y = dataset[y_set_name][:]
        return x, y


images, matches = load_data(r"train_catvnoncat.h5", "train_set_x", "train_set_y")
images_flattened = []

for image in images:
    pixels = [pixel for row in image for pixel in row]
    components = [component for pixel in pixels for component in pixel]
    images_flattened.append(components)


imagesM = Matrix(images_flattened)

imagesM.rtocol()
m = Matrix([matches])
m.rtocol()

layers = [
    Layer(imagesM.rows, 5, sigmoid, sigmoid_prime),
    Layer(5, 1, sigmoid, sigmoid_prime),
    Layer(1, 1, sigmoid, sigmoid_prime)
]