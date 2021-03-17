from typing import List, Union
from os import path
from shutil import rmtree
import pickle
import csv
import logging
from ..Model.Layer import Layer

class ModelRepository:
    __logger = logging.getLogger('ModelRepository')
    __file_name = "model.pkl"

    def __init__(self, folder_name: str):
        self.__folder_name = folder_name
    
    def write(self, layers: Union[List[Layer], List[List[Layer]]]) -> None:
        fullpath = path.join(self.__folder_name, ModelRepository.__file_name)
        self.__logger.debug(f"Writing Model to {fullpath}")

        with open(fullpath, 'xb') as file:
            pickle.dump(layers, file)


    def read(self) -> Union[List[Layer], List[List[Layer]]]:
        fullpath = path.join(self.__folder_name, ModelRepository.__file_name)
        self.__logger.debug(f"Reading Model from {fullpath}")

        with open(fullpath, 'rb') as file:
            return pickle.load(file)


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


    def write_costs(self, costs: Union[List[float], List[List[float]]]):

        l = costs if isinstance(costs[0], list) else [costs]
        for i in range(len(l)):
            with open(fr'{self.__folder_name}\costs-{i}.csv', 'x') as f:
                f.write("\n".join([str(x) for x in l[i]]))


    def remove(self) -> None:
        rmtree(self.__folder_name)