import data_loader as data_loader
from clarin_api_wrapper.morfeusz_wrapper import MorfeuszWrapperLexeme
from tokenizer.tokenizer import Tokenizer


def print_analysis(analysis):
    for element in analysis:
        print(element)


def main():
    dataset = data_loader.load_text_file("data_2.txt")
    tokenizer = Tokenizer()
    separated = tokenizer.tokenize([dataset])
    morfeusz = MorfeuszWrapperLexeme()
    for sentence in separated:
        analysed = morfeusz.analyse(sentence)
        for word, analysis in analysed.items():
            print("{}:".format(word))
            print_analysis(analysis)
        print()


if __name__ == '__main__':
    main()
