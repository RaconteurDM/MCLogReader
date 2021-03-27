import re
from ..loadConfig import Config
from ..time import Time

class Line:

    connection = dict()
    for type, strRe in Config.config["minecraft"]["serveur"].items():
        connection[type] = re.compile(strRe)

    def __init__(self, rawLine) -> None:
        self.rawLine = rawLine
        self.type = "Unknown"
        reChat = re.compile(Config.config["minecraft"]["regular_chat_line"])
        self.serv = "Unknown"
        self.completeIp = ""
        self.ip = ""
        self.ipSet = 0
        

        self.wordList = rawLine.strip().split(" ")
        self.time = Time(self.wordList[0])
        if (reChat.match(rawLine)):
            self.type = "Chat"
        else:
            for type, regex in self.connection.items():
                if (regex.match(rawLine)):
                    self.type = type
            if (self.type == "connection"):
                self.completeIp = self.wordList[4].replace(",", ":") + self.wordList[5]
                self.ip = self.wordList[4].replace(",", "")