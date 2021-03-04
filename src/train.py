# pyright: reportMissingTypeStubs=false
import logging, math, argparse, datetime
from typing import Tuple
from .Model.Layer import Layer
from .Mathematics.Matrix import Matrix
from .Mathematics.Model_Calculations import cost, error_prime
from .Model.Network import Network
from .IO.ModelRepositoryFactory import model_data_repo_factory
from .IO.ModelRepository import ModelRepository
from .IO.TrainingDataRepository import trainingDataRepository

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s %(name)s:%(message)s')
logger = logging.getLogger('model')

def load_data(name: str) -> Tuple[Matrix, Matrix]:
    logger.debug(f"Loading data from: {name}")
    trainingData = trainingDataRepository.read(name)

    data = list(zip(*[list(row.rgb) + row.labels for row in trainingData.data]))
    number_of_samples =  len(trainingData.data) - 1

    red_arr = data[0]
    green_arr = data[1]
    blue_arr = data[2]
    inputs = Matrix([red_arr, green_arr, blue_arr], 3, number_of_samples)

    labels = Matrix(data[3:], len(trainingData.field_names) - 3, number_of_samples)
    
    return inputs, labels

def doTraining(input:str, name: str, epochs:int, rate:float, exportLayers:bool):
    pixels, labels = load_data(input)

    pixels = pixels.divide(255)

    repo: ModelRepository

    try:
        repo = model_data_repo_factory.create_repo(name)
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
    parser.add_argument("input", help="Training data name", type=str)
    parser.add_argument("-l", "--learningRate", help="Learning rate for the network", type=float, default=0.005)
    parser.add_argument("-e", "--epochs", help="Number of iterations to train the network", type=int, default=2000)
    parser.add_argument("-n", "--name", help="Model name", type=str, default=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    parser.add_argument("-x", "--exportLayers", help="Export layers weights and biases in CSV format", action='store_true')
    args = parser.parse_args()

    doTraining(args.input, args.name, args.epochs, args.learningRate, args.exportLayers)
