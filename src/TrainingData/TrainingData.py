from typing import List, NamedTuple, Tuple

class TrainingRow(NamedTuple):
    rgb: Tuple[int, int, int]
    labels: List[int]

class TrainingData(NamedTuple):
    field_names: List[str]
    data: List[TrainingRow]
