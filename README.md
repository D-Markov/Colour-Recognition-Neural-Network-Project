# Colour-Recognition-Neural-Network-Project

To download the solution:

```
git clone https://github.com/D-Markov/Colour-Recognition-Neural-Network-Project.git <target folder>
```

To install prerequisites execute:

```
python -m pip install -r requirements.txt
```

>A c compiler is required inorder to build a Cython module. For windows you could use [Microsoft Build Tools for Visual Studio 2019](https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2019)

Build the Cython module
```
python ./src/setup.py build_ext --inplace
```

To run the tests:

```
python -m unittest discover -v -p "*_test.py" -s tests
```

To run coverage:
```
coverage run --source=./src --omit=*__init__.py -m unittest discover tests/ -p *_test.py
coverage html
```
