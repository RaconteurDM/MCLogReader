import sqlite3
from sqlite3 import Error
from ..loadConfig import Config

class Sql(object):

    conn = None
    init = True

    @classmethod
    def __init__(cls) -> None:
        db_file = Config.config["paths"]["db_path"]
        if (cls.init):
            cls.create_connection(db_file)
            cls.create_basic_tables()
            cls.init = False

    @classmethod
    def create_connection(cls, db_file):
        try:
            cls.conn = sqlite3.connect(db_file)
            print("Data Connection OK")
        except Error as e:
            print(e)

    @classmethod
    def create_basic_tables(cls):
        try:
            c = cls.conn.cursor()
            c.execute(Config.config["sql"]["files"]["create"])
            c.execute(Config.config["sql"]["serveurs"]["create"])
            c.execute(Config.config["sql"]["serveurs_ip"]["create"])
            c.execute(Config.config["sql"]["lines"]["create"])
            print("Table Creation OK")
        except Error as e:
            print(e)
        finally:
            if c:
                c.close()

    @classmethod
    def insert_cmd(cls, cmd, values_list):
        try:
            cur = cls.conn.cursor()
            cur.execute(cmd, values_list)
            cls.conn.commit()
        except Error as e:
            print(e)
        finally:
            cur.close()
            return cur.lastrowid

    @classmethod
    def fetch_cmd(cls, cmd):
        try:
            sql_select_query = cmd
            cursor = cls.conn.cursor()
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            return (records)

    @classmethod
    def fetch_by_value_cmd(cls, cmd, values):
        t_values = tuple(values)
        try:
            sql_select_query = cmd
            cursor = cls.conn.cursor()
            cursor.execute(sql_select_query, t_values)
            records = cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            return (records)

    @classmethod
    def insert_in_table(cls, table, values_names, values):
        t_values_names = tuple(values_names)
        t_values = tuple(values)
        cmd = "INSERT INTO " + table + "(" + ', '.join(t_values_names) + ") VALUES" + cls.gen_tuple_values(cls, len(values))
        insert_ret = cls.insert_cmd(cls, cmd, t_values)
        return (insert_ret)

    @classmethod
    def gen_tuple_values(cls, size):
        tup = "("
        for i in range(size - 1):
            tup += "?,"
        tup += "?)"
        return (tup)

    @classmethod
    def fetch_all(cls, table):
        cmd = "select * from " + table
        ret_fetch = cls.fetch_cmd(cmd)
        return (ret_fetch)

    @classmethod
    def fetch_by_value(cls, table, values_names, values):
        cmd = "select * from " + table + " WHERE " + '=? AND WHERE '.join(values_names) + "=?"
        ret_fetch = cls.fetch_by_value_cmd(cmd, values)
        return (ret_fetch)

    @classmethod
    def exist(cls, table, values_names, values):
        t_values = tuple(values)
        c = cls.conn.cursor()
        cmd = "select 1 from " + table + " WHERE " + '=? AND WHERE '.join(values_names) + "=?"
        ret = True
        val = c.execute(cmd, t_values).fetchone()
        if not val or len(val) == 0:
            ret = False
        c.close()
        return ret

    @classmethod
    def end(cls):
        if cls.conn:
            cls.conn.close()