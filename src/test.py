# pyright: reportMissingTypeStubs=false
from src.Model.OvRClassifier import OvRClassifier
from typing import Tuple, List
from .Mathematics.Matrix import Matrix, Scalar
import logging, argparse
from .IO.ModelRepositoryFactory import model_data_repo_factory
from .IO.TrainingDataRepository import trainingDataRepository

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s %(name)s:%(message)s')
logger = logging.getLogger('run')

def get_accuracy(expected: List[Scalar], actual: List[float]) -> Tuple[float, float, float]:
    tp = tn = fp = fn = 0.0
    cnt = len(expected)

    for pair in zip([int(e) for e in expected], [int(round(r)) for r in actual]):
        if(pair[0] == 1 and pair[1] == 1):
            tp += 1
        elif(pair[0] == 0 and pair[1] == 0):
            tn += 1
        elif(pair[0] == 0 and pair[1] == 1):
            fp += 1
        elif(pair[0] == 1 and pair[1] == 0):
            fn += 1
        
    accuracy = (tp + tn) / cnt
    precision = tp / (tp + fp) if tp != 0 and fp != 0 else 0.0
    recall = tp / (tp + fn)

    return accuracy, precision, recall

def load_training_data(name: str) -> Tuple[Matrix, List[str]]:
    logger.debug(f"Loading data from: {name}")
    trainingData = trainingDataRepository.read(name)

    data = list(zip(*[list(row.rgb) for row in trainingData]))
    labels = [row.label for row in trainingData]

    return Matrix([list(d) for d in data]), labels

def load_model(modelName: str):
    model_repo = model_data_repo_factory.get_repo(modelName)
    layers = model_repo.read()
    return layers

def calculate_confusion_matrix(results: List[str], labels: List[str]) -> Tuple[List[List[int]], List[str], List[Tuple[int, str, str]]]:
    label_names = sorted(set(labels))
    label_names.append("unknown")
    matrix_size = len(label_names)
    confusion = [[0] * matrix_size for _ in label_names]
    unmatched: List[Tuple[int, str, str]] = []

    for idx, label in enumerate(labels):
        tidx = label_names.index(label)
        if(results[idx] == label):            
            confusion[tidx][tidx] += 1
        elif results[idx] in label_names:
            ridx = label_names.index(results[idx])
            confusion[tidx][ridx] += 1
        else:
            confusion[tidx][-1] += 1
            unmatched.append((idx, label, results[idx]))

    return confusion, label_names, unmatched

def print_confusion_matrix(confusion_matrix: List[List[int]], label_names: List[str]):
    max_len = max(map(lambda x: len(x), label_names))
    print("\t".join([" " * max_len] + label_names + [""]))
    for idx, row in enumerate(confusion_matrix):
        values = '\t'.join([label_names[idx]] + [str(v) for v in row])
        print(values)

def doTest(model_name: str, input_data: str):
    model = load_model(model_name)
    inputs, labels = load_training_data(input_data)
    inputs = inputs.divide(255)
    logger.debug(f"Running model: {model_name}")
    results = OvRClassifier.run_model(model, inputs)

    confusion_matrix, label_names, unmatched = calculate_confusion_matrix(results, labels)

    print("Confusion Matrix:\r\n")
    print_confusion_matrix(confusion_matrix, label_names)

    print(f"\r\nUnmatched ({len(unmatched)}):\r\n", unmatched)
    logger.debug(f"Number of results: {len(results)}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Neural Network")
    parser.add_argument("model_name", help="The name of the model to use", type=str)
    parser.add_argument("input_data", help="The input data to the network", type=str)
    args = parser.parse_args()
    
    doTest(args.model_name, args.input_data)
