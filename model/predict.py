import sys
import os
from .model import (
    Model
)

if __name__ == "__main__":
    model = Model()
    path = sys.argv[1]
    if not os.path.exists(path):
        print('Path given doesn\'t exist')
        exit(1)

    breed = model.predict_path(path)
    if breed:
        print(f"breed: {breed}")
    else:
        print("no dog")
