from data_loader import load_polemo_file, load_polemo_no_segm_file
from clarin_api_wrapper.wcrft2_wrapper import Wcrft2Wrapper
from clarin_api_wrapper.morphodita_wrapper import MorphoditaWrapper
from clarin_api_wrapper.krnnt_api_wrapper import KRNNTWrapper
import pandas as pd
import numpy as np
from settings import PATH_TO_DATA
import json

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def main():
    data = load_polemo_no_segm_file("plemo2.0-no-segm.txt")
    x_data, y_data = data.values[:, 0], data.values[:, 1]
    print(data.shape)
    tagger_wrapper = KRNNTWrapper()
    results = []

    for i in batch(range(0, x_data.shape[0]), 500):
        result = tagger_wrapper.analyse(" EOF ".join(list(x_data[i])) + " EOF ")
        print(len(results))
        results.extend(result)

    print(results)
    #
    # print(len(results))
    # results_df = pd.DataFrame(data=np.array([results, y_data]).transpose())
    # results_df.to_csv(f"{PATH_TO_DATA}/taggers_output/morphodita/plemo_no_segm_data.csv")

    with open(f"{PATH_TO_DATA}/taggers_output/krnnt/plemo_no_segm_data.json", 'w') as outfile:
        json.dump(results, outfile)


if __name__ == '__main__':
    main()
