import data_loader as data_loader
from clarin_api_wrapper.wcrft2_wrapper import Wcrft2Wrapper
from tokenizer.tokenizer import Tokenizer


def print_analysis(analysis):
    for element in analysis:
        print(element)


def main():
    wcrft2 = Wcrft2Wrapper()
    sentence = 'Ala ma kota. Kot ma Alę. Tomek to ich dobry przyjaciel.'
    analysed = wcrft2.analyse(sentence)
    print(type(analysed))
    print(analysed)
    print()


if __name__ == '__main__':
    main()
