from typing import List, Tuple

class DefaultHscSelector:
    def __init__(self):
        self.s = 1.0
        self.v = 1.0

    def get_hsvs(self, base_hue:int) -> List[Tuple[float, float, float]]:
        return [(base_hue, self.s, self.v)]