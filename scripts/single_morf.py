import data_loader as data_loader
from clarin_api_wrapper.morfeusz_wrapper import MorfeuszWrapperLexeme
from tokenizer.tokenizer import Tokenizer


def print_analysis(analysis):
    for element in analysis:
        print(element)


def main():
    text = 'Charakteryzował się on ustawieniem zawodników w kształcie piramidy' \
          ' – bramkarz - 2 obrońców - 3 pomocników - 5 napastników (1-2-3-5).'
    morfeusz = MorfeuszWrapperLexeme()
    tokenizer = Tokenizer()
    text = tokenizer.tokenize([text])
    for sen in text:
        analysed = morfeusz.analyse([w for w, tag in sen], as_xml=False)
        print(analysed)

        analysed = morfeusz.analyse([w for w, tag in sen], as_xml=True)
        print(analysed)
        print()

if __name__ == "__main__":
    main()