from typing import Any
from PIL import Image
import logging, argparse
from src.TrainingData.TrainingData import ColourRange
from src.TrainingData.TrainDataGenerator import TrainDataGenerator
from src.TrainingData.DefaultHscSelector import DefaultHscSelector
from src.TrainingData.FixedHscSelector import FixedHscSelector
from src.TrainingData.RandomHsvSelector import RandomHsvSelector
from src.IO.TrainingDataRepository import trainingDataRepository

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s %(name)s:%(message)s')
logger = logging.getLogger("trainingData")

colour_ranges = [
    ColourRange("red", 350, 10),
    ColourRange("green", 120, 140),
    ColourRange("blue", 220, 240),
    ColourRange("yellow", 50, 60),
    ColourRange("orange", 20, 40),
    ColourRange("pink", 295, 307),
    ColourRange("violet", 270, 274)
]


def gen_trainig_data(selector: Any, steps_per_hue: int, name: str, override: bool, args: argparse.Namespace):
    generator = TrainDataGenerator(steps_per_hue, selector)
    data = generator.get_random_colours(colour_ranges)

    settings = ",".join([f"{a[0]}={a[1]}" for a in vars(args).items() if not a[0] in ["tag", "override", "command"]])
    name = f"{name}-{settings}"
    logger.info(f"Created trainig data: {name} with {len(data)} data points")
    trainingDataRepository.write(data, name, override)


def list_training_data():
    for n in trainingDataRepository.list():
        print(f"{n[0]}\t {n[1]}")


def visualize_training_data(name: str, height: int = 10, save: bool = False):

    data = trainingDataRepository.read(name)
    rgbs = [ d.rgb for d in data ]

    with Image.new("RGB", (len(rgbs), height)) as im:
        im.putdata(rgbs * height)
        
        if(save):
            im.save(f"{name}.png", "PNG")

        im.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Colour Training Data')
    subparser_parser = parser.add_subparsers(dest='command')

    list_parser = subparser_parser.add_parser("list", help="List avalable training data")
    
    visualize_parser = subparser_parser.add_parser("visualize", help="Visualizes training data")
    visualize_parser.add_argument("--height", help="Image height (default is 50)", type=int, default=50)
    visualize_parser.add_argument("--save", help="Saves the generated visualization", action='store_true')
    visualize_parser.add_argument("name", help="Training data name", type=str)

    create_parser = subparser_parser.add_parser("create", help="Generates training data")
    selector_parser = create_parser.add_subparsers(dest="selector")

    fixedHsvSelector_parser = selector_parser.add_parser("FixedHsvSelector", help="Selects fixed s v points from a plane")

    randomHsvSelector_parser=  selector_parser.add_parser("RandomHsvSelector", help="Randomly selects a specified number of s v values within the radius from a plane")
    randomHsvSelector_parser.add_argument("-r", "--radius", help="Radius within which random values should be picked (0 to 1)", type=float, default=.5)
    randomHsvSelector_parser.add_argument("-c", "--count", help="Number of random values to pick", type=int, default=5)

    create_parser.add_argument("tag", help="name prefix", type=str)
    create_parser.add_argument("-s", "--steps_per_hue", help="Number of Steps per hue", type=int, default=1)
    create_parser.add_argument("-o", "--override", help="Override existing data", action='store_true')

    args = parser.parse_args()
    
    if args.command == "create":
        selector = DefaultHscSelector()
        if args.selector == "FixedHscSelector":
            selector = FixedHscSelector([(1,1),(.93,.86),(.86,.93),(.7,.7)])
        elif args.selector == "RandomHsvSelector":
            selector = RandomHsvSelector(args.radius, args.count)

        gen_trainig_data(selector, args.steps_per_hue, args.tag, args.override, args)
    elif args.command == "list":
        list_training_data()
    elif args.command == "visualize":
        visualize_training_data(args.name, args.height, args.save)
