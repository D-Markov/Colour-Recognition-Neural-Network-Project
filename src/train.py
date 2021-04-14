# pyright: reportMissingTypeStubs=false
import logging, math, argparse, datetime
from src.Model.OvRClassifier import OvRClassifier
from typing import Tuple, List
from .Model.Layer import Layer
from .Mathematics.Matrix import Matrix
from .Mathematics.Model_Calculations import cost, error_prime
from .IO.ModelRepositoryFactory import model_data_repo_factory
from .IO.ModelRepository import ModelRepository
from .IO.TrainingDataRepository import trainingDataRepository

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s %(name)s:%(message)s')
logger = logging.getLogger('train')


def load_data(name: str) -> Tuple[Matrix, List[str]]:
    logger.debug(f"Loading data from: {name}")
    trainingData = trainingDataRepository.read(name)

    data = list(zip(*[list(row.rgb) for row in trainingData]))
    labels = [row.label for row in trainingData]

    return Matrix([list(d) for d in data]), labels


def doTraining(input:str, name: str, epochs:int, rate:float, tolerance: float, exportLayers:bool):
    pixels, labels = load_data(input)
    pixels = pixels.divide(255)

    try:
        repo = model_data_repo_factory.get_repo(name)
        print(f"Repository {name} already exists")
        return
    except ValueError:
        pass

    layer_defs = [
        (pixels.rows, 6, math.sqrt(pixels.rows), 'relu', 'relu_prime'),
        (6, 12, math.sqrt(6), 'relu', 'relu_prime'),
        (12, 6, math.sqrt(12), 'relu', 'relu_prime'),
        (6, 1, math.sqrt(6), 'sigmoid', 'sigmoid_prime')
    ]

    create_layers = lambda: [
        Layer.create(layer_def[0],layer_def[1],layer_def[2],layer_def[3],layer_def[4]) for layer_def in layer_defs
    ]

    classifier = OvRClassifier(create_layers, rate, cost, error_prime)
    layers, costs= classifier.train_model(pixels, labels, epochs, tolerance)

    repo: ModelRepository
    try:
        repo = model_data_repo_factory.create_repo(name)
    except ValueError:
        print(f"Repository {name} already exists")
        return

    model_parameters = {
        "model": "OvRClassifier",
        "epochs": epochs,
        "rate": rate,
        "tolerance": tolerance,
        "exportLayers": exportLayers
    }

    for idx, layer_def in enumerate(layer_defs):
        model_parameters[f"layer-{idx}"] = f"number_of_inputs: {layer_def[0]}, number_of_outputs: {layer_def[1]}, factor: {layer_def[2]}, activation: {layer_def[3]}, activation_prime: {layer_def[4]}"

    repo.write(layers)
    repo.write_costs(costs)
    repo.write_model_parameters(model_parameters)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train Neural Network')
    parser.add_argument("input", help="Training data name", type=str)
    parser.add_argument("-l", "--learningRate", help="Learning rate for the network", type=float, default=0.01)
    parser.add_argument("-t", "--tolerance", help="Error tolerance to stop learing", type=float, default=0.0001)
    parser.add_argument("-e", "--epochs", help="Number of iterations to train the network", type=int, default=2500)
    parser.add_argument("-n", "--name", help="Model name", type=str, default=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    parser.add_argument("-x", "--exportLayers", help="Export layers weights and biases in CSV format", action='store_true')
    args = parser.parse_args()

    print("input: ", args.input)
    print("name: ", args.name)
    print("epochs: ", args.epochs)
    print("learningRate: ", args.learningRate)
    print("tolerance: ", args.tolerance)
    print("exportLayers: ", args.exportLayers)

    doTraining(args.input, args.name, args.epochs, args.learningRate, args.tolerance, args.exportLayers)
