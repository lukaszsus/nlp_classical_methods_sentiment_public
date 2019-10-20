from clarin_api_wrapper.morphodita_wrapper import MorphoditaWrapper


def print_analysis(analysis):
    for element in analysis:
        print(element)


def main():
    morphodita = MorphoditaWrapper()
    sentence = 'Ala ma kota. Kot ma Alę. Tomek to ich dobry przyjaciel.'
    analysed = morphodita.analyse(sentence)
    print(type(analysed))
    print(analysed)
    print()


if __name__ == '__main__':
    main()
