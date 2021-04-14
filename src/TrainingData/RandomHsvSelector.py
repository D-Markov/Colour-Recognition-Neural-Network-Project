from typing import List, Tuple
import random, math

class RandomHsvSelector:
    def __init__(self, radius:float = 0.6, count:int = 5):
        self.radius = radius
        self.count = count
        self.get_random_svs = lambda: [self.get_random_sv(radius) for _ in range(count)]

    def get_hsvs(self, hue: int) -> List[Tuple[float, float, float]]:
        return [ (hue , s, v) for s, v in self.get_random_svs() ]

    @staticmethod
    def get_random_sv(r:float = 0.6) -> Tuple[float, float]:
        r = random.random() * r
        angle = random.random() * math.pi / 2
        s = 1 - r * math.cos(angle)
        v = 1 - r * math.sin(angle)

        return s, v
        