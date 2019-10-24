import numpy as np
import pandas as pd
from data_loader import load_tagger_preprocesses_json_file
from settings import PATH_TO_DATA


def find_idx_with_tag(data, tags):

    idx = []

    for i in range(0, len(data)):
        found = False
        for token in data[i]:
            if any(tag in token['lex']['ctag'] for tag in tags):
                found = True

        if found:
            idx.append(i)

    return idx


def main():
    # wcrtf2_data = load_tagger_preprocesses_json_file(
    #     f"{PATH_TO_DATA}/taggers_output/wcrft2/plemo_no_segm_data.json")

    # morphodita_data = load_tagger_preprocesses_json_file(
    #     f"{PATH_TO_DATA}/taggers_output/morphodita/plemo_no_segm_data.json")
    #
    krnnt_data = load_tagger_preprocesses_json_file(
        f"{PATH_TO_DATA}/taggers_output/krnnt/plemo_no_segm_data.json")

    krnnt_ign_idx = find_idx_with_tag(krnnt_data, ["ign"])
    print(krnnt_ign_idx)


if __name__ == '__main__':
    main()