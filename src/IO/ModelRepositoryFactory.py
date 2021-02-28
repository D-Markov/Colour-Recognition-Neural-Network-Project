from os import path, mkdir
from .ModelRepository import ModelRepository

class ModelRepositoryFactory():
    def __init__(self, folder_name: str):
        self.root = folder_name

    def create_repo(self, name: str) -> ModelRepository:
        target_path = path.join(self.root, name)
        
        if path.exists(target_path):
            raise ValueError(f"Repository exists")

        mkdir(target_path)
        return ModelRepository(target_path)

    def get_repo(self, name: str) -> ModelRepository:
        target_path = path.join(self.root, name)

        if not path.exists(target_path):
            raise ValueError(f"Repository not found")

        return ModelRepository(target_path)
