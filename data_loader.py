import numpy as np
import os
import pandas as pd
import re
from settings import PATH_TO_DATA
import json
import pickle

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
    f = open(os.path.join(PATH_TO_DATA, file_path), "r")
    for x in f:
        x = x.replace("\n", "").split("__label__z_")
        dataset.append([x[0], POL_EMO_CLASSES_TO_INDEXES[x[1]]])

    return pd.DataFrame(dataset)


def load_polemo_no_segm_file(file_path):
    dataset = []
    f = open(os.path.join(PATH_TO_DATA, file_path), "r")
    for x in f:
        x = x.replace("\n", "").replace("\t", " ")
        splitted = x.split(" ")
        label = splitted[0].replace("meta_", "")
        sentence = " ".join(splitted[1:])

        dataset.append([sentence, POL_EMO_CLASSES_TO_INDEXES[label]])

    return pd.DataFrame(dataset)


def load_tagger_preprocesses_data_file(file_path):
    return pd.read_csv(file_path, index_col=0)


def load_tagger_preprocesses_json_file(file_path):
    with open(file_path, 'r') as outfile:
        return np.array(json.load(outfile))


def load_train_test_idx_file(file_path):
    pkl_file = open(file_path, 'rb')
    content = pickle.load(pkl_file)
    pkl_file.close()
    return content['train_idx'], content['test_idx']

def load_tagger_output(file_path):
    with open(file_path, 'r') as outfile:
        return np.array(json.load(outfile))