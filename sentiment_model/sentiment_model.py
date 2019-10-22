from stop_words import get_stop_words


class SentimentModel():
    def __init__(self, tagger_wrapper):
        self.tagger_wrapper = tagger_wrapper
        self.stop_words = get_stop_words("pl")

    def fit(self, x_train, y_train, part_of_speech=None):
        """
        Fit model to training set.
        :param x_train:
        :param y_train:
        :param part_of_speech: possible values: verb, noun, adjective, None
        :return:
        """
        tagger_analyzed = self.tagger_wrapper.analyse(" EOF ".join(list(x_train)) + "EOF")
        print("Got data analyzed by tagger")
        print(tagger_analyzed)
        filter_out_interp = self.filter_out_tokens_tags(tagger_analyzed, ['interp'])
        print(filter_out_interp)
        filter_in_form_class = self.filter_in_part_of_speech(filter_out_interp, part_of_speech=part_of_speech)
        print(filter_in_form_class)
        lemmatized_texts = self.get_lemmatized_sentences(filter_in_form_class)
        print(lemmatized_texts)
        removed_stop_words = self.remove_stop_words(lemmatized_texts)
        print(removed_stop_words)
        print("Got lematized texts")

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