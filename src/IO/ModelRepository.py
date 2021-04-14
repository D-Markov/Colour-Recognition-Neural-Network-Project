from typing import Dict, List, Any, Tuple
from os import path
from shutil import rmtree
import pickle
import csv, json
import logging
from ..Model.Layer import Layer

class ModelRepository:
    __logger = logging.getLogger('ModelRepository')
    __file_name = "model.pkl"

    def __init__(self, folder_name: str):
        self.__folder_name = folder_name
    
    def write(self, layers: List[Tuple[str, List[Layer]]]) -> None:
        fullpath = path.join(self.__folder_name, ModelRepository.__file_name)
        self.__logger.debug(f"Writing Model to {fullpath}")

        with open(fullpath, 'xb') as file:
            pickle.dump(layers, file)


    def read(self) -> List[Tuple[str, List[Layer]]]:
        fullpath = path.join(self.__folder_name, ModelRepository.__file_name)
        self.__logger.debug(f"Reading Model from {fullpath}")

        with open(fullpath, 'rb') as file:
            return pickle.load(file)


    def read_metadate(self) -> Dict[str, str]:
        fullpath = path.join(self.__folder_name, ModelRepository.__file_name)
        self.__logger.debug(f"Reading metadata from {fullpath}")

        with open(fullpath, 'rb') as file:
            return json.load(file)

    def export_to_csv(self, layers: List[Layer], tag: str):
        for i, layer in enumerate(layers):
            with open(fr'{self.__folder_name}\layer{i}-weights-{tag}.csv','x') as f:
                writer = csv.writer(f)
                for row in layer.weights:
                    writer.writerow(row)

            with open(fr'{self.__folder_name}\layer{i}-biases-{tag}.csv','x') as f:
                writer = csv.writer(f)
                for row in layer.biases:
                    writer.writerow(row)


    def write_costs(self, costs: Dict[str, List[float]]):

        for label, cost in costs.items():
            with open(fr'{self.__folder_name}\{label}-costs.csv', 'x') as f:
                f.write("\n".join([str(value) for value in cost]))

    def write_model_parameters(self, metadata: Dict[str, Any]):

        with open(fr'{self.__folder_name}\metadata.json', 'x') as f:
            json.dump(metadata, f, indent=4)


    def remove(self) -> None:
        rmtree(self.__folder_name)