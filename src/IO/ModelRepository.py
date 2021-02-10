from typing import List
from os import path
import pickle
import logging
from ..Model.Layer import Layer

class ModelRepository:
    __logger = logging.getLogger('ModelRepository')

    def __init__(self, folder_name: str):
        self.folder_name = folder_name
    
    def write(self, filename: str, layers: List[Layer]) -> None:
        fullpath = path.join(self.folder_name, filename)
        self.__logger.debug(f"Writing Model to {fullpath}")

        with open(fullpath, 'wb') as file:
            pickle.dump(layers, file)


    def read(self, filename: str) -> List[Layer]:
        fullpath = path.join(self.folder_name, filename)
        self.__logger.debug(f"Reading Model from {fullpath}")

        with open(fullpath, 'rb') as file:
            return pickle.load(file)
            