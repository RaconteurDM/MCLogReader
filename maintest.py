# -*-coding:utf-8 -*
#!/usr/bin/env python

from mod.loadConfig.getConfig import config
import os
import mod

def stockFile(file):
    db = mod.sql()
    db.create_connection("db/db.db")
    db.create_tables()
    file_id = db.insert_in_table(config.config["sql"]["files"]["insert"], (file.filename, file.date.date, file.num))
    for line in file.lines:
        db.insert_in_table(config.config["sql"]["lines"]["insert"], (file_id, file.date.date, line.type, line.time.time, line.rawLine, "0"))
    db.end()


def maintest():
    test = mod.logData.file("logs/0-0-0-0.log")
    print(test.filename)
    print(test.rawLines[0])
    if not os.path.exists("db/db.db"):
        print("Existe pas")
        fichier = open("db/db.db", "w")
        fichier.close
    stockFile(test)

if __name__ == "__main__":
    maintest()