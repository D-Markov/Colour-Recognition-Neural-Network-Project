from unittest import TestCase
import os, shutil
from src.IO.ModelRepositoryFactory import ModelRepositoryFactory

class TestModelRepository(TestCase):
    def setUp(self):
        self.rootPath = r"tests\tmp"

        if(os.path.isdir(self.rootPath)):
           shutil.rmtree(self.rootPath)

        os.mkdir(self.rootPath)

        self.repoFactory = ModelRepositoryFactory(self.rootPath)


    def test_create_non_existing(self):
        self.assertIsNotNone(self.repoFactory.create_repo("test"))
        self.assertTrue(os.path.exists(os.path.join(self.rootPath, "test")))


    def test_create_errors_on_existing(self):
        self.repoFactory.create_repo("test")
        self.assertRaises(ValueError, lambda: self.repoFactory.create_repo("test"))


    def test_get_returns_existing(self):
        self.repoFactory.create_repo("test")
        self.assertIsNotNone(self.repoFactory.get_repo("test"))
        

    def test_get_errors_on_non_existing(self):
        self.assertRaises(ValueError, lambda: self.repoFactory.get_repo("test"))


    def tearDown(self) -> None:
        shutil.rmtree(self.rootPath)