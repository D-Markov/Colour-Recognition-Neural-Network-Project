# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false
from typing import List
import unittest
from parameterized import parameterized
from src.TrainingData.DefaultHscSelector import DefaultHscSelector
from src.TrainingData.TrainDataGenerator import TrainDataGenerator, ColourRange

class TrainDataGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.ranges = [
            ColourRange("red", 350, 10),
            ColourRange("green", 120, 140),
            ColourRange("blue", 220, 240)
            ]

        self.sut = TrainDataGenerator(1, DefaultHscSelector())

    @parameterized.expand([
        ("step of one", 0, 5, 1, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]),
        ("step of 2", 0, 5, 0.5, [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]),
        ("step of 4", 0, 2, 0.25, [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]),
        ("cycle with step of 1", 355, 10, 1, [355.0, 356.0, 357.0, 358.0, 359.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    ])
    def test_hue_generation(self, name: str, start: int, count: int, step: int, expected: List[float]):
        result = TrainDataGenerator.get_hue_values(start, count, step)
        self.assertSequenceEqual(expected, result)

    def test_creates_correct_number_of_random_colours(self):
        result = self.sut.get_random_colours(self.ranges)

        self.assertEquals(63, len(result))

if __name__ == '__main__':
    unittest.main()