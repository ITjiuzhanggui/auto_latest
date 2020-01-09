#!/usr/bin/env python3
import time
import os
from logs import SetLog
from core.abstract import exect_contest
from conf import ConfManagement
from core.defaultslog import *
from core.clearlogs import *
from core.statusDef import *
from core.statusCle import *

auto_path = ConfManagement().get_ini("AUTOMATEDLOGPARSING")

date = time.strftime("%Y-%m-%d", time.localtime()).replace(' ', ':').replace(':', ':')

CURPATH = os.path.dirname(os.path.realpath(__file__)) + "/%s" % date
os.makedirs(CURPATH, exist_ok=True)

JSON_PATH = os.path.join(CURPATH, "json")
os.makedirs(JSON_PATH, exist_ok=True)
JSON_STATUS_PATH = os.path.join(JSON_PATH, "status")
JSON_TEST_PATH = os.path.join(JSON_PATH, "test")
os.makedirs(JSON_TEST_PATH, exist_ok=True)
os.makedirs(JSON_STATUS_PATH, exist_ok=True)
os.system("chmod a+x 1.sh")
os.system("cp 1.sh %s/" % auto_path)


def get_log_update(cmd, logs_patg):
    SetLog().info("updte:cmd:%s" % cmd)
    for i in range(5):
        SetLog().info("*****************")
        os.system("{} > {}/{}.log 2>&1 ".format(
            cmd, logs_patg, time.strftime( \
                "%Y-%m-%d-%H:%M:%S", \
                time.localtime()).replace(' ', ':'). \
                replace(':', ':'))
        )


path = os.path.join(CURPATH, "update")
os.makedirs(path, exist_ok=True)
make_path = auto_path + "/1.sh"
make_path += " %s make update" % auto_path
get_log_update(make_path, path)


def get_log_status(cmd, logs_patg):
    SetLog().info("status:cmd:%s" % cmd)
    for i in range(1):
        SetLog().info("++++++++++++++++")
        os.system("{} > {}/{}.log 2>&1 ".format(
            cmd, logs_patg, time.strftime( \
                "%Y-%m-%d-%H:%M:%S", \
                time.localtime()).replace(' ', ':'). \
                replace(':', ':'))
        )


path = os.path.join(CURPATH, "status_log")
os.makedirs(path, exist_ok=True)
make_path = auto_path + '/1.sh'
make_path += " %s make status" % auto_path
get_log_status(make_path, path)

test_cmd = ["make httpd", "make nginx", "make memcached", "make redis", "make php", "make python", "make node",
            "make golang", "make postgres", "make tensorflow", "make mariadb", "make perl", "make openjdk",
            "make rabbitmq", "make flink", "make cassandra", "make ruby"]


def get_log_test(cmd, logs_patg):
    SetLog().info("test:cmd:%s" % cmd)
    for i in range(5):
        SetLog().info("-----------------------")
        os.system("{} > {}/{}.log 2>&1 ".format(
            cmd, logs_patg, time.strftime( \
                "%Y-%m-%d-%H:%M:%S", \
                time.localtime()).replace(' ', ':'). \
                replace(':', ':'))
        )


for i in test_cmd:
    path = os.path.join(CURPATH, "test_log")
    path = os.path.join(path, i.split(' ')[-1])
    os.makedirs(path, exist_ok=True)
    make_path = auto_path + '/1.sh'
    make_path += " {} {} ".format(auto_path, i)
    get_log_test(make_path, path)

for num in range(1):
    SetLog().info("Successfully written:log_file")

sh = auto_path + '/1.sh'
os.system("rm %s" % sh)
