from data_loader import load_polemo_file
from sentiment_model.sentiment_model import SentimentModel
from clarin_api_wrapper.wcrft2_wrapper import Wcrft2Wrapper


def main():
    train_data = load_polemo_file("dataset_conll/hotels.sentence.train.txt")
    dev_data = load_polemo_file("dataset_conll/hotels.sentence.dev.txt")
    test_data = load_polemo_file("dataset_conll/hotels.sentence.test.txt")

    x_train, y_train = train_data.values[:, 0], train_data.values[:, 1]
    x_dev, y_dev = dev_data.values[:, 0], dev_data.values[:, 1]
    x_test, y_test = test_data.values[:, 0], test_data.values[:, 1]

    model = SentimentModel(tagger_wrapper=Wcrft2Wrapper())
    model.fit(x_train[:100], y_train[:100])


if __name__ == '__main__':
    main()
