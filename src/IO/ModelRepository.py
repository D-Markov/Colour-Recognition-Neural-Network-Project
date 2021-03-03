from typing import List
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
    
    def write(self, layers: List[Layer]) -> None:
        fullpath = path.join(self.__folder_name, ModelRepository.__file_name)
        self.__logger.debug(f"Writing Model to {fullpath}")

        with open(fullpath, 'xb') as file:
            pickle.dump(layers, file)


    def read(self) -> List[Layer]:
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
    
    def remove(self) -> None:
        rmtree(self.__folder_name)