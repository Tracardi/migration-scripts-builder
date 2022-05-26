import os


class AppConfig:

    def __init__(self, environment):
        self.elastic_host = environment["ELASTIC_HOST"] if "ELASTIC_HOST" in environment else "http://localhost:9200"


config = AppConfig(os.environ)
