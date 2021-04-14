from typing import List, Callable, Tuple, Dict
from src.Model.Layer import Layer
from src.Mathematics.Matrix import Matrix
from src.Model.Network import Network
import random, logging
from tqdm import trange

class OvRClassifier:
    logger = logging.getLogger('OvRClassifier')

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
    
    def train_model(self, inputs: Matrix, labels: List[str], epochs: int, tolerance: float = 0.0001) -> Tuple[List[Tuple[str, List[Layer]]], Dict[str, List[float]]]:
        assert inputs.colomns == len(labels), F"Number of labels must match the number of training samples ({len(labels)} <> {inputs.colomns})"

        model: List[Tuple[str, List[Layer]]] = []
        costs: Dict[str, List[float]] = {}

        training_sets = OvRClassifier.distribute_training_data(inputs, labels, 1)

        for label, data in training_sets.items():
            current_inputs = data[0]
            labels_mask = data[1]

            layers = self.__layer_factory()
            network = Network(layers)

            for _ in trange(epochs, desc=label):
                network.train(current_inputs, labels_mask, self.__cost, self.__error_prime, self.__learning_rate)

                # convergence check
                if(len(network.costs) >= 10 and network.costs[-10] - network.costs[-1] < tolerance):
                    break

            costs[label] = network.costs
            model.append((label, layers))

        return model, costs
    
    @staticmethod
    def run_model(model: List[Tuple[str, List[Layer]]], inputs: Matrix) -> List[str]:

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
        OvRClassifier.logger.debug("Grouping data...")

        for idx, label in enumerate(labels):
            if not label in by_label.keys():
                by_label[label] = []

            by_label[label].append(inputs[idx])

        OvRClassifier.logger.debug(f"Created {len(by_label)} groups")
        return by_label

    @staticmethod
    def balance_training_data(inputs: Dict[str, List[List[float]]]) -> Dict[str, List[List[float]]]:
        min_sample_count = min([len(samples) for samples in inputs.values()])
        OvRClassifier.logger.debug(f"Balancing data with mallest samples size: {min_sample_count}")
        
        return {
            k:random.choices(v, k = min_sample_count) for k, v in inputs.items()
        }


    @staticmethod
    def distribute_training_data(inputs: Matrix, labels: List[str], proportion: float) -> Dict[str, Tuple[Matrix, Matrix]]:
        inputsT = inputs.rtocol()
        gouped_by_label = OvRClassifier.group_by_label(inputsT, labels)

        min_sample_count = min([len(samples) for samples in gouped_by_label.values()])
        OvRClassifier.logger.debug(f"Smallest samples size: {min_sample_count}")
        # samples_count = min_sample_count #min(min_sample_count, 0 if samples_count == None else samples_count)
        # OvRClassifier.logger.debug(f"Sample count: {samples_count} [min samples size: {min_sample_count}, samples_count: {samples_count}]")

        distributed_data: Dict[str, Tuple[List[List[float]], List[int]]] = {}

        for label in gouped_by_label:
            OvRClassifier.logger.debug(f"Generating data for: {label}")
            rgbs = random.choices(gouped_by_label[label], k = min_sample_count)
            OvRClassifier.logger.debug(f"Got {len(rgbs)} positive samples out of {len(gouped_by_label[label])}")

            mask = [1] * len(rgbs)

            other_data: List[List[float]]= []
            for other_label in [l for l in gouped_by_label if l != label]:
                other_data.extend(gouped_by_label[other_label])

            proportion_amount = int(len(rgbs) * proportion)
            negative_samples = random.choices(other_data, k=proportion_amount)
            OvRClassifier.logger.debug(f"Got {len(negative_samples)} negative samples out of {len(other_data)} [proportion: {proportion}]")

            rgbs.extend(negative_samples)
            mask.extend([0] * proportion_amount)

            rgbs_shuffled: List[List[float]] = []
            mask_shuffled: List[int] = []

            OvRClassifier.logger.debug(f"Shuffling {len(rgbs)} samples")
            indices = list(range(len(rgbs)))
            random.shuffle(indices)
            for idx in indices:
                rgbs_shuffled.append(rgbs[idx])
                mask_shuffled.append(mask[idx])

            distributed_data[label] = (rgbs_shuffled, mask_shuffled)

        return {
            label: (Matrix(data[0]).rtocol(), Matrix([data[1]]))
            for label, data in distributed_data.items()
        }
