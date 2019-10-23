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
        return response_xml.decode()

    def _create_input_json(self, text) -> dict:
        input_json = {"lpmn": self.__lpmn,
                 "text": text,
                 "user": self.__user}
        return input_json


