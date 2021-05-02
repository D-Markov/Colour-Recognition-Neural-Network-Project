# pyright: reportMissingTypeStubs=false
from PIL import Image
import argparse, io
from .IO.ModelRepositoryFactory import model_data_repo_factory
import matplotlib.pyplot as plt

def show_costs(model_name: str) -> None:
    repo = model_data_repo_factory.get_repo(model_name)
    data = repo.read_costs()

    plt.figure(figsize=(1280/92, 720/92), dpi=92)
    
    for label, d in data.items():
        plt.plot(range(len(d)), d, color=label, label=label)

    plt.xlabel("Epochs")
    plt.ylabel("Cost")
    plt.title(f"Learning progress for model: {model_name}")
    plt.legend()

    io_buf = io.BytesIO()
    plt.savefig(io_buf, format="png")
    io_buf.seek(0)
    image = Image.open(io_buf)
    image.show()    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train Neural Network')
    
    parser.add_argument("name", help="Training data name", type=str)

    args = parser.parse_args()

    show_costs(args.name)