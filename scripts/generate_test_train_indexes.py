from data_loader import load_polemo_no_segm_file
import numpy as np
import pickle
from settings import PATH_TO_DATA


def main():
    split = 0.8

    train_data = load_polemo_no_segm_file("plemo2.0-no-segm.txt")
    x_train, y_train = train_data.values[:, 0], train_data.values[:, 1].astype(int)

    data_length = x_train.shape[0]
    split_index = int(data_length * split)
    idx = np.arange(0, data_length)
    np.random.shuffle(idx)
    train_idx = idx[:split_index]
    test_idx = idx[split_index:]

    results = {
        "train_idx": train_idx,
        "test_idx": test_idx
    }

    output = open(f'{PATH_TO_DATA}/train_test_idx.pkl', 'wb')
    pickle.dump(results, output)
    output.close()


if __name__ == '__main__':
    main()