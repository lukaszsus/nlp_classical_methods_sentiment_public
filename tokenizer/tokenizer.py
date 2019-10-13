import re
from user_settings import PROJECT_PATH

# \1 - first group found in regex
# \g<0> - recursion in regex
PUNCTUATION = [
        (re.compile(r'([:,])([^\d])'), r' \1 '),    # : or , sticked to word after it (allows float numbers)
        (re.compile(r'([:,])$'), r' \1 '),          # : or , in the end of sentence
        (re.compile(r'\.\.\.'), r' ... '),          # ...
        (re.compile(r'[;#$%&]'), r' \g<0> '),      # strange characters, '@' removed for e-mail
        (re.compile(r'[?!]'), r' \g<0> '),          # imo unnecessary
        (re.compile(r"([^'])' "), r"\1 ' "),        # probably handling '"
        (re.compile(r"([„'”])"), r" \1 "),               # '
        (re.compile(r'(")'), r' " ')                # "
    ]

END_OF_SENTENCE = " END_OF_SENTENCE"

END_CHARS = [
    # (re.compile(r'([^.])([.][\s]+)'), r"\1." + END_OF_SENTENCE),  # 'p.n.e.' will not finish sentence
    (re.compile(r'(\.{3})([\s]+)'), r"\g<0> " + END_OF_SENTENCE),         # '...' usually finishes sentence in Polish
    (re.compile(r'([?]\s+)'), r"\1 " + END_OF_SENTENCE),
    (re.compile(r'([!]\s+)'), r"\1 " + END_OF_SENTENCE),
    (re.compile(r'((\.) ([A-Z]))'), r" \g<2>" + END_OF_SENTENCE + r" \g<3>"), # new sentence starts with '. [UpperCaseLetter]'
    (re.compile(r'((\.) ((\"|\'|\-)[A-Z]))'), r" \g<2>" + END_OF_SENTENCE + r" \g<3>"),  # new sentence starts with '. [" or ' or -][UpperCaseLetter]'
]

SHORTCUTS_EXCEPTION_FILEPATH = f"{PROJECT_PATH}/tokenizer/shortcuts_exceptions.txt"

SPECIAL_TOKENS_REG_EXPRESSIONS = {
    "date": [
        re.compile(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'),
        re.compile(r'([12]\d{3}.(0[1-9]|1[0-2]).(0[1-9]|[12]\d|3[01]))'),
    ],
    "mail":[
        re.compile(r'([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)'),
    ]

}
#TODO Handle sentence 'Zakończenie skrótem r.?'


class Tokenizer(object):
    def __init__(self):
        super(Tokenizer, self).__init__()
        self.shortcuts_exceptions = self.load_shortucts_exceptions_file()

    def load_shortucts_exceptions_file(self):
        dataset = []
        f = open(f"{SHORTCUTS_EXCEPTION_FILEPATH}", "r")
        for x in f:
            x = x.replace("\r\n", "\n").replace("\n", "")
            dataset.append(x)

        return dataset

    def tokenize(self, data) -> list:
        output = list()
        for text in data:
            text = text.replace("\n", "")
            sentences = self.get_sentences(text)
            sentences = [sentence for sentence in sentences if sentence!=""]
            for sentence in sentences:
                output.append(self.tokenize_sentence(sentence))

        return self.__merge_sentences_by_not_ending_shortcut(output)

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

        [self.check_possible_tokens(tokens) for tokens in tokenized]
        return tokenized

    def check_possible_tokens(self, token):
        possible_tokens = []
        for key, value in SPECIAL_TOKENS_REG_EXPRESSIONS.items():
            for regexp in value:
                if regexp.match(token):
                    possible_tokens.append(key)

        if possible_tokens:
            print(f"{token} possible token types: {possible_tokens}")

    def white_space_tokenizer(self, string):
        return string.split(" ")

    def __merge_sentences_by_not_ending_shortcut(self, sentences):
        last_sentence_last_word = ""
        new_sentences = []
        for sentence in sentences:
            if last_sentence_last_word in self.shortcuts_exceptions:
                new_sentences[-1].extend(sentence)
            else:
                new_sentences.append(sentence)
            last_sentence_last_word = f"{sentence[-2]}{sentence[-1]}"

        return new_sentences

    def __correct_ending_shortcut(self, words: list):
        if len(words) > 0:
            last_word: str = words[-1]
            if len(last_word) > 1:
                last_word = re.sub(r'(\.[^.])$', r"\1 .", last_word)
            else:
                last_word = re.sub(r'(\w)$', r"\1.", last_word)     # sentence finished with one letter shortcut
            words[-1] = last_word
            return words