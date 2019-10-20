import numpy as np
import re
from settings import PATH_TO_DATA


def load_text_file(filename):
    dataset = []
    f = open(f"{PATH_TO_DATA}/{filename}", "r")
    for x in f:
        x = x.replace("\r\n", "\n").replace("\n", "")
        dataset.append(x)

    return " ".join(dataset)


def load_polemo_file(file_path):
    dataset = []
    f = open(f"{PATH_TO_DATA}/{file_path}", "r")
    for x in f:
        x = x.replace("\r\n", "\n").replace("\n", "")
        x = re.sub(r"__label.+$", "", x)
        dataset.append(x)

    return " ".join(dataset)