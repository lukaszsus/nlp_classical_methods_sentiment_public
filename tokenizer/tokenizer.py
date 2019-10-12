import re

# \1 - first group found in regex
# \g<0> - recursion in regex
PUNCTUATION = [
        (re.compile(r'([:,])([^\d])'), r' \1 '),    # : or , sticked to word after it (allows float numbers)
        (re.compile(r'([:,])$'), r' \1 '),          # : or , in the end of sentence
        (re.compile(r'\.\.\.'), r' ... '),          # ...
        (re.compile(r'[;#$%&]'), r' \g<0> '),      # strange characters, '@' removed for e-mail
        (
            re.compile(r'([^\.])(\.)([\]\)}>"\']*)\s*$'),
            r'\1 \2\3 ',
        ),  # Handles the final period. Not sure if we want that.
        (re.compile(r'[?!]'), r' \g<0> '),          # imo unnecessary
        (re.compile(r"([^'])' "), r"\1 ' "),        # probably handling '"
        (re.compile(r"([„'”])"), r" \1 "),               # '
        (re.compile(r'(")'), r' " ')                # "
    ]

END_OF_SENTENCE = " END_OF_SENTENCE"

END_CHARS = [
    (re.compile(r'([^.])([.][\s]+)'), r"\1" + END_OF_SENTENCE),       # 'p.n.e.' will not finish sentence
    (re.compile(r'(\.{3})([\s]+)'), r"\1" + END_OF_SENTENCE),         # '...' usually finishes sentence in Polish
    (re.compile(r'([?]\s+)'), END_OF_SENTENCE),
    (re.compile(r'([!]\s+)'), END_OF_SENTENCE),
]

#TODO Handle sentence 'Zakończenie skrótem r.?'

class Tokenizer(object):
    def __init__(self):
        super(Tokenizer, self).__init__()

    def tokenize(self, data) -> list:
        output = list()
        for text in data:
            sentences = self.get_sentences(text)
            sentences = [sentence for sentence in sentences if sentence!=""]
            for sentence in sentences:
                output.append(self.tokenize_sentence(sentence))
        return output

    def get_sentences(self, text):
        for regexp, substitution in END_CHARS:
            text = regexp.sub(substitution, text)

        return text.split(END_OF_SENTENCE)

    def tokenize_sentence(self, sentence):
        for regexp, substitution in PUNCTUATION:
            sentence = regexp.sub(substitution, sentence)

        tokenized = self.white_space_tokenizer(sentence)
        tokenized = [word.replace(" ", "") for word in tokenized if word != ""]
        tokenized = self.__correct_ending_shortcut(tokenized)
        return tokenized

    def white_space_tokenizer(self, string):
        return string.split(" ")

    def __correct_ending_shortcut(self, words: list):
        if len(words) > 0:
            last_word: str = words[-1]
            if len(last_word) > 1:
                last_word = re.sub(r'(\.[^.])$', r"\1.", last_word)
            else:
                last_word = re.sub(r'(\w)$', r"\1.", last_word)     # sentence finished with one letter shortcut
            words[-1] = last_word
            return words