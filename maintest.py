# -*-coding:utf-8 -*
#!/usr/bin/env python

from mod.logData.LogStock import LogStock
from mod.logData.LogStock import ParseMode
from mod.loadConfig.getConfig import Config
import os
import mod

def maintest():
    if not os.path.exists("db/db.db"):
        print("Existe pas")
        fichier = open("db/db.db", "w")
        fichier.close
    mod.Sql()
    #LogStock.decompressAllLogs("/home/paulbrancieq/projects/MCLogReader/logsorigin")
    LogStock.parseAllFiles("./logs")
    #LogStock.parseFile("logs/0-0-0-0.log")
    mod.Sql.end()

if __name__ == "__main__":
    maintest()