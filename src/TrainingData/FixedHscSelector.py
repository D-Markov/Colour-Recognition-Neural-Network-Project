from typing import List, Tuple
class FixedHscSelector:

    def __init__(self, svs: List[Tuple[float, float]]):
        self.svs = svs

    def get_hsvs(self, base_hue:float) -> List[Tuple[float, float, float]]:
        
        return [ (base_hue, s, v) for s, v in self.svs ]



