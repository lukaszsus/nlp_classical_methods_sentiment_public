from clarin_api_wrapper.clarin_nlprest2_api_wrapper import ClarinNlprest2ApiWrapper


class Wcrft2Wrapper(ClarinNlprest2ApiWrapper):
    def __init__(self):
        super().__init__("any2txt | wcrft2({\"guesser\": false, \"morfeusz2\": true})",
                         "dummy@student.pwr.edu.pl")

    def analyse(self, text) -> dict:
        return super().request(text=text)