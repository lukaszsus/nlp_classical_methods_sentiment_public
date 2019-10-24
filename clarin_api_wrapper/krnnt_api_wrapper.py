import requests
import xml.etree.ElementTree as ET


class KRNNTWrapper(object):
    def __init__(self):
        self.__url = 'http://localhost:9200/'
        # application/json - defined in clarin docs
        # charset=utf-8 cos of diacritic characters in Polish
        self.__headers = {'Content-Type': 'application/json; charset=UTF-8'}

    def analyse(self, texts):
        return self.parse_response(self.request(texts))

    def parse_response(self, response):
        splitted = response.split("\n")
        splitted = [line for line in splitted if line != '']
        data = [[i.split('\t'), j.split('\t')] for i, j in zip(splitted[::2], splitted[1::2])]

        sentences = []

        tokens = []

        for row in data:
            result_token = {}
            orth_text = row[0][0]
            result_token['orth'] = orth_text
            result_token['lex'] = {
                'disamb': 1,
                'base': row[1][1],
                'ctag': row[1][2]
            }

            if orth_text == "EOF":
                sentences.append(tokens)
                tokens = []
            else:
                tokens.append(result_token)

        return sentences

    def request(self, text):
        input_json = text
        response = requests.post(self.__url, data=input_json.encode('utf-8'), headers=self.__headers)
        response_xml = response.content
        return response_xml.decode()


