import re
from user_settings import PROJECT_PATH

DEFAULT_TOKEN = "def."
MAIL_TOKEN = "mail"
DATE_TOKEN = "date"
SHORTCUT_TOKEN = "short."

# \1 - first group found in regex
# \g<0> - recursion in regex
POLISH_UPPER_CASE_LETTERS = "[AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]"

PUNCTUATION = [
        (re.compile(r'([:,])([^\d])'), r' \1 '),    # : or , sticked to word after it (allows float numbers)
        (re.compile(r'([:,])$'), r' \1 '),          # : or , in the end of sentence
        (re.compile(r'([(])'), r' \1 '),          # : handling (
        (re.compile(r'([)])'), r' \1 '),           # : handling )
        (re.compile(r'\.\.\.'), r' ... '),          # ...
        (re.compile(r'[;#$%&]'), r' \g<0> '),      # strange characters, '@' removed for e-mail
        (re.compile(r'[?!]'), r' \g<0> '),          # handling ? and !
        (re.compile(r"([^'])' "), r"\1 ' "),        # probably handling '
        (re.compile(r"([„'”])"), r" \1 "),          # '
        (re.compile(r'(")'), r' " ')                # "
    ]

END_OF_SENTENCE = " END_OF_SENTENCE"

END_CHARS = [
    # (re.compile(r'([^.])([.][\s]+)'), r"\1." + END_OF_SENTENCE),  # 'p.n.e.' will not finish sentence
    (re.compile(r'(\.{3})([\s]+)'), r"\g<0> " + END_OF_SENTENCE),         # '...' usually finishes sentence in Polish
    (re.compile(r'([?]\s+)'), r"\1 " + END_OF_SENTENCE),
    (re.compile(r'([!]\s+)'), r"\1 " + END_OF_SENTENCE),
    (re.compile(r'((\.) ([AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ]))'), r"\g<2>" + END_OF_SENTENCE + r" \g<3>"), # new sentence starts with '. [UpperCaseLetter]'
    (re.compile(r'((\.) (("|\'|-)[AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ]))'), r"\g<2>" + END_OF_SENTENCE + r" \g<3>"),  # new sentence starts with '. [" or ' or -][UpperCaseLetter]'
]

SHORTCUTS_EXCEPTION_FILEPATH = f"{PROJECT_PATH}/tokenizer/named_shortcuts_exceptions.txt"
SHORTCUTS_DICT_FILEPATH = f"{PROJECT_PATH}/tokenizer/shortcuts_dict.txt"

SPECIAL_TOKENS_REG_EXPRESSIONS = {
    DATE_TOKEN: [
        re.compile(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'),
        re.compile(r'([12]\d{3}.(0[1-9]|1[0-2]).(0[1-9]|[12]\d|3[01]))'),
    ],
    MAIL_TOKEN:[
        re.compile(r'([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)'),
    ]

}
#TODO Handle sentence 'Zakończenie skrótem r.?'


class Tokenizer(object):
    def __init__(self):
        super(Tokenizer, self).__init__()
        self.shortcuts_exceptions = self.load_shortucts_exceptions_file()
        self.shortcuts_dict = self.load_shortucts_dict()

    def load_shortucts_exceptions_file(self):
        shortcuts = {}
        f = open(f"{SHORTCUTS_EXCEPTION_FILEPATH}", "r")
        for x in f:
            x = x.replace("\r\n", "\n").replace("\n", "")
            splitted = x.split(":")
            shortcuts[splitted[0]] = splitted[1]

        return shortcuts

    def load_shortucts_dict(self):
        shortcuts = {}
        f = open(f"{SHORTCUTS_DICT_FILEPATH}", "r")
        for x in f:
            x = x.replace("\r\n", "\n").replace("\n", "")
            splitted = x.split(":")
            shortcuts[splitted[0]] = splitted[1]

        return shortcuts

    def tokenize(self, data) -> list:
        output = list()
        for text in data:
            text = text.replace("\n", "")
            sentences = self.get_sentences(text)
            sentences = [sentence for sentence in sentences if sentence!=""]
            for sentence in sentences:
                output.append(self.tokenize_sentence(sentence))

        sentences = self.__merge_sentences_by_not_ending_shortcut(output)
        sentences = self.get_with_tokens_notation(sentences)
        sentences = [[self.check_possible_tokens_by_regexps(tokens) for tokens in tokenized] for tokenized in sentences]
        sentences = [self.check_for_shortcuts_tokens(tokenized_sentence) for tokenized_sentence in sentences]
        sentences = [self.replace_shortcuts_with_full_version(tokenized_sentence) for tokenized_sentence in sentences]
        return sentences

    def get_with_tokens_notation(self, sentences):
        new_sentences = []
        for sentence in sentences:
            new_sentence = []
            for token in sentence:
                new_sentence.append((token, DEFAULT_TOKEN))
            new_sentences.append(new_sentence)
        return new_sentences

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

    def check_possible_tokens_by_regexps(self, token):
        for key, value in SPECIAL_TOKENS_REG_EXPRESSIONS.items():
            for regexp in value:
                word, token_type = token
                if regexp.match(word):
                    token = (word, key)

        return token

    def check_for_shortcuts_tokens(self, tokenized_sentence):
        for i in range(len(tokenized_sentence)):
            word, token_type = tokenized_sentence[i]
            if word in self.shortcuts_dict.keys():
                tokenized_sentence[i] = (word, SHORTCUT_TOKEN)
                if i == len(tokenized_sentence) - 1 and word[-1] == '.':
                    tokenized_sentence.append((".", DEFAULT_TOKEN))

        return tokenized_sentence

    def replace_shortcuts_with_full_version(self, sentence):
        for i in range(len(sentence)):
            word, token_type = sentence[i]
            if token_type == SHORTCUT_TOKEN:
                sentence[i] = (self.shortcuts_dict[word], token_type)

        return sentence

    def white_space_tokenizer(self, string):
        return string.split(" ")

    def __merge_sentences_by_not_ending_shortcut(self, sentences):
        last_sentence_last_word = ""
        new_sentences = []
        for sentence in sentences:
            if last_sentence_last_word in self.shortcuts_exceptions.keys():
                new_sentences[-1].extend(sentence)
            else:
                new_sentences.append(sentence)
            last_sentence_last_word = f"{sentence[-1]}"

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