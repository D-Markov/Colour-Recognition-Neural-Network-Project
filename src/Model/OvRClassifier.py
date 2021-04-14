from typing import List, Callable, Tuple, Dict, Union
from src.Model.Layer import Layer
from src.Mathematics.Matrix import Matrix
from src.Model.Network import Network
import random
from tqdm import trange

class OvRClassifier:
    def __init__(
        self,
        layer_factory: Callable[[], List[Layer]],
        learning_rate: float,
        cost: Callable[[Matrix, Matrix], float],
        error_prime: Callable[[Matrix, Matrix], Matrix]):

        self.__layer_factory = layer_factory
        self.__learning_rate = learning_rate
        self.__cost = cost
        self.__error_prime = error_prime
        return
    
    def train_model(self, inputs: Matrix, labels: List[str], epochs: int) -> Tuple[List[Tuple[str, List[Layer]]], List[List[float]]]:
        assert inputs.colomns == len(labels), F"Number of labels must match the number of training samples ({len(labels)} <> {inputs.colomns})"

        model: List[Tuple[str, List[Layer]]] = []
        costs: List[List[float]] = []

        training_sets = OvRClassifier.distribute_training_data(inputs, labels, 1, None)

        for label, data in training_sets.items():
            current_inputs = data[0]
            labels_mask = data[1]

            layers = self.__layer_factory()
            network = Network(layers)

            for _ in trange(epochs):
                network.train(current_inputs, labels_mask, self.__cost, self.__error_prime, self.__learning_rate)

                # convergence check
                if(len(network.costs) >= 10 and network.costs[-10] - network.costs[-1] < 0.00001):
                    break

            costs.append(network.costs)
            model.append((label, layers))

        return model, costs

    def run_model(self, model: List[Tuple[str, List[Layer]]], inputs: Matrix) -> List[str]:

        labels: List[str] = []
        results: List[List[float]] = []
        
        for label, layers in model:
            network = Network(layers)
            result = network.run(inputs)[0]
            labels.append(label)
            results.append(result)

        results_labled: List[str] = [""] * inputs.colomns

        for idx, values in enumerate(zip(*results)):
            best_value = max(values)
            
            if best_value > .5:
                label = labels[values.index(best_value)]
                results_labled[idx] = label

        return results_labled

    @staticmethod
    def group_by_label(inputs: Matrix, labels: List[str]) -> Dict[str, List[List[float]]]:
        by_label: Dict[str, List[List[float]]] = {}

        for idx, label in enumerate(labels):
            if not label in by_label.keys():
                by_label[label] = []

            by_label[label].append(inputs[idx])

        return by_label

    @staticmethod
    def distribute_training_data(inputs: Matrix, labels: List[str], proportion: float, samples_count: Union[int, None] = None) -> Dict[str, Tuple[Matrix, Matrix]]:
        inputsT = inputs.rtocol()
        gouped_by_label = OvRClassifier.group_by_label(inputsT, labels)

        distributed_data: Dict[str, Tuple[List[List[float]], List[int]]] = {}

        for label in gouped_by_label:
            rgbs = gouped_by_label[label].copy()
            mask = [1] * len(rgbs) 

            other_data: List[List[float]]= []
            for other_label in [l for l in gouped_by_label if l != label]:
                other_data.extend(gouped_by_label[other_label])

            proportion_amount = int(len(rgbs) * proportion)
            rgbs.extend(random.choices(other_data, k=proportion_amount))
            mask.extend([0] * proportion_amount)

            rgbs_shuffled: List[List[float]] = []
            mask_shuffled: List[int] = []
            indices = list(range(len(rgbs)))
            random.shuffle(indices)
            for idx in indices:
                rgbs_shuffled.append(rgbs[idx])
                mask_shuffled.append(mask[idx])

            # rgbs_shuffled.extend(rgbs)
            # mask_shuffled.extend(mask)

            if samples_count:
                distributed_data[label] = (rgbs_shuffled[:samples_count], mask_shuffled[:samples_count])
            else:
                distributed_data[label] = (rgbs_shuffled, mask_shuffled)

        return {
            label: (Matrix(data[0]).rtocol(), Matrix([data[1]]))
            for label, data in distributed_data.items()
        }
