import numpy as np
from settings import PATH_TO_DATA


def load_text_file(filename):
    dataset = []
    f = open(f"{PATH_TO_DATA}/{filename}", "r")
    for x in f:
        dataset.append(x.replace("\n", ""))

    return np.array(dataset)