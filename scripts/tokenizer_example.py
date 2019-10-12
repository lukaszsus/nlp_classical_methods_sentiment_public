from tokenizer.tokenizer import Tokenizer
import data_loader as data_loader


def main():
    dataset = data_loader.load_text_file("data_2.txt")
    tokenizer = Tokenizer()
    output = tokenizer.tokenize(dataset)
    for sentence in output:
        print(sentence)


if __name__ == '__main__':
    main()