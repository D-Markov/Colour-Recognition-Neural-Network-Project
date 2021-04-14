from typing import List, Tuple
from src.TrainingData.TrainingData import Rgb, TrainingRow
import csv, time
from os import path, mkdir, listdir
from pathlib import Path

class TrainingDataRepository:
    def __init__(self, folder: str):
        if not path.isdir(folder):
            raise ValueError(f"Folder '{folder}' does not exist")

        self.__folder = folder

    def __get_file_path(self, name: str):
        return path.join(self.__folder, f"{name}.csv")

    def write(self, data: List[TrainingRow], name: str, override: bool = False) -> None:
        filepath = self.__get_file_path(name)
        mode = "w" if override else "x"
        
        with open(filepath, mode, newline='') as training_Data:
            writer = csv.writer(training_Data)
            writer.writerow(['R','G','B','label'])
            for row in data:
                writer.writerow([str(row.rgb[0]), str(row.rgb[1]), str(row.rgb[2])] + [row.label])

 
    def read(self, name: str) -> List[TrainingRow]:
        filepath = self.__get_file_path(name)
        with open(filepath, 'r') as training:
            reader = csv.reader(training)
            next(reader)

            return [ TrainingRow(Rgb((int(r), int(g), int(b))), label) for r, g, b, label in reader]

    def list(self) -> List[Tuple[str, str]]:
        return [ 
           (time.ctime(path.getctime(path.join(self.__folder, n))), Path(n).stem) for n in listdir(self.__folder)
        ]


data_folder_name = "TrainingData"
if not path.isdir(data_folder_name):
    mkdir(data_folder_name)
    
trainingDataRepository = TrainingDataRepository("TrainingData")
