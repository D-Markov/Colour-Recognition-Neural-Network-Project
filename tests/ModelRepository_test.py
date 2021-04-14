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
        
        self.layers = [
            Layer.create(5, 5, 1, "sigmoid", "sigmoid_prime"),
            Layer.create(5, 5, 1, "sigmoid", "sigmoid_prime")
        ]
        
        self.repo = ModelRepository(self.rootPath)

    
    def test_store_layers(self):
        self.repo.write([("name", self.layers)])
        self.assertTrue(os.path.isfile(fr"{self.rootPath}\model.pkl"))

    def test_read_layers(self):
        self.repo.write([("name", self.layers)])
        read_layers = self.repo.read()[0][1]
        self.assertEqual(len(self.layers), len(read_layers))
        self.assertMatrixAreEqual(self.layers[0].weights, read_layers[0].weights)
        self.assertMatrixAreEqual(self.layers[0].biases, read_layers[0].biases)
        self.assertEqual(self.layers[0].a, read_layers[0].a)
        self.assertEqual(self.layers[0].a_prime, read_layers[0].a_prime)

    def test_error_writing_when_the_file_exists(self):
        self.repo.write([("name", self.layers)])
        self.assertRaises(OSError, self.repo.write, self.layers)

    def test_remove(self):
        self.repo.write([("name", self.layers)])
        self.repo.remove()
        self.assertFalse(os.path.exists(self.rootPath))


    def tearDown(self) -> None:
        shutil.rmtree(self.rootPath, ignore_errors=True)