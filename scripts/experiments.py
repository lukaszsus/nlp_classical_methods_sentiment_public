import time
import pandas as pd

from sklearn.metrics import accuracy_score
from clarin_api_wrapper.krnnt_api_wrapper import KRNNTWrapper
from clarin_api_wrapper.morphodita_wrapper import MorphoditaWrapper
from clarin_api_wrapper.wcrft2_wrapper import Wcrft2Wrapper
from data_loader import load_tagger_preprocesses_json_file, load_polemo_no_segm_file, load_train_test_idx_file
from sentiment_model.sentiment_model import SentimentModel
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


def get_tagger_class(name):
    if name == "krnnt":
        return KRNNTWrapper
    if name == "morphodita":
        return MorphoditaWrapper
    if name == "wcrft2":
        return Wcrft2Wrapper

def do_research():
    taggers = ["krnnt", "morphodita", "wcrft2"]
    parts_of_speech = ["verb", "noun", "adj", None]     # None for all parts of speech
    results = pd.DataFrame(columns=["tagger", "part_of_speech", "accuracy", "time"])
    for tagger in taggers:
        for part_of_speech in parts_of_speech:
            acc, time = do_reasearch_for_one_case(tagger, part_of_speech)
            part_of_speech_str = part_of_speech if part_of_speech is not None else "all"
            row = pd.DataFrame([{"tagger": tagger,
                                 "part_of_speech": part_of_speech,
                                 "accuracy": acc,
                                 "time": time}])
            results = results.append(row, ignore_index=True)
            results.to_csv(f"{PATH_TO_DATA}/results/{tagger}-{part_of_speech_str}.csv")

def do_reasearch_for_one_case(tagger, part_of_speech):
    train_data = load_polemo_no_segm_file("plemo2.0-no-segm.txt")
    preprocessed_data = load_tagger_preprocesses_json_file(
        f"{PATH_TO_DATA}/taggers_output/{tagger}/plemo_no_segm_data.json")
    train_idx, test_idx = load_train_test_idx_file(f"{PATH_TO_DATA}/train_test_idx.pkl")
    x_data, y_data = train_data.values[:, 0], train_data.values[:, 1].astype(int)

    x_train, y_train = preprocessed_data[train_idx], y_data[train_idx]
    x_test, y_test = preprocessed_data[test_idx], y_data[test_idx]

    preprocessed_train, preprocessed_test = preprocessed_data[train_idx], preprocessed_data[test_idx]

    model = SentimentModel(tagger_wrapper=Wcrft2Wrapper())

    start = time.time()
    model.fit(preprocessed_train, y_train, part_of_speech=part_of_speech, tagger_preprocessed=True)
    elapsed = time.time() - start
    y_pred = model.predict(preprocessed_test, part_of_speech=part_of_speech, tagger_preprocessed=True)

    acc = accuracy_score(y_test, y_pred)
    part_of_speech_str = part_of_speech if part_of_speech is not None else "all"
    print("Tagger: {} Part of speech: {} Accuracy: {}".format(tagger,
                                                              part_of_speech_str,
                                                              acc))
    return acc, elapsed

if __name__ == '__main__':
    do_research()