import unittest
from TrainingData.TrainDataGenerator import TrainDataGenerator
from PIL import Image

class TrainDataGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.image = Image.open("colour_Gradient.jpg")
        self.sut = TrainDataGenerator(self.image)

    def test_get_pixel_rgb(self):
        rgb = self.sut.get_RGB(36, 415)
        self.assertEqual(rgb, (254, 66, 101))

    def test_get_colour_name(self):
        results = ["red", "yellow", "blue", "orange", "light green", "light red"]
        x = [28, 680, 240, 900, 509, 950]
        funcResults = []
        for i in range(len(results)):
            funcResults.append((self.sut.get_colour_name([(40, "red"), (100, "pink"), (300, "blue"), (460, "white"), (520, "light green"), (600, "green"), (840, "yellow"), (910, "orange"), (980, "light red")], x[i])))
        self.assertListEqual(funcResults, results)

if __name__ == '__main__':
    unittest.main()