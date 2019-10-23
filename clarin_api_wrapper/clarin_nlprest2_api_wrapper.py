import requests
import xml.etree.ElementTree as ET


class ClarinNlprest2ApiWrapper():
    def __init__(self, lpmn: str, user: str):
        self.__url = 'http://ws.clarin-pl.eu/nlprest2/base/process'
        # application/json - defined in clarin docs
        # charset=utf-8 cos of diacritic characters in Polish
        self.__headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.__lpmn = lpmn
        self.__user = user

    def request(self, text):
        input_json = self._create_input_json(text)
        response = requests.post(self.__url, json=input_json, headers=self.__headers)
        response_xml = response.content
        return self.parse_response(response_xml.decode())

    def _create_input_json(self, text) -> dict:
        input_json = {"lpmn": self.__lpmn,
                 "text": text,
                 "user": self.__user}
        return input_json

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



