from stop_words import get_stop_words
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from tokenizer.tokenizer import Tokenizer
import numpy as np

class SentimentModel():
    def __init__(self, tagger_wrapper):
        self.tagger_wrapper = tagger_wrapper
        self.stop_words = get_stop_words("pl")
        self.vectorizer = CountVectorizer()
        self.nb_model = MultinomialNB()

    def fit(self, x_train, y_train, part_of_speech=None, tagger_preprocessed=False):
        """
        Fit model to training set.
        :param x_train:
        :param y_train:
        :param part_of_speech: possible values: verb, noun, adjective, None
        :return:
        """
        preprocessed = self.preprocess_texts(x_train, part_of_speech=part_of_speech,
                                             tagger_preprocessed=tagger_preprocessed)
        X = self.fit_vectorizer(preprocessed)
        self.fit_nb_model(X_train=X, y_train=y_train)
        print("Got lematized texts")

    def predict(self, X, part_of_speech=None, tagger_preprocessed=False, sentence_level=False):

        i = 0
        if sentence_level:
            results = []
            for text in X:
                tokenizer = Tokenizer()
                sentences = tokenizer.tokenize([text])
                sentences = [" ".join([token[0] for token in sentence]) for sentence in sentences]

                preprocessed_sentences = self.preprocess_texts(sentences, part_of_speech=part_of_speech,
                                                         tagger_preprocessed=tagger_preprocessed)

                X = self.vectorizer.transform(preprocessed_sentences).toarray()
                pred = self.nb_model.predict(X)
                results.append(int(round(np.mean(pred))))
                print(i)
                i += 1
            return np.array(results)

        else:
            preprocessed = self.preprocess_texts(X, part_of_speech=part_of_speech,
                                                 tagger_preprocessed=tagger_preprocessed)
            X = self.vectorizer.transform(preprocessed).toarray()
            return self.nb_model.predict(X)

    def preprocess_texts(self, texts, part_of_speech=None, tagger_preprocessed=False):
        if not tagger_preprocessed:
            tagger_analyzed = self.tagger_wrapper.analyse(" EOF ".join(list(texts)) + " EOF ")
        else:
            tagger_analyzed = texts

        filter_out_interp = self.filter_out_tokens_tags(tagger_analyzed, ['interp'])
        filter_in_form_class = self.filter_in_part_of_speech(filter_out_interp, part_of_speech=part_of_speech)
        lemmatized_texts = self.get_lemmatized_sentences(filter_in_form_class)
        removed_stop_words = self.remove_stop_words(lemmatized_texts)
        data = [" ".join(sentence) for sentence in removed_stop_words]
        return data

    def fit_vectorizer(self, X_train):
        X = self.vectorizer.fit_transform(X_train)
        return X

    def fit_nb_model(self, X_train, y_train):
        x_train = X_train.toarray()
        print(x_train.shape)
        y_train = y_train.squeeze().astype(int)
        self.nb_model.fit(x_train, y_train)

    def filter_in_part_of_speech(self, data, part_of_speech: str = None):
        """
        :param data: list of tagged sentences
        :param part_of_speech: possible values: verb, noun, adjective, None
        :return: filtered tags, if form_class is None, then leave all tags (nothing is filter out)
        """
        if part_of_speech is None:
            return data
        else:
            tags = self.__get_part_of_speech_tags(part_of_speech)
        new_data = []

        for sentence in data:
            tokens = [token for token in sentence if any(tag in token['lex']['ctag'] for tag in tags)]
            new_data.append(tokens)

        return new_data

    def __get_part_of_speech_tags(self, form_class: str):
        """
        :param form_class: possible values: verb, noun, adjective, None
        :return: nkjp tags appropriate for form class
        """
        if form_class == 'verb':
            return ['fin', 'bedzie', 'aglt', 'praet', 'impt', 'imps', 'inf', 'pcon',
                    'pant', 'ger', 'pact', 'ppas', 'winien']
        if form_class == 'noun':
            return ['subst', 'depr']
        if form_class == 'adj':
            return ['adj', 'adja', 'adjp', 'adjc']

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
