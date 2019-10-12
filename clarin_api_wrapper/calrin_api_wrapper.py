from collections import OrderedDict

import requests


class ClarinApiWrapper():
    """
    Wrapper for requesting Clarin-Pl API.
    Class allows to send json requests to Clarin-Pl API.
    Input json has a following keys:
        - tool - one of four Clarin's tools
        - task - tool-secified
        - lexeme - lexeme or list of lexemes to process
        - options - other option, not required and not implemented.

    """
    def __init__(self, tool: str = "all", task: str = "all"):
        """
        Initializer for ClarinApiWrapper.
        :param tool: 5 values available:
                    - morfeusz - morphological analyser and generator
                    - word2vec
                    - plwordnet
                    - walenty
                    - all - use all tools.
        :param task: all - ask for all tasks, other values are tool-dependent.
        """
        self.__url = 'http://ws.clarin-pl.eu/lexrest/lex/'
        # application/json - defined in clarin docs
        # charset=utf-8 cos of diacritic characters in Polish
        self.__headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.__tool = tool
        self.__task = task

    def request(self, lexeme, task=None) -> list:
        if task is None:
            task = self.__task
        input_json = self._create_input_json(lexeme, task)
        response = requests.post(self.__url, json=input_json, headers=self.__headers)
        response_json = response.json()
        return response_json['results']

    def _create_input_json(self, lexeme, task: str) -> dict:
        input_json = {"task": task,
                 "lexeme": lexeme,
                 "tool": self.__tool}
        return input_json



