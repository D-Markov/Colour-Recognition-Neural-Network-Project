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


def doTraining(input:str, name: str, epochs:int, rate:float, exportLayers:bool):
    pixels, labels = load_data(input)
    pixels = pixels.divide(255)

    repo: ModelRepository
    try:
        repo = model_data_repo_factory.create_repo(name)
    except ValueError:
        print(f"Repository {name} already exists")
        return
    
    create_layers = lambda: [
        Layer.create(pixels.rows, 6, math.sqrt(pixels.rows), 'relu', 'relu_prime'),
        Layer.create(6, 12, math.sqrt(6), 'relu', 'relu_prime'),
        Layer.create(12, 6, math.sqrt(12), 'relu', 'relu_prime'),
        # Layer.create(pixels.rows, 6, math.sqrt(pixels.rows), 'sigmoid', 'sigmoid_prime'),
        # Layer.create(6, 12, math.sqrt(12), 'sigmoid', 'sigmoid_prime'),
        Layer.create(6, 1, math.sqrt(6), 'sigmoid', 'sigmoid_prime')
    ]

    classifier = OvRClassifier(create_layers, rate, cost, error_prime)
    layers, costs= classifier.train_model(pixels, labels, epochs)

    repo.write(layers)
    repo.write_costs(costs)

    # if(exportLayers):
    #     repo.export_to_csv(layers, "post")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train Neural Network')
    parser.add_argument("input", help="Training data name", type=str)
    parser.add_argument("-l", "--learningRate", help="Learning rate for the network", type=float, default=0.01)
    parser.add_argument("-e", "--epochs", help="Number of iterations to train the network", type=int, default=2500)
    parser.add_argument("-n", "--name", help="Model name", type=str, default=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    parser.add_argument("-x", "--exportLayers", help="Export layers weights and biases in CSV format", action='store_true')
    args = parser.parse_args()

    print("input: ", args.input)
    print("name: ", args.name)
    print("epochs: ", args.epochs)
    print("learningRate: ", args.learningRate)
    print("exportLayers: ", args.exportLayers)

    doTraining(args.input, args.name, args.epochs, args.learningRate, args.exportLayers)
