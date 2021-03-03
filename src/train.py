# pyright: reportMissingTypeStubs=false
import os, csv, logging, math, argparse, datetime
from typing import Tuple, Any
import h5py as h5
from .Model.Layer import Layer
from .Mathematics.Matrix import Matrix
from .Mathematics.Model_Calculations import cost, error_prime
from .Model.Network import Network
from .IO.ModelRepositoryFactory import ModelRepositoryFactory
from .IO.ModelRepository import ModelRepository

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s %(name)s:%(message)s')
logger = logging.getLogger('model')

models_dir = 'ModelData'
if not os.path.isdir(models_dir):
    os.mkdir(models_dir)


def load_data(path: str, x_set_name: str, y_set_name: str) -> Tuple[Any, Any]:
    logger.debug(f"Loading x set: {x_set_name}; y_set {y_set_name} from {path}")
    with h5.File(path, "r") as dataset:
        x = dataset[x_set_name][:]
        y = dataset[y_set_name][:]
        
        return x, y


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
            # components = [int(component) for pixel in pixels for component in pixel]
            image_colours.extend(colour)
        flattened.append(image_colours)
    return flattened

def doTraining(input:str, name: str, epochs:int, rate:float, exportLayers:bool):
    images, matches = load_data(input, "train_set_x", "train_set_y")
    images_flattened = []

    logger.debug(f"Tranforming data...")
    matches = [int(match) for match in matches]
    images_flattened = flatter_by_colour(images)
    
    assert(len(images_flattened) == 209)
    assert(all([len(img) == 12288 for img in images_flattened]))

    number_of_train_samples = 209
    imagesM = Matrix(images_flattened[:number_of_train_samples]).rtocol().divide(255)

    labels = Matrix([matches[:number_of_train_samples]])

    repo_factory = ModelRepositoryFactory(models_dir)

    repo: ModelRepository

    try:
        repo = repo_factory.create_repo(name)
    except ValueError:
        print(f"Repository {name} already exists")
        return
    
    layers = [
        Layer.create(imagesM.rows, 7, math.sqrt(imagesM.rows), 'sigmoid', 'sigmoid_prime'),
        # Layer.create(5, 1, 'sigmoid', 'sigmoid_prime'),
        Layer.create(7, 1, math.sqrt(7), 'sigmoid', 'sigmoid_prime')
    ]

    if(exportLayers):
        repo.export_to_csv(layers, "pre")

    nn = Network(layers)

    for i in range(epochs):
        logger.info(f'running epoch {i}')
        nn.train(imagesM, labels, cost, error_prime, rate)

    repo.write(layers)
    repo.write_costs(nn.costs)

    if(exportLayers):
        repo.export_to_csv(layers, "post")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train Neural Network')
    parser.add_argument("input", help="Training data file", type=str)
    parser.add_argument("-l", "--learningRate", help="Learning rate for the network", type=float, default=0.005)
    parser.add_argument("-e", "--epochs", help="Number of iterations to train the network", type=int, default=2000)
    parser.add_argument("-n", "--name", help="Model name", type=str, default=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    parser.add_argument("-x", "--exportLayers", help="Export layers weights and biases in CSV format", action='store_true')
    args = parser.parse_args()

    doTraining(args.input, args.name, args.epochs, args.learningRate, args.exportLayers)

