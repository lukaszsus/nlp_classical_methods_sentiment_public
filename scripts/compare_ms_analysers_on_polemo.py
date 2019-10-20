import data_loader
from clarin_api_wrapper.wcrft2_wrapper import Wcrft2Wrapper
from clarin_api_wrapper.morphodita_wrapper import MorphoditaWrapper


def main():
    file_path = "/dataset_conll/all.sentence.test.txt"
    dataset = data_loader.load_polemo_file(file_path)
    wcrft2 = Wcrft2Wrapper()
    morphodita = MorphoditaWrapper()
    print("===========WCRFT2")
    print(wcrft2.analyse(dataset))
    print("\n\n\n\n\n")
    print("===========MorphoDita")
    print(morphodita.analyse(dataset))


if __name__ == '__main__':
    main()
