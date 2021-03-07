# -*-coding:utf-8 -*

import re
from ..time import date
from ..state import state
from .line import line
import codecs

class file:

    reVerif = re.compile(r"(.+(\\|/)+)*[0-9]*-[0-9]*-[0-9]*-[0-9]*\.log")
    reFilename = re.compile(r"[0-9]*-[0-9]*-[0-9]*-[0-9]*")

    def __init__(self, filepath):
        self.state = state.INVALID
        self.filename = "Invalid"
        self.rawLines = list()
        self.lines = list()
        self.lastServIp = "Unknown"
        self.lastServCompleteIp = "Unknown"

        if (self.reVerif.match(filepath) is not None):
            self.state = state.VALID

            match = self.reFilename.search(filepath)
            self.filename = match.group()

            file = codecs.open(filepath, "r", encoding='ISO-8859-1')
            self.rawLines = file.readlines()
            file.close()

            self.date = date(self.filename)
            self.num = self.date.num

            self.listAllLines()

    def listAllLines(self):
        for rawLine in self.rawLines:
            newLine = line(rawLine)
            if (line.type == "Connection"):
                self.lastServIp = newLine.ip
                self.lastServCompleteIp = newLine.completeIp
            else:
                newLine.ip = self.lastServIp
                newLine.completeIp = newLine.completeIp
            self.lines.append(line(rawLine))