from clarin_api_wrapper.clarin_nlprest2_api_wrapper import ClarinNlprest2ApiWrapper


class MorphoditaWrapper(ClarinNlprest2ApiWrapper):
    def __init__(self, version: str="XXI"):
        super().__init__("any2txt|morphoDita({\"guesser\":false, \"allforms\":false, \"model\":\"" + version + "\"})",
                         "dummy@student.pwr.edu.pl")

    def analyse(self, text) -> dict:
        return super().request(text=text)