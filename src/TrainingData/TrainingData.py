from typing import NamedTuple, Tuple, NewType

Rgb = NewType('Rgb', Tuple[int, int, int])

class ColourRange(NamedTuple):
    colour_name: str
    hue_from: int
    hue_to: int

class TrainingRow(NamedTuple):
    rgb: Rgb
    label: str

