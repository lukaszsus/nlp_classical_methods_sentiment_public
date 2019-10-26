from data_loader import load_polemo_no_segm_file, load_tagger_preprocesses_json_file, load_train_test_idx_file
from sentiment_model.sentiment_model import SentimentModel
from clarin_api_wrapper.wcrft2_wrapper import Wcrft2Wrapper
from settings import PATH_TO_DATA
from sklearn.metrics.classification import accuracy_score, recall_score, precision_score, f1_score
import numpy as np


def main():
    train_data = load_polemo_no_segm_file("plemo2.0-no-segm.txt")
    preprocessed_data = load_tagger_preprocesses_json_file(
        f"{PATH_TO_DATA}/taggers_output/krnnt/plemo_no_segm_data.json")
    train_idx, test_idx = load_train_test_idx_file(f"{PATH_TO_DATA}/train_test_idx.pkl")
    x_data, y_data = train_data.values[:, 0], train_data.values[:, 1].astype(int)

    x_train, y_train = preprocessed_data[train_idx], y_data[train_idx]
    x_test, y_test = preprocessed_data[test_idx], y_data[test_idx]

    preprocessed_train, preprocessed_test = preprocessed_data[train_idx], preprocessed_data[test_idx]

    model = SentimentModel(tagger_wrapper=Wcrft2Wrapper())
    model.fit(preprocessed_train, y_train, part_of_speech="verb", tagger_preprocessed=True)
    y_pred = model.predict(preprocessed_test, part_of_speech="verb", tagger_preprocessed=True)

    print(accuracy_score(y_test, y_pred))

    # print(recall_score(y_test, y_pred))
    # print(precision_score(y_test, y_pred))
    # print(f1_score(y_test, y_pred))y_pred


if __name__ == '__main__':
    main()
