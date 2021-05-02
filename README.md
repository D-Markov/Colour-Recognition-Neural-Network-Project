# Colour-Recognition-Neural-Network-Project

To download the solution:

```
git clone https://github.com/D-Markov/Colour-Recognition-Neural-Network-Project.git <target folder>
```

To install prerequisites execute:

```
python -m pip install -r requrements.txt
```

To run the tests:

```
python -m unittest discover -v -p "*_test.py" -s tests
```

To run the app:

```
python -m src.ColourRecognition
```

the app will generate a random set of weights and biases that will be saved in the `.tmp` folder with *pre-train* prefixed csv files. It will then run 20 loops to train the model and save the updated weights and biases to the `.tmp` folder with *post-train* prefixed csv files. It will also save the results of the *cost* function for each loop to the `.tmp\costs.csv` file.

>At the moment the number of the loops is set to 20 to reduce the runtime but still produce a noticable change in the trained model.

to run test:
`python -m unittest discover test/ -p *_test.py`
to run covarage:
```
coverage run --source=./src --omit=*__init__.py -m unittest discover tests/ -p *_test.py
coverage html
```
