import numpy as np
from settings import PATH_TO_DATA


def load_text_file(filename):
    dataset = []
    f = open(f"{PATH_TO_DATA}/{filename}", "r")
    for x in f:
        x = x.replace("\r\n", "\n").replace("\n", "")
        dataset.append(x)

    return " ".join(dataset)