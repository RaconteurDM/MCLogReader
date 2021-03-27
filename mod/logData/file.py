# -*-coding:utf-8 -*

import re
from ..time import Date
from ..state import State
from .line import Line
from .serveur import Serveur
from .. import Sql
import codecs

class File:

    reVerif = re.compile(r"(.+(\\|/)+)*[0-9]*-[0-9]*-[0-9]*-[0-9]*\.log")
    reFilename = re.compile(r"[0-9]*-[0-9]*-[0-9]*-[0-9]*")

    lastServIp = "Unkown"
    lastServCompleteIp = "Unknown"

    ipSet_id = -1

    def __init__(self, filepath):
        if self.ipSet_id == -1:
            self.ipSet_id = Serveur(self.lastServIp, self.lastServCompleteIp).serv_ip_id
        self.state = State.INVALID
        self.filename = "Invalid"
        self.rawLines = list()
        self.lines = list()

        match = self.reFilename.search(filepath)
        self.filename = match.group()

        if Sql.exist("files", ["Name",], [self.filename,]):
            return

        if (self.reVerif.match(filepath) is not None):
            self.state = State.VALID

            file = codecs.open(filepath, "r", encoding='ISO-8859-1')
            self.rawLines = file.readlines()
            file.close()

            self.date = Date(self.filename)
            self.num = self.date.num

            self.listAllLines()

    def listAllLines(self):
        for rawLine in self.rawLines:
            newLine = Line(rawLine)
            if (newLine.type == "connection"):
                self.lastServIp = newLine.ip
                self.lastServCompleteIp = newLine.completeIp
                self.ipSet_id = Serveur(self.lastServIp, self.lastServCompleteIp).serv_ip_id
            else:
                newLine.ip = self.lastServIp
                newLine.completeIp = self.lastServCompleteIp
            newLine.ipSet = self.ipSet_id
            self.lines.append(newLine)