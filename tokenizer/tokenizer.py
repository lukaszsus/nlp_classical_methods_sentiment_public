import re

PUNCTUATION = [
        (re.compile(r'([:,])([^\d])'), r' \1 '),
        (re.compile(r'([:,])$'), r' \1 '),
        (re.compile(r'\.\.\.'), r' ... '),
        (re.compile(r'[;@#$%&]'), r' \g<0> '),
        (
            re.compile(r'([^\.])(\.)([\]\)}>"\']*)\s*$'),
            r'\1 \2\3 ',
        ),  # Handles the final period.
        (re.compile(r'[?!]'), r' \g<0> '),
        (re.compile(r"([^'])' "), r"\1 ' "),
    ]


class Tokenizer(object):
    def __init__(self):
        super(Tokenizer, self).__init__()

    def tokenize(self, data):
        for text in data:
            for regexp, substitution in PUNCTUATION:
                text = regexp.sub(substitution, text)

            tokenized = self.white_spece_tokenizer(text)
            print(tokenized)

    def white_spece_tokenizer(self, string):
        return string.split(" ")