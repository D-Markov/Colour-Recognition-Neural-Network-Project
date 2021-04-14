from typing import List, Any
from src.TrainingData.DefaultHscSelector import DefaultHscSelector
from src.TrainingData.TrainingData import TrainingRow, Rgb, ColourRange
import itertools
from colorsys import hsv_to_rgb

class TrainDataGenerator:
    def __init__(self, steps_per_hue: int, hscSelector: Any = DefaultHscSelector()):
        self.hscSelector = hscSelector
        self.steps_per_hue = steps_per_hue

    @staticmethod
    def get_rgb_for_hsv(hue: float, s: float, v: float) -> Rgb:
        r, g, b = hsv_to_rgb(hue, s, v)
        return Rgb((int(r * 256), int(g * 256), int(b * 256)))

    @staticmethod
    def get_hue_values(start: int, count: int, step: float = 1) -> List[float]:
        hues: List[float] = []
        major_steps = list(itertools.islice(itertools.cycle(range(360)), start, start + count + 1))
        for hue in major_steps[:-1]:
            for hue_step in [(hue + step * i) for i in range(int(1/step))]:
                hues.append(hue_step)
        
        hues.append(major_steps[-1])
        return hues
        
    def get_random_colours(self, color_ranges: List[ColourRange]) -> List[TrainingRow]:

        colours: List[TrainingRow] = []

        for colour, hue_from, hue_to  in color_ranges:
            hue_count = (hue_to - hue_from) % 360
            rgbs: List[Rgb]= []

            hue_values = list(self.get_hue_values(hue_from, hue_count, 1 / self.steps_per_hue))
            for hue_step in hue_values:
                random_rgbs = [ self.get_rgb_for_hsv(h, s, v) for h, s, v in self.hscSelector.get_hsvs(hue_step / 360) ]
                rgbs.extend(random_rgbs)
            
            unique_rgbs = set(rgbs)
            print(f"{colour}\t\thues:[{hue_from}:{hue_to}, {hue_count}]\trgbs[total: {len(rgbs)}; unique: {len(unique_rgbs)}]")

            colours.extend([TrainingRow(rgb, colour) for rgb in list(unique_rgbs)])

        return colours
