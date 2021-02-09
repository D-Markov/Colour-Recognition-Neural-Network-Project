from PIL import Image
from .TrainingData.TrainDataGenerator import TrainDataGenerator
from .IO import CsvStore
import random

store = CsvStore(r"..\TrainingData\training.txt")
image = Image.open(r"..\TrainingData\Colour_Gradient.jpg")
colour_Range = [(40, "red"), (100, "pink"), (300, "blue"), (460, "white"), (520, "light green"), (600, "green"), (840, "yellow"), (910, "orange"), (980, "light red")]
sampleSize = 900
random_x = [random.uniform(0, image.size[0]) for i in range(sampleSize)]
tdGenerator = TrainDataGenerator(image)
rgb_Vals = tdGenerator.create_data(random_x, colour_Range)

store.write(rgb_Vals)
rgb_Vals = store.read()

print(rgb_Vals)
rgb_Vals1 = []

for t in rgb_Vals:
    rgb_Vals1.append(t[1])
    
print(rgb_Vals1)


print(rgb_Vals1.count("red"), rgb_Vals1.count("pink"), rgb_Vals1.count("blue"), rgb_Vals1.count("white"), rgb_Vals1.count("light green"), rgb_Vals1.count("green"), rgb_Vals1.count("yellow"), rgb_Vals1.count("orange"), rgb_Vals1.count("light red"))
