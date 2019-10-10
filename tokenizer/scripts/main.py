from tokenizer.tokenizer import Tokenizer
import data_loader as data_loader


def main():
    dataset = data_loader.load_text_file("data_1.txt")
    tokenizer = Tokenizer()
    tokenizer.tokenize(dataset)


if __name__ == '__main__':
    main()