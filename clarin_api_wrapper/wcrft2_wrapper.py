from clarin_api_wrapper.clarin_nlprest2_api_wrapper import ClarinNlprest2ApiWrapper
import xml.etree.ElementTree as ET


class Wcrft2Wrapper(ClarinNlprest2ApiWrapper):
    def __init__(self):
        super().__init__("any2txt | wcrft2({\"guesser\": false, \"morfeusz2\": true})",
                         "dummy@student.pwr.edu.pl")

    def analyse(self, text):
        return self.parse_response(super().request(text=text))

    def parse_response(self, response: str):
        root = ET.fromstring(response)
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