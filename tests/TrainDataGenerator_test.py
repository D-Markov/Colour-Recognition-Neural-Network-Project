import unittest
from src.TrainingData.TrainDataGenerator import TrainDataGenerator, ColorRange
from PIL import Image

class TrainDataGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.image = Image.open(r"TrainingData\colour_Gradient.jpg")
        self.colour_map = [
            ColorRange(40, "red"), ColorRange(100, "pink"), ColorRange(300, "blue"),
            ColorRange(460, "white"), ColorRange(520, "light green"), ColorRange(600, "green"),
            ColorRange(840, "yellow"), ColorRange(910, "orange"), ColorRange(979, "light red")]
        self.sut = TrainDataGenerator(self.image)
    
    def tearDown(self) -> None:
        self.image.close()

    def test_get_pixel_rgb(self):
        rgb = self.sut.get_RGB(36, 415)
        self.assertEqual(rgb, (254, 66, 101))

    def test_get_colour_name(self):
        results = ["red", "yellow", "blue", "orange", "light green", "light red"]
        x = [28, 680, 240, 900, 509, 950]
        funcResults = []
        for i in range(len(results)):
            funcResults.append((self.sut.get_colour_name(self.colour_map, x[i])))
        self.assertListEqual(funcResults, results)
    
    def test_create_data_for_red(self):
        x_Vals = [0, 22, 40]
        colour_vals = self.sut.create_data(x_Vals, self.colour_map)
        colours = [val.labels[0] for val in colour_vals.data]
        self.assertTrue(all(1 == c for c in colours))

    def test_create_data_for_blue(self):
        x_Vals = [101, 200, 300]
        colour_vals = self.sut.create_data(x_Vals,self.colour_map)
        colours = [val.labels[2] for val in colour_vals.data]
        self.assertTrue(all(1 == c for c in colours))

    def test_create_data_for_light_red(self):
        x_Vals = [911, 930, 979]
        colour_vals = self.sut.create_data(x_Vals, self.colour_map)
        colours = [val.labels[8] for val in colour_vals.data]
        self.assertTrue(all(1 == c for c in colours))     

if __name__ == '__main__':
    unittest.main()