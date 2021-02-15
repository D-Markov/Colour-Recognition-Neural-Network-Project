# pyright: reportMissingTypeStubs=false
import os
from typing import Tuple, Any
from .Mathematics.Matrix import Matrix
import h5py as h5
from .Model.Layer import Layer
from .Mathematics.Model_Calculations import cost, derror
from .Model.Network import Network
import csv
import logging
from .IO.ModelRepository import ModelRepository

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s %(name)s:%(message)s')
logger = logging.getLogger('model')

tmp_dir = '.tmp'
if not os.path.isdir(tmp_dir):
    os.mkdir(tmp_dir)

models_dir = 'ModelData'
if not os.path.isdir(models_dir):
    os.mkdir(models_dir)


def load_data(path: str, x_set_name: str, y_set_name: str) -> Tuple[Any, Any]:
    logger.debug(f"Loading x set: {x_set_name}; y_set {y_set_name} from {path}")
    with h5.File(path, "r") as dataset:
        x = dataset[x_set_name][:]
        y = dataset[y_set_name][:]
        
        return x, y

def save_layer_to_csv(layers, file_base_name):
    for i, layer in enumerate(layers):
        with open(fr'{tmp_dir}\{file_base_name}-weights-layer{i}.csv','w') as f:
            writer = csv.writer(f)
            for row in layer.weights:
                writer.writerow(row)

        with open(fr'{tmp_dir}\{file_base_name}-biases-layer{i}.csv','w') as f:
            writer = csv.writer(f)
            for row in layer.biases:
                writer.writerow(row)

def flatter_by_pixel(images):
    flattened = []
    for image in images:
        pixels = [pixel for row in image for pixel in row]
        components = [int(component) for pixel in pixels for component in pixel]
        flattened.append(components)
    return flattened

def flatter_by_colour(images):
    flattened = []
    for image in images:
        image_colours = []
        for i in range(3):
            colour = [pixel[i] for row in image for pixel in row]
            image_colours.extend(colour)
        flattened.append(image_colours)
    return flattened

images, matches = load_data(r"TrainingData\train_catvnoncat.h5", "train_set_x", "train_set_y")
images_flattened = []

logger.debug(f"Tranforming data...")
images_flattened = flatter_by_colour(images)

imagesM = Matrix(images_flattened).rtocol().divide(255)
labels = Matrix([matches]).rtocol()

layers = [
    Layer(imagesM.rows, 5, 'sigmoid', 'sigmoid_prime'),
    Layer(5, 1, 'sigmoid', 'sigmoid_prime'),
    Layer(1, 1, 'sigmoid', 'sigmoid_prime')
]

model_repo = ModelRepository(models_dir)

nn = Network(layers)

# *** training ***
save_layer_to_csv(layers, 'pre-train')
model_repo.write('untrained.pkl', layers)

for i in range(20):
    logger.info(f'running epoch {i}')
    nn.train(imagesM, labels, cost, derror, 0.005)

save_layer_to_csv(layers, 'post-train')
model_repo.write('trained.pkl', layers)
with open(fr'{tmp_dir}\costs.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(nn.costs)


# *** running ***
# layers = model_repo.read('keep_trained.pkl')
# results = nn.run(imagesM)
# logger.debug(f"Number of results: {len(results)}")
# print(results)
