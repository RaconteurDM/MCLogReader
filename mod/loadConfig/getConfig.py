import json

class Config:

    config = dict()

    def __init__(self):
        file_str = ""
        with open("config/config.json", "r", encoding='ISO-8859-1') as file:
            configJSON = json.load(file)
        self.config["minecraft"] = configJSON["minecraft"]["regular"]
        self.config["paths"] = configJSON["paths_config"]
        self.config["sql"] = configJSON["sql_config"]

Config()