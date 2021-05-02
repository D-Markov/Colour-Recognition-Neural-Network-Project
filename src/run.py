# pyright: reportMissingTypeStubs=false
from src.Model.OvRClassifier import OvRClassifier
from typing import List
from .Mathematics.Matrix import Matrix
import logging, argparse, csv
from pathlib import Path
from .IO.ModelRepositoryFactory import model_data_repo_factory

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s %(name)s:%(message)s')
logger = logging.getLogger('run')

def load_data(file_name: str) -> Matrix:
    logger.debug(f"Loading data from: {file_name}")
    rgbs: List[List[int]] = []

    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for r, g, b in reader:
            rgbs.append([int(r), int(g), int(b)])

    return Matrix(rgbs)


def write_results(file_name: str, results: List[str]) -> None:
    logger.debug(f"Writing results to: {file_name}")
    with open(file_name, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows([[result] for result in results])


def load_model(modelName: str):
    model_repo = model_data_repo_factory.get_repo(modelName)
    layers = model_repo.read()
    return layers


def runFromFile(model_name: str, input_data: str):
    model = load_model(model_name)
    inputs = load_data(input_data)
    inputs = inputs.divide(255)
    logger.debug(f"Running model: {model_name}")
    results = OvRClassifier.run_model(model, inputs)
    
    p = Path(input_data)
    name= p.stem
    p = p.with_name(f"{name}-result.csv")

    write_results(f"{p}", results)


def runFromRgb(model_name: str, rgb: List[int]):
    model = load_model(model_name)
    inputs = Matrix([[rgb[0]], [rgb[1]], [rgb[2]]])
    inputs = inputs.divide(255)
    logger.debug(f"Running model: {model_name}")
    results = OvRClassifier.run_model(model, inputs)
    print(f"RGB {rgb} is {results[0]}")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Runs the Neural Network")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--file', type=str, help="Use data from csv file (R,G,B) without header. ")
    group.add_argument('--rgb', type=int, nargs=3, help="RGB values ([0-255] [0-255] [0-255])")
    parser.add_argument('modelName', type=str)

    args = parser.parse_args()
    print(args)
    if  args.file != None :
        runFromFile(args.modelName, args.file)
    elif args.rgb != None:
        runFromRgb(args.modelName, args.rgb)
