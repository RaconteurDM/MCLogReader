import gzip
import shutil
import re
import glob

from ..state import State
from .. import Sql
from enum import Enum
from ..loadConfig import Config
from .file import File

class ParseMode(Enum):
    EMPTY = 0,
    FILE = 1,
    ALL = 2

class LogStock:

    @classmethod
    def parseFile(cls, path):
        file_c = File(path)
        if (file_c.state != State.INVALID): 
            file_id = Sql.insert_cmd(Config.config["sql"]["files"]["insert"], (file_c.filename, file_c.date.date, file_c.num))
            if file_id is not None:
                for line in file_c.lines:
                    Sql.insert_cmd(Config.config["sql"]["lines"]["insert"], (file_id, file_c.date.date, line.type, line.time.time, line.rawLine, line.ipSet))

    @classmethod
    def parseAllFiles(cls, dirPath):
        for file in glob.glob(dirPath + "/*"):
            print(file)
            cls.parseFile(file)

    @classmethod
    def decompressAllLogs(cls, dirpath):
        for entry in glob.glob(dirpath + "/*"):
            print(entry)
            if (re.match(".*[0-9]+-[0-9]+-[0-9]+\\.log(\\.gz)?", entry)):
                print(re.split("/|\\\\", (entry.split(".")[0]))[-1] + "." + entry.split(".")[1])
                name = re.split("/|\\\\", (entry.split(".")[0]))[-1] + "." + entry.split(".")[1]
                cls.decompressLog(entry, "./logs", name)

    @classmethod
    def decompressLog(cls, logPath, logDirDest, name):
        if (logPath.split(".")[-1] == "log"):
            with open(logPath, "rb") as f_in:
                with open(logDirDest +  "/" + name, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
        elif (logPath.split(".")[-1] == "gz"):
            with gzip.open(logPath, "rb") as f_in:
                with open(logDirDest +  "/" + name, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)