import os, shutil
from src.Model.Layer import Layer
from src.IO.ModelRepository import ModelRepository
from MatrixTestCase import MatrixTestCase


class TestModelRepository(MatrixTestCase):
    def setUp(self):
        self.rootPath = r"tests\tmp"
        
        if(os.path.isdir(self.rootPath)):
           shutil.rmtree(self.rootPath)

        os.mkdir(self.rootPath)
        
        self.layers = [Layer(5, 5, "sigmoid", "sigmoid_prime"), Layer(5, 5, "sigmoid", "sigmoid_prime")]
        self.filename = "ModelRepository.pkl"
        self.q = ModelRepository(self.rootPath)

    
    def test_store_layers(self):
        self.q.write(self.filename, self.layers)
        self.assertTrue(os.path.isfile(fr"{self.rootPath}\ModelRepository.pkl"))

    def test_read_layers(self):
        self.q.write(self.filename, self.layers)
        read_layers = self.q.read(self.filename)
        self.assertEqual(len(self.layers), len(read_layers))
        self.assertMatrixAreEqual(self.layers[0].weights, read_layers[0].weights)
        self.assertMatrixAreEqual(self.layers[0].biases, read_layers[0].biases)
        self.assertEqual(self.layers[0].a, read_layers[0].a)
        self.assertEqual(self.layers[0].a_prime, read_layers[0].a_prime)

        
    def tearDown(self) -> None:
        shutil.rmtree(self.rootPath)