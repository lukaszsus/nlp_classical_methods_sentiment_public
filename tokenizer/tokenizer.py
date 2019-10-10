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

END_OF_SENTENCE = " END_OF_SENTENCE"

END_CHARS = [
    (re.compile(r'([.])'), END_OF_SENTENCE),
    (re.compile(r'([?])'), END_OF_SENTENCE),
    (re.compile(r'([!])'), END_OF_SENTENCE),
]


class Tokenizer(object):
    def __init__(self):
        super(Tokenizer, self).__init__()

    def tokenize(self, data):
        for text in data:
            sentences = self.get_sentences(text)
            sentences = [sentence for sentence in sentences if sentence!=""]
            for sentence in sentences:
                print(self.tokenize_sentence(sentence))


    def get_sentences(self, text):
        for regexp, substitution in END_CHARS:
            text = regexp.sub(substitution, text)

        return text.split(END_OF_SENTENCE)

    def tokenize_sentence(self, sentence):
        for regexp, substitution in PUNCTUATION:
            sentence = regexp.sub(substitution, sentence)

        tokenized = self.white_spece_tokenizer(sentence)
        tokenized = [word.replace(" ", "") for word in tokenized if word != ""]
        return tokenized

    def white_spece_tokenizer(self, string):
        return string.split(" ")