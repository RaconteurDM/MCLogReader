import os
from ..sql import Sql
from enum import Enum
from ..loadConfig import Config

class Serveur:

    def __init__(self, ip, complete_ip) -> None:
        values_names = list()
        values = list()
        values_names.append("server_complete_ip")
        values.append(complete_ip)
        if Sql.exist("serveurs_ip", values_names, values):
            self.serv_ip_id = Sql.fetch_by_value("serveurs_ip", values_names, values)[0][0]
        else:
            self.createIpSet("DEFAULT", ip, complete_ip)

    def createIpSet(self, serv_name, ip, complete_ip):
        values = (serv_name, ip, complete_ip)
        self.serv_ip_id = Sql.insert_cmd(Config.config["sql"]["serveurs_ip"]["insert"], values)
        print("New ip set: IP=" + ip + " completeIP=" + complete_ip)

