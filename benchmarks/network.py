import sys
from os import getcwd, path
sys.path.append(getcwd())

import cProfile
import pstats
import timeit

import argparse
from pathlib import Path
from array import array
from datetime import datetime
import random
import math

from src.Mathematics.Matrix import Matrix
from src.Model.Layer import Layer
from src.Mathematics.Model_Calculations import cost, error_prime
from src.Model.Network import Network

def get_output_file_name(tag: str) -> str:
    p = Path(__file__)
    file_name = f'{p.stem}-{tag}'
    return path.join(p.parent, file_name)

profiler = cProfile.Profile()

imagesM = Matrix.randomMatrix(12288, 209)
labels = Matrix([array('f',[ random.choice([0, 1]) for _ in range(209) ])])
layers = [
    Layer.create(imagesM.rows, 5, math.sqrt(imagesM.rows), 'sigmoid', 'sigmoid_prime'),
    Layer.create(5, 1, math.sqrt(5), 'sigmoid', 'sigmoid_prime'),
    Layer.create(1, 1, math.sqrt(1), 'sigmoid', 'sigmoid_prime')
]
nn = Network(layers)

def doProfile(tag: str) -> None:
    profiler.enable()
    for i in range(1):
        nn.train(imagesM, labels, cost, error_prime, 0.005)
    profiler.disable()

    profile_file_name = get_output_file_name(tag)
    profiler.dump_stats(f"{profile_file_name}.prof")
    with open(f"{profile_file_name}.txt", "w") as f:
        ps = pstats.Stats(profiler, stream=f).strip_dirs()
        ps.print_stats()

    profiler.print_stats()

def doTimeit(repeat: int):
    t = timeit.Timer(lambda: nn.train(imagesM, labels, cost, error_prime, 0.005))
    res = t.repeat(repeat=repeat, number=1)
    print(f"Min: {min(res)} Max: {max(res)} Avg: {sum(res)/len(res)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Network performance tests.')
    parser.add_argument('--profile', help="runs cProfile", type=str, nargs='?', const=datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    parser.add_argument('--timeit', help="runs timeit 10 times", type=int, nargs='?', const=10)

    args = parser.parse_args()
    if not any([args.profile, args.timeit]):
        parser.error('No arguments provided.')

    if args.profile:
        print('Profiling...')
        doProfile(args.profile)
    if args.timeit:
        print(f'Timing {args.timeit} times...')
        doTimeit(args.timeit)

# To generate html with flame graph: from the project root run:
# python .\flameprof.py  <name.prof> > <name.html>