from clarin_api_wrapper.clarin_lexeme_api_wrapper import ClarinLexemeApiWrapper


class MorfeuszWrapperLexeme(ClarinLexemeApiWrapper):
    """
    Morfeusz tool has two tasks available:
        - analyse,
        - generate.
    """
    def __init__(self):
        super().__init__("morfeusz", "all")

    def analyse(self, lexeme) -> dict:
        """
        Morphological analysis of words.
        :param lexeme: one word or list of words
        :return: Morfeusz response as list of (in Polish):
            [form (forma), lemma (lemat), tag,  name (nazwa),  qualifier (kwalifikator)]
        """
        return super().request(lexeme=lexeme,
                               task="analyse")

    def generate(self, lexeme) -> dict:
        return super().request(lexeme=lexeme,
                               task="generate")