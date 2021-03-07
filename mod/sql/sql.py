import sqlite3
from sqlite3 import Error
from ..loadConfig import config

class sql:

    conn = None

    def __init__(self) -> None:
        pass

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            print("Data Connection OK")
        except Error as e:
            print(e)
    
    def create_tables(self):
        try:
            c = self.conn.cursor()
            c.execute(config.config["sql"]["files"]["create"])
            print(config.config["sql"]["files"]["create"])
            c.execute(config.config["sql"]["lines"]["create"])
            print("Table Creation OK")
        except Error as e:
            print(e)
        finally:
            if c:
                c.close

    def insert_in_table(self, cmd, values_list):
        cur = self.conn.cursor()
        cur.execute(cmd, values_list)
        self.conn.commit()
        cur.close()
        return cur.lastrowid

    def fetch_from_table(self, cmd):
        sql_select_query = cmd
        cursor = self.conn.cursor()
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        cursor.close()
        return (records)

    def fetch_by_name_from_table(self, cmd, name):
        sql_select_query = cmd
        cursor = self.conn.cursor()
        cursor.execute(sql_select_query, (name,))
        records = cursor.fetchall()
        cursor.close()
        return (records)

    def end(self):
        self.conn.close()