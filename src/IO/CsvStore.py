from typing import List, Union
import csv

class CsvStore:
    def __init__(self, filename):
        self.__filename = filename

    def write(self, data: List[List[int]], header:Union[List[str], None] = None) -> None:
        with open(self.__filename, "w", newline='') as training_Data:
            writer = csv.writer(training_Data)
            if(not header == None):
                writer.writerow(header)
            
            writer.writerows(data)

    
    def read(self):
        with open(self.__filename) as training:
            data = csv.reader(training)
            read_Data = []     
            
            for red, green, blue, name in data:
                read_Data.append(((red, green, blue), name))
            
            return(read_Data)
