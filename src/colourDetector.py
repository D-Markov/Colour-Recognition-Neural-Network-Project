from PIL import Image
from .TrainingData.TrainDataGenerator import TrainDataGenerator, ColorRange
from .IO.TrainingDataRepository import TrainingDataRepository
import random


colour_Range = [
    ColorRange(40, "red"), ColorRange(100, "pink"), ColorRange(300, "blue"),
    ColorRange(460, "white"), ColorRange(520, "light green"), ColorRange(600, "green"),
    ColorRange(840, "yellow"), ColorRange(910, "orange"), ColorRange(979, "light red")]

image: Image.Image = Image.open(r"TrainingData\Colour_Gradient.jpg")
tdGenerator = TrainDataGenerator(image)
sampleSize = 900
random_x = [int(random.uniform(0, image.size[0] - 1)) for _ in range(sampleSize)]

store = TrainingDataRepository(r"TrainingData\training.txt")

rgb_Vals = tdGenerator.create_data(random_x, colour_Range)

header = ['R','G','B'] + [ v[1] for v in colour_Range]

store.write(rgb_Vals, header)
# rgb_Vals = store.read()

# print(rgb_Vals)
# rgb_Vals1 = []

# for t in rgb_Vals:
#     rgb_Vals1.append(t[1])
    
# print(rgb_Vals1)


# print(rgb_Vals1.count("red"), rgb_Vals1.count("pink"), rgb_Vals1.count("blue"), rgb_Vals1.count("white"), rgb_Vals1.count("light green"), rgb_Vals1.count("green"), rgb_Vals1.count("yellow"), rgb_Vals1.count("orange"), rgb_Vals1.count("light red"))



