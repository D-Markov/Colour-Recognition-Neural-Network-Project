import sys
from os import getcwd, path
sys.path.append(getcwd())

import cProfile
import pstats

from pathlib import Path
from array import array
from datetime import datetime
import random

from src.Mathematics.Matrix import Matrix
from src.Model.Layer import Layer
from src.Mathematics.Model_Calculations import cost, error_prime
from src.Model.Network import Network

def get_output_file_name():
    p = Path(__file__)
    file_name = f'{p.stem}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
    return path.join(p.parent, file_name)

profiler = cProfile.Profile()

imagesM = Matrix.randomMatrix(12288, 209)
labels = Matrix([array('f',[ random.choice([0, 1]) for _ in range(209) ])])
layers = [
    Layer(imagesM.rows, 5, 'sigmoid', 'sigmoid_prime'),
    Layer(5, 1, 'sigmoid', 'sigmoid_prime'),
    Layer(1, 1, 'sigmoid', 'sigmoid_prime')
]
nn = Network(layers)

profiler.enable()
for i in range(1):
    nn.train(imagesM, labels, cost, error_prime, 0.005)
profiler.disable()

profile_file_name = get_output_file_name()
profiler.dump_stats(f"{profile_file_name}.prof")
with open(f"{profile_file_name}.txt", "w") as f:
    ps = pstats.Stats(profiler, stream=f).strip_dirs()
    ps.print_stats()

profiler.print_stats()

# To generate html with flame graph: from the project root run:
# python .\flameprof.py  <name.prof> > <name.html>