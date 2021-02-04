import csv

class CsvStore:
    def __init__(self, filename):
        self.__filename = filename

    def write(self, data):
        with open(self.__filename, "w+") as training_Data:
            training_Data.write("R,G,B,Colour Name \n")
            
            for rgb in data:  
                training_Data.write(f"{rgb[0][0]},{rgb[0][1]},{rgb[0][2]},{rgb[1]}\n")


    
    def read(self):
        with open(self.__filename) as training:
            data = csv.reader(training)
            read_Data = []     
            
            for red, green, blue, name in data:
                read_Data.append(((red, green, blue), name))
            
            return(read_Data)
