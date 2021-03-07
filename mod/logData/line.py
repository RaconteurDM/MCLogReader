import re
from ..loadConfig import config
from ..time import time

class line:

    connection = dict()
    for type, strRe in config.config["minecraft"]["serveur"].items():
        connection[type] = re.compile(strRe)

    def __init__(self, rawLine) -> None:
        self.rawLine = rawLine
        self.type = "Unknown"
        reChat = re.compile(config.config["minecraft"]["regular_chat_line"])
        self.serv = "Unknown"

        self.wordList = rawLine.strip().split(" ")
        self.time = time(self.wordList[0])
        if (reChat.match(rawLine)):
            self.type = "Chat"
        else:
            for type, regex in self.connection.items():
                if (regex.match(rawLine)):
                    self.type = type
            if (self.type == "Connection"):
                self.completeIp = self.wordList[4].replace(",", ":") + self.wordList[5]
                self.ip = self.wordList[4]
