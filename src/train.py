# pyright: reportMissingTypeStubs=false
import os, csv, logging, math, argparse, datetime
from typing import Tuple
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

def load_data(path: str) -> Tuple[Matrix, Matrix]:
    logger.debug(f"Loading data from: {path}")
    with open(path, "r") as dataset:
        reader = csv.reader(dataset)
        fieldnames = next(reader)
        data = list(zip(*[[int(c) for c in row] for row in reader]))

        red_arr = data[0]
        green_arr = data[1]
        blue_arr = data[2]
        inputs = Matrix([red_arr, green_arr, blue_arr], 3, reader.line_num - 1)

        labels = Matrix(data[3:], len(fieldnames) - 3, reader.line_num - 1)
        
        return inputs, labels

def doTraining(input:str, name: str, epochs:int, rate:float, exportLayers:bool):
    pixels, labels = load_data(input)

    pixels = pixels.divide(255)

    repo_factory = ModelRepositoryFactory(models_dir)

    repo: ModelRepository

    try:
        repo = repo_factory.create_repo(name)
    except ValueError:
        print(f"Repository {name} already exists")
        return
    
    layers = [
        Layer.create(pixels.rows, 12, math.sqrt(pixels.rows), 'sigmoid', 'sigmoid_prime'),
        Layer.create(12, 24, math.sqrt(12), 'sigmoid', 'sigmoid_prime'),
        Layer.create(24, labels.rows, math.sqrt(labels.rows), 'sigmoid', 'sigmoid_prime')
    ]

    if(exportLayers):
        repo.export_to_csv(layers, "pre")

    nn = Network(layers)

    for i in range(epochs):
        logger.info(f'running epoch {i}')
        nn.train(pixels, labels, cost, error_prime, rate)

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