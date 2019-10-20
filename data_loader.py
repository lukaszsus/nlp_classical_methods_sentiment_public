import numpy as np
import pandas as pd
import re
from settings import PATH_TO_DATA

POL_EMO_CLASSES_TO_INDEXES = {
    'minus_m': 0,
    'minus_s': 1,
    'zero': 2,
    'plus_s': 3,
    'plus_m': 4,
    'amb': 5,
}

POL_EMO_INDEXES_TO_CLASSES = {value: key for key, value in POL_EMO_CLASSES_TO_INDEXES.items()}


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
        x = x.replace("\n", "").split("__label__z_")
        dataset.append([x[0], POL_EMO_CLASSES_TO_INDEXES[x[1]]])

    return pd.DataFrame(dataset)