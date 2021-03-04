from src.TrainingData.TrainingData import TrainingData, TrainingRow
from typing import List, NamedTuple, Tuple
from PIL.Image import Image

class ColorRange(NamedTuple):
    max: int
    colourName: str

class TrainDataGenerator:
    def __init__(self, image: Image):
        self.image = image

    @staticmethod
    def get_colour_pos(colour_ranges: List[ColorRange], colour:str):
        res = [idx for idx, v in enumerate(colour_ranges) if v[1] == colour]

        return res[0] if len(res) else -1


    def create_data(self, x_pos: List[int], colours_map: List[ColorRange]) -> TrainingData:
        if min(x_pos) < 0 or max(x_pos) > self.image.size[0] -1 :
            raise ValueError(f"x-coordinate outside of image size of {self.image.size[0]}")

        colour_x_coordinates = [m.max for m in colours_map]
        
        if min(colour_x_coordinates) < 0 or max(colour_x_coordinates) > self.image.size[0] - 1:
            raise ValueError(f"colour map x-coordinate outside of image size of {self.image.size[0]}")
        
        template = [0] * len(colours_map)
        rows: List[TrainingRow] = []
        for x in x_pos:
            colour = self.get_colour_name(colours_map, x)
            colour_pos = TrainDataGenerator.get_colour_pos(colours_map, colour)
            new_row_labels = template.copy()
            new_row_labels[colour_pos] = 1
            rgb = self.get_RGB(x, 0)
            rows.append(TrainingRow(rgb, new_row_labels))

        colour_names = [ v.colourName for v in colours_map ]
        return TrainingData(colour_names, rows)

    def get_RGB(self, x: int, y: int) -> Tuple[int, int, int]:
        return self.image.getpixel((x, y))[0:3]

    @staticmethod
    def get_colour_name(colours: List[ColorRange], x: int) -> str:
        count = 0
        
        while x - colours[count].max > 0:
            count += 1
        
        return colours[count].colourName
