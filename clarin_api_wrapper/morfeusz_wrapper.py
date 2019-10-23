import xml.etree.ElementTree as ET
import re
from clarin_api_wrapper.clarin_lexeme_api_wrapper import ClarinLexemeApiWrapper


class MorfeuszWrapperLexeme(ClarinLexemeApiWrapper):
    """
    Morfeusz tool has two tasks available:
        - analyse,
        - generate.
    """
    def __init__(self):
        super().__init__("morfeusz", "all")

    def analyse(self, words, as_xml = False) -> dict:
        """
        Morphological analysis of words.
        :param words: one word or list of words
        :return: Morfeusz response as list of (in Polish):
            [form (forma), lemma (lemat), tag,  name (nazwa),  qualifier (kwalifikator)]
        """
        self.__order = words
        response = super().request(lexeme=words, task="analyse")
        if as_xml:
            response = self.parse_response_to_xml_ccl(response)
        return response

    def generate(self, lexeme) -> dict:
        return super().request(lexeme=lexeme,
                               task="generate")

    def parse_response_to_xml_ccl(self, response: dict):
        """
        :param response: contains one sentence always as dict
        :return:
        """
        chunkList = ET.Element("chunkList")
        chunk = ET.SubElement(chunkList, "chunk", id="ch1")
        sentence = ET.SubElement(chunk, "sentence", id="s1")
        for word in self.__order:
            analysis = response[word]
            tok = ET.SubElement(sentence, "tok")
            ET.SubElement(tok, "orth").text = word
            for proposition in analysis:
                self.__insert_lex_to_xml(tok, proposition)

        tree = ET.ElementTree(chunkList)
        tree.write("morfeusz_output.xml", encoding='utf-8', xml_declaration=True)
        with open("morfeusz_output.xml", 'r') as file:
            xml = file.read()
        return xml

    def __insert_lex_to_xml(self, tok, proposition):
        # proposition[2] = proposition[2].replace(":_", "")
        # proposition[2] = proposition[2].replace(":n2", ":n")
        # proposition[2] = proposition[2].replace("dig", "num")
        # m = re.search(r"(.+:)([^:]+)\.([^:]+)(:.+)", proposition[2])
        # if m:
        #     before = m.group(1)
        #     tag1 = m.group(2)
        #     tag2 = m.group(3)
        #     after = m.group(4)
        #     self.__insert_lex_to_xml(tok, [proposition[0], proposition[1], before + tag1 + after])
        #     self.__insert_lex_to_xml(tok, [proposition[0], proposition[1], before + tag2 + after])
        # else:
        lex = ET.SubElement(tok, "lex")
        ET.SubElement(lex, "base").text = proposition[1]
        ET.SubElement(lex, "ctag").text = proposition[2]
