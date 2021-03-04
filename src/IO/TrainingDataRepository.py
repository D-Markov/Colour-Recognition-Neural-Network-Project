from src.TrainingData.TrainingData import TrainingData, TrainingRow
import csv
from os import path, mkdir

class TrainingDataRepository:
    def __init__(self, folder: str):
        if not path.isdir(folder):
            raise ValueError(f"Folder '{folder}' does not exist")

        self.__folder = folder

    def __get_file_path(self, name: str):
        return path.join(self.__folder, f"{name}.csv")

    def write(self, data: TrainingData, name: str) -> None:
        filepath = self.__get_file_path(name)
        with open(filepath, "x", newline='') as training_Data:
            writer = csv.writer(training_Data)
            writer.writerow(['R','G','B'] + data.field_names)
            for row in data.data:
                writer.writerow(list(row.rgb) + row.labels)

    
    def read(self, name: str) -> TrainingData:
        filepath = self.__get_file_path(name)
        with open(filepath, 'r') as training:
            reader = csv.reader(training)
            fieldnames = next(reader)

            rows = [TrainingRow(tuple([int(i) for i in row[:3]]), [int(i) for i in row[3:]]) for row in reader]

            return TrainingData(fieldnames, rows)

data_folder_name = "TrainingData"
if not path.isdir(data_folder_name):
    mkdir(data_folder_name)
    
trainingDataRepository = TrainingDataRepository("TrainingData")
