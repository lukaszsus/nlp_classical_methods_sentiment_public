from clarin_api_wrapper import wcrft2_wrapper
import xml.etree.ElementTree as ET
from stop_words import get_stop_words

class SentimentModel():
    def __init__(self, tagger_wrapper):
        self.tagger_wrapper = tagger_wrapper
        self.stop_words = get_stop_words("pl")

    def fit(self, x_train, y_train):
        tagger_analyzed = self.analyze_data_with_tagger(x_train)
        print("Got data analyzed by tagger")
        print(tagger_analyzed)
        filter_out_interp = self.filter_out_tokens_tags(tagger_analyzed, ['interp'])
        print(filter_out_interp)
        lemmatized_texts = self.get_lemmatized_sentences(filter_out_interp)
        print(lemmatized_texts)
        removed_stop_words = self.remove_stop_words(lemmatized_texts)
        print(removed_stop_words)
        print("Got lematized texts")

    def analyze_data_with_tagger(self, x_train):
        result = self.tagger_wrapper.analyse(" EOF ".join(list(x_train)) + "EOF")
        root = ET.fromstring(result)
        sentences = []
        print("Got data from tagger")
        tokens = []
        for chunk in root:
            sent = chunk.find("sentence")
            for token in sent.iter('tok'):
                result_token = {}
                orth = token.find("orth")
                lex = token.find("lex")
                orth_text = orth.text
                result_token['orth'] = orth_text
                result_token['lex'] = {
                    'disamb': lex.get("disamb"),
                    'base': lex.find("base").text,
                    'ctag': lex.find("ctag").text,
                }

                if orth_text == "EOF":
                    sentences.append(tokens)
                    tokens = []
                else:
                    tokens.append(result_token)

        return sentences

    def filter_out_tokens_tags(self, data, tags):
        new_data = []

        for sentence in data:
            tokens = [token for token in sentence if token['lex']['ctag'] not in tags]
            new_data.append(tokens)

        return new_data

    def get_lemmatized_sentences(self, data):
        new_data = []

        for sentence in data:
            tokens = [token['lex']['base'] for token in sentence]
            new_data.append(tokens)

        return new_data

    def remove_stop_words(self, data):
        new_data = []

        for sentence in data:
            tokens = [token for token in sentence if token not in self.stop_words]
            new_data.append(tokens)

        return new_data