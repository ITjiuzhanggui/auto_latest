import configparser
import os
import json


class ConfManagement(object):
    def __init__(self, section="default"):
        self.section = section
        self.curpath = os.path.dirname(os.path.realpath(__file__))
        self.inipath = os.path.join(self.curpath, "conf.ini")
        self.conf = configparser.ConfigParser()
        self.conf.read(self.inipath)

    def get_ini(self, value):
        return self.conf.get(self.section, value)

    def set_ini(self, session, value):
        self.conf.set(self.section, session, value)
        self.conf.write(open(self.inipath, "w+"))

# from conf import ConfManagement
# ConfManagement("pro").get("viewphone")
# ConfManagement().set(session="appPackage",value="B")
# print(ConfManagement().get_ini("debug"))
